#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from xio.core import resource
from xio.core.resource import handleRequest, getResponse
from xio.core import peer

from xio.core.request import Request, Response
from xio.core.lib.logs import log
from xio.core.lib.utils import is_string, urlparse

from xio import path
from xio.core.utils import spawn

import os
import posixpath
import sys
import traceback
import time

import importlib
import yaml

import collections

from functools import wraps

import requests
import json
import base64
import uuid
import inspect
import hashlib
import copy


from pprint import pprint


# to fix etx xio
_extdir = os.path.dirname(os.path.realpath(__file__)) + '/ext'
path.append(_extdir)


def getAppsFromDirectory(path):

    syspath = path
    p = path.split('/')

    apps = []
    sys.path.insert(0, syspath)
    if os.path.isdir(path):
        for name in os.listdir(path):
            try:
                directory = path + '/' + name
                if os.path.isdir(directory):
                    modpath = name + '.app'
                    mod = importlib.import_module(modpath, package='.')
                    apps.append((name, mod.app))
            except Exception as err:
                import xio
                import traceback
                xio.log.warning('unable to load', name, 'from', directory)
                # traceback.print_exc()
    sys.path.remove(syspath)
    return apps


def app(*args, **kwargs):
    return App.factory(*args, **kwargs)


def handleCache(func):

    @wraps(func)
    def _(res, req):

        method = req.xmethod or req.method

        xio_skip_cache = req.query.pop('xio_skip_cache', None)
        ttl = res._about.get('ttl') or res._about.get('methods', {}).get(method, {}).get('ttl')
        usecache = req.GET and ttl
        cached = None
        if usecache and not xio_skip_cache:

            print('----handlecache', res._about)
            service = req.service('cache')
            if service:
                uid = req.uid()
                cached = service.get(uid)
                print('----handlecache', cached)
                if cached and cached.status in (200, 201) and cached.content:
                    info = cached.content or {}
                    result = info.get('content')
                    print('found cache !!!', info)
                    req.response = Response(200)
                    req.response.content_type = info.get('content_type')
                    req.response.headers = info.get('headers', {})
                    # req.response.content = result
                    req.response.ttl = 0  # prevent multi caching
                    print('CACHED RESULT ....', str(req.response.content))
                    return result
        result = getResponse(res, req, func)
        try:
            response = req.response
            # pb if response is a resource
            if not ttl:
                if req.response.ttl and isinstance(req.response.ttl, int):
                    ttl = req.response.ttl

            write_cache = usecache and ttl and bool(response) and response.status == 200 and not inspect.isgenerator(response.content)
            if write_cache:
                # pb avec cache implicite (ttl setted to app about, not in resource about)
                #res._about.setdefault('ttl', ttl)
                #service = req.service('cache')
                if service:
                    uid = req.uid()
                    print(res._about, res)
                    print('write cache !!!!!!', uid, ttl, response.content)
                    headers = dict(response.headers)
                    service.put(uid, {'content': response.content, 'ttl': int(ttl), 'headers': headers})
        except Exception as err:
            print('cache error', err)
            traceback.print_exc()
        return result

    return _


def handleStats(func):

    @wraps(func)
    def _(self, req):
        # need explicit configuration => about.quota or about.stats
        """
        if req.path.startswith('www/'):
            statservice = self.get('services/stats')
            statservice.post({
                'userid': req.client.id,
                'path': req.path,
            })
        """
        return getResponse(self, req, func)
    return _


class App(peer.Peer):

    name = 'lambda'
    module = None
    directory = None
    _about = None
    _skip_handler_allowed = True

    def __init__(self, name=None, module=None, **kwargs):

        peer.Peer.__init__(self, **kwargs)

        if module:
            self.module = module
            self.directory = os.path.realpath(os.path.dirname(self.module.__file__)) if self.module else None
            self.load()

        self.endpoint = None
        self._started = None
        self.log = log
        self._events = {}
        self._started = 0

        self.init()

    @classmethod
    def factory(cls, id=None, *args, **kwargs):

        if is_string(id):
            module = sys.modules.get(id)
            if module:
                return cls(module=module, **kwargs)

        if callable(id) and inspect.isfunction(id):
            app = cls(*args, **kwargs)
            app.bind('www', id)
            return app

        kwargs.setdefault('_cls', cls)
        return peer.Peer.factory(id, *args, **kwargs)

    def load(self):
        module = self.module
        import xio
        # check env
        if os.path.isfile(self.directory + '/.env'):
            xio.env.load(self.directory + '/.env')
        # loading ext first because about can refer on
        if os.path.isdir(self.directory + '/ext'):

            xio.path.append(self.directory + '/ext')
            for childname, child in getAppsFromDirectory(self.directory + '/ext'):
                child = xio.app(child)
                self.put('ext/%s' % childname, child)

        # loading about.yml
        if os.path.isfile(self.directory + '/about.yml'):
            with open(self.directory + '/about.yml') as f:
                self._about = yaml.load(f)

        self.name = self._about.get('name')
        # register local apps in context
        if self.name and self.name.startswith('xrn:'):
            xio.register(self.name, self)

        if 'id' in self._about:
            self.id = self._about.get('id')
        else:
            # tofix - dev only, generate app key from name
            from xio.core.lib.crypto import crypto
            self.key = crypto.key(seed=self.name)
            self.id = self.key.account('ethereum').address
            self.token = self.key.generateToken('ethereum')

        # loading test
        if os.path.isfile(self.directory + '/tests.py') or os.path.isdir(self.directory + '/tests'):
            sys.path.insert(0, self.directory)
            try:
                print('.....', self.directory)
                import tests
                self._tests = tests
            except Exception as err:
                #import traceback
                # traceback.print_exc()
                log.warning('TEST LOADING FAILED', err)
                self._tests = None
            sys.path.remove(self.directory)

    def init(self):

        # auto inspect
        for m in dir(self):
            h = getattr(self, m)
            if callable(h) and hasattr(h, '__xio_path__'):
                self.bind(h.__xio_path__, h)

        self.redis = False
        try:
            import xio
            import redis
            endpoint = xio.env.get('redis')
            if endpoint:
                self.redis = redis.Redis(endpoint)  # if endpoint else redis.Redis()
        except Exception as err:
            self.log.debug('redis error : %s' % err)  # bug not at init ??

        # scheduler
        from .lib.cron import SchedulerService
        self.put('services/cron', SchedulerService(self))

        # pub/sub
        from .lib.pubsub import PubSubService
        self.put('services/pubsub', PubSubService(self))

        # stats/quota
        from .lib.stats import StatsService
        self.put('services/stats', StatsService(self))

        # cache
        from .lib.cache import CacheService
        self.put('services/cache', CacheService(self))

        """
        # build resources
        if self._about:
            resources = self._about.get('resources')
            if resources and isinstance(resources,dict):
                for path,info in list(self._about.get('resources',{}).items()):
                    handler_class = info.get('handler',None)
                    handler_path = info.get('path','')
                    handler_params = info.get('params',{})

                    handler_params['xio_id'] =  self.id
                    handler_params['xio_token'] = 'FAKE TOKEN' # tofix

                    rhandler = client.app(handler_class,handler_params)
                    rhandler.basepath = handler_path
                    rhandler.profile = handler_params # tofix
                    self.bind(path, rhandler )
        """

        # build services
        services = copy.deepcopy(self._about.get('services'))
        if services:
            log.info('=== LOADING SERVICES ===')
            for service in services:
                log.info('=== LOADING SERVICE ', service)
                name = service.pop('name')
                handler_class = service.get('handler', None)
                handler_params = service.get('params', {})

                if is_string(handler_class):
                    remotehandler = ':' in handler_class or '/' in handler_class
                    pythonhandler = not remotehandler and '.' in handler_class

                    if remotehandler:
                        servicehandler = xio.client(handler_class, handler_params, client=self)
                    else:
                        import importlib
                        p = handler_class.split('.')
                        classname = p.pop()
                        modulepath = '.'.join(p)
                        module = importlib.import_module(modulepath)
                        handler_class = getattr(module, classname)
                        servicehandler = handler_class(app=self, **handler_params)

                    if servicehandler:
                        # tofix: warning ! bug with self.put (eg cache)
                        self.put('services/%s' % name, servicehandler)
                    else:
                        log.warning('unable to load service', service)

        # www/xio/admin/*
        from .admin import enhance
        enhance(self)

        # create default 'www' (required for ABOUT call which fail if not www)
        if not 'www' in self._children:
            self.put('www', None)

        if self.directory:

            wwwdir = self.directory + '/www'
            if os.path.isdir(wwwdir):
                self.bind('www', resource.DirectoryHandler(wwwdir))

            # to fix cousion between static and www
            wwwstaticdir = self.directory + '/www/static'
            if os.path.isdir(wwwstaticdir):
                self.bind('www/static', resource.DirectoryHandler(wwwstaticdir))

    @handleRequest
    @handleCache
    @handleStats
    def render(self, req):
        """
        pb with code in this method not called if we use request ...
        """

        # self.log.info('RENDER', req.xmethod or req.method, repr(req.path), 'by', self # tofix: maximum recursion depth exceeded

        # handle test
        if not req.path and req.TEST:
            return self._handleTest(req)

        req.path = 'www/' + req.path if req.path else 'www'
        return self.request(req)

    def _handleCheck(self, req):

        # resouce check
        results = peer.Peer._handleCheck(self, req)

        # unittest
        print(self._tests)
        if self._tests:
            try:
                testresult = self._handleTest(req)
                result = (200, testresult)
            except Exception as err:
                import traceback
                traceback.print_exc()
                result = (500, err)
            results['test'] = result

        # check all sub services
        for name, service in self.get('services')._children.items():
            try:
                res = service.check()
                result = (res.status, res.content)
            except Exception as err:
                result = (500, err)
            results['service/%s' % name] = result
        return results

    def _handleTest(self, req):

        if self._tests:

            import unittest

            modules = [
                self._tests,
            ]

            suite = unittest.TestSuite()
            loader = unittest.TestLoader()
            for mod in modules:
                suitemod = loader.loadTestsFromModule(mod)
                suite.addTests(suitemod)
            results = unittest.TestResult()
            results.buffer = True
            suite.run(results)

            # for r in results:
            #    results.append(r)
        print(results)
        print(dir(results))
        return {
            'run': results.run
        }

    def run(self, loop=True, **options):

        self.start(**options)
        if loop:
            import time
            while True:
                time.sleep(0.1)

    def uwsgi(self):
        """
        run app in uwsgi thread
        return app as wsgi application
        usage :  uwsgi --python --module app:uwsgi()
        """
        import uwsgidecorators

        @uwsgidecorators.postfork
        @uwsgidecorators.thread
        def _run():
            self.run()

        return self

    def start(self, use_wsgi=False, **options):

        import xio

        if not use_wsgi:
            self.emit('start')

        http = options.get('http', xio.env.get('http', 8080))
        ws = options.get('ws', xio.env.get('ws'))
        debug = options.get('debug', xio.env.get('debug'))

        if http:
            self.put('etc/services/http', {'port': int(http)})
        if ws:
            self.put('etc/services/ws', {'port': int(ws)})
        if debug:
            log.setLevel('DEBUG')

        self._started = int(time.time())

        for name, res in list(self.get('etc/services')._children.items()):

            try:
                servicehandler = None
                if use_wsgi and name not in ['http', 'https', 'ws', 'wss']:
                    continue

                conf = copy.copy(res.content)  # need to kepp the original config for debug/map

                self.log.info('STARTING SERVICE %s (%s)' % (name, conf))

                if not isinstance(conf, dict):
                    servicehandler = conf
                else:
                    from .lib import websocket
                    from .lib import http

                    port = conf.get('port')
                    scheme = conf.get('scheme', name)
                    options = {}
                    path = conf.get('path')
                    if scheme == 'ws':
                        servicehandler = websocket.WebsocketService(app=self, port=port, **options)
                    elif scheme == 'http':
                        servicehandler = http.HttpService(app=self, path=path, port=port, **options)
                    elif scheme == 'https':
                        servicehandler = http.HttpsService(app=self, path=path, port=port, **options)

                if servicehandler and hasattr(servicehandler, 'start'):
                    servicehandler.start()
                    self.put('run/services/%s' % name, servicehandler)
            except Exception as err:
                self.log.error('STARTING SERVICE %s FAIL : %s' % (name, err))

        if not use_wsgi:
            # pb for uwsgi basic handle & theaded operation on start
            self.emit('started')
            self.debug()

    def __call__(self, environ, start_response=None):
        """
        this method can be used as WSGI callable as well as xio.app handler

        for wsgi in uwsgi context we have to start the app if not already do
        """

        # handle app as handler
        if isinstance(environ, Request):
            req = environ
            return self.request(req)

        if not self._started:  # need handler
            import xio
            print('...wsgi init')
            self.start(use_wsgi=True)

        if environ.get('HTTP_CONNECTION') == 'Upgrade' and environ.get('HTTP_UPGRADE') == 'websocket' and environ.get('HTTP_SEC_WEBSOCKET_KEY'):
            handler = self.get('run/services/ws')._handler
        else:
            handler = self.get('run/services/http')._handler

        print('...wsgi call handling', handler)

        if not environ:
            self.log.warning('BAD WSGI CTX')
            return None

        if not handler:
            self.log.warning('NO WSGI HANDLER')
            return None

        # handle error
        try:
            result = handler(environ, start_response)
        except Exception as err:
            import traceback
            traceback.print_exc()
            start_response('500 ERROR', [('Content-Type', 'text')])
            result = [str(traceback.format_exc())]
        print('...wsgi call stop')
        return result

    def service(self, name):
        service = self.get('services').get(name)
        return service

    def schedule(self, *args, **kwargs):

        scheduler = self.get('services/cron')

        if len(args) > 1:
            scheduler.schedule(*args, **kwargs)
        else:
            def _wrapper(func):
                c = args[0]
                return scheduler.schedule(c, func, *args[1:], **kwargs)
            return _wrapper

    def on(self, *args):

        if len(args) > 1:
            event, handler = args
            self._events.setdefault(event, [])
            self._events[event].append(handler)
        else:
            def _(handler):
                event = args[0]
                self._events.setdefault(event, [])
                self._events[event].append(handler)
            return _

    def emit(self, event, *args, **kwargs):
        for handler in self._events.get(event, []):
            try:
                spawn(handler)(*args, **kwargs)
            except Exception as err:
                log.warning('event handler error', err)
                import traceback
                traceback.print_exc()

    def publish(self, topic, *args, **kwargs):
        # to fix,  pb loopback with pubsubservice.publish
        # 1/ self.get('services/pubsub') must be in App
        # 2/ default/fallback handler for these methode must forward to self.server

        pubsubservice = self.get('services/pubsub').content  # why content and not handler ? + conflict res.publish and res.content.publish
        if pubsubservice:
            print('...app.publish', topic)
            return pubsubservice.publish(topic, *args, **kwargs)

    def subscribe(self, *args):

        if len(args) > 1:
            topic, callback = args
            return self.get('services/pubsub').subscribe(topic, callback)
        else:
            def _wrapper(callback):
                topic = args[0]
                return self.get('services/pubsub').subscribe(topic, callback)
            return _wrapper

    def main(self):

        import sys
        import os
        from pprint import pprint
        import os.path
        import xio

        import argparse

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('cmd', nargs='?', const=None, default=None)
        parser.add_argument('param', nargs='?', const=None, default=None)
        parser.add_argument('--http', type=int, nargs='?', const=8080, default=8080)
        parser.add_argument('--ws', type=int, nargs='?', const=8484, default=None)
        parser.add_argument('--debug', action='store_true')
        parser.add_argument('--network', action='store_true')
        parser.add_argument('--env', type=str, default=None)

        # add custom env
        for k, v in xio.env.items():
            try:
                parser.add_argument('--' + k, default=v)
            except:
                pass

        args = parser.parse_args()
        options = vars(parser.parse_args())
        for key, val in options.items():
            xio.env.set(key, val)

        # handler env file
        envfilepath = xio.env.get('env')
        if envfilepath and os.path.isfile(envfilepath):
            xio.env.load(envfilepath)
        print()
        print("\tapp=", self)
        print("\tapp=", self.id)
        print('\tapp=', self.name)
        print('\tapp=', self._about)
        print('\tnode=', xio.env.get('node'))
        for k, v in xio.env.items():
            print('\tenv', k, '.' * (40 - len(k)), v)
        print()

        if args.cmd == 'run':

            self.run(**options)

            import time
            while True:
                time.sleep(0.1)

        elif args.cmd == 'about':

            if not args.param:
                print('\n======= about /')
                pprint(self.about().content)
                print('\n======= about www')

                pprint(self.render('ABOUT').content)
            else:
                pprint(self.render('ABOUT', args.param).content)

        elif args.cmd == 'api':

            path = args.param or ''
            res = self.render('API', path)
            print(res)
            api = self.render('API', path).content
            assert api
            pprint(dict(api))
            for key, val in api.items():
                print(key, val.get('description'))

        elif args.cmd == 'get':

            path = param1 or ''

            h = getattr(self, method)
            res = h(path)
            print(type(res.content))
            print()
            print('_' * 30)
            print()
            print('\trequest:\t', method, repr(path or '/'))
            print('\tresponse:\t', res)
            print('\tresponse code:\t', res.status)
            print('\tresponse headers:\t')
            for k, v in list(res.headers.items()):
                print('\t\t', k, ':', v)
            print('\tresponse type:\t', res.content_type)
            print('\tcontent:\t', res.content)
            print()

            if isinstance(res.content, list) or isinstance(res.content, dict):
                pprint(res.content)
            else:
                print(str(res.content)[0:500])

            print()

        elif args.cmd:

            h = self.get('bin/%s' % args.cmd)
            pprint(h.content)
            """
            if h.content:
                print('=====> bin', args.cmd,  h.content ) #, args[2:])
                res = h(xio.request('POST', '', data={'args': args[2:]}))
                pprint(res)
            """

        else:
            self.debug()
