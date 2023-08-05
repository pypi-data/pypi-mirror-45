#!/usr/bin/env python
# -*- coding: utf-8 -*--

import sys
import os
from pprint import pprint
import datetime
import yaml
import time
import traceback
import xio

from xio.core.utils import md5, mktime

from xio.core.lib.db import db


class Containers:

    def __init__(self, node, db=None):

        self.node = node

        # warning, services may be unavalable yet (required full app/init or app/start)

        self.docker = node.service('docker').content  # skip resource wrapper
        assert self.docker
        self.ipfs = node.service('ipfs')  # pb ipfs is under network.ipfs (not a os.service)
        db = db or xio.db()
        self.db = db.container('containers')  # , factory=Container => pb for Containers arg

    def get(self, index):
        container = Container(self, index, container=self.db)
        return container

    def register(self, uri):
        index = md5(uri)
        container = self.get(index)
        if not container._created:
            container.uri = uri
            container.state = 'pending'
            container.autodeliver = False
            container.save()

    def deliver(self, uri):

        index = md5(uri)
        container = self.get(index)
        if not container._created:
            xio.log.info('delivering container from', uri)
            container.uri = uri
            container.state = 'fetch'
            container.autodeliver = True
            container.save()

    # @xio.tools.cache(200)
    def resync(self):
        """ update containers states from current dockers running containers"""
        # sync docker containers

        # get containers to provide
        containers_to_provide = self.node.getContainersToProvide()
        for row in containers_to_provide:
            self.deliver(row)

        # update all containers
        for row in self.db.select():
            if row['uri'] not in containers_to_provide:
                self.db.delete(row['_id'])

        running_endpoints = {}
        for container in self.docker.containers():
            name = container.name
            # find port 8080
            for k, v in container.ports.items():
                if v == 80:
                    # look like deliverable container
                    http_endpoint = 'http://127.0.0.1:%s' % k

                    running_endpoints[name] = {
                        'endpoint': http_endpoint
                    }

                    try:
                        self.node.register(http_endpoint)
                    except Exception as err:
                        #import traceback
                        # traceback.print_exc()
                        print('dockersync error', err)

        return running_endpoints

    def sync(self):

        # resync from currents running docker containers
        self.resync()

        # sync deliverable containers
        for row in self.db.select():
            container = self.get(row['_id'])

            if container.autodeliver:
                try:
                    container.sync()
                except Exception as err:
                    self.node.log.error('container.sync error', err)

    def select(self):
        return self.db.select()

    def images(self):
        return self.docker.images('xio')


from functools import wraps


def workflowOperation(func):

    @wraps(func)
    def _(self, *args, **kwargs):
        res = None
        opname = func.__name__
        state = self.state
        if state != opname:
            xio.log.warning('wrong state', opname, state)
            return
        workflow = self.workflow
        if not workflow:
            self.workflow = {}
        self.workflow.setdefault(opname, {})
        opstate = self.workflow.get(opname)
        if not opstate:
            opstate['started'] = int(time.time())
            opstate['status'] = 'RUNNING'
            self.save()
            try:
                xio.log.info('workflowOperation', opname, 'start')
                res = func(self, *args, **kwargs)
                opstate['status'] = 'SUCCEED'
            except Exception as err:
                xio.log.error('workflowOperation', opname, 'FAILED', err)
                opstate['status'] = 'FAILED'
                opstate['error'] = err

            self.save()
            return res
        else:
            xio.log.warning('workflowOperation', opname, 'already running')

    return _


class Container(db.Item):

    def __init__(self, containers, *args, **kwargs):

        self._containers = containers
        self._docker = containers.docker  # skip resource wrapper
        self._log = self._containers.node.log

        db.Item.__init__(self, *args, **kwargs)

    def about(self):
        about = self.data
        about.update({
            'image': self.image.about() if self.image else {'name': self.iname},
            'container': self.container.about() if self.container else {'name': self.cname},
        })
        return about

    def sync(self):

        self._log.info('sync', self.uri)

        if self.state != 'running':

            self.fetch()
            self.build()
            self.run()

        else:

            dockercontainer = self._docker.container(name=self.cname)
            running = dockercontainer.running if dockercontainer else False

            if running:
                try:
                    self._containers.node.register(self.endpoint)
                except Exception as err:
                    xio.log.error('unable to register containers endpoint ', self.endpoint, err)

            else:
                xio.log.warning('container not running, try to restart it ', self.iname)
                try:
                    self._containers.node.unregister(self.endpoint)
                except Exception as err:
                    xio.log.error('unable to unregister containers endpoint', self.endpoint, err)

                self.state = 'run'
                if self.workflow and 'run' in self.workflow:
                    del self.workflow['run']
                self.save()

    @workflowOperation
    def fetch(self):

        if self.uri.startswith('/'):
            self.directory = self.uri

        about_filepath = self.directory + '/about.yml'
        with open(about_filepath) as f:
            about = yaml.load(f)

        self.name = about.get('name')
        nfo = self.name.split(':')
        nfo.pop(0)  # strip xrn:

        self.cname = '-'.join(nfo)

        dockerinfo = about.get('docker', {})

        # set image
        dockerfile = self.directory + '/Dockerfile'
        if not os.path.isfile(dockerfile):
            # if no dockerfile, could be local app (no docker container needed ?)
            self.iname = dockerinfo.get('image', 'inxio/app')
            self.dockerfile = None
        else:
            self.iname = self.cname.replace('-', '/')
            self.dockerfile = dockerfile

        self.state = 'build'

    @workflowOperation
    def build(self):

        dockercontainer = self._docker.container(name=self.cname)
        if dockercontainer:
            dockercontainer.stop()
            dockercontainer.remove()

        if self.dockerfile:

            dockerimage = self._docker.image(name=self.iname)
            """
            created = dockerimage._about['created']
            created = mktime(created)

            """

            if not dockerimage and self.dockerfile:
                self._docker.build(name=self.iname, directory=self.directory)  # ,dockerfile=self.dockerfile
                self._dockerimage = self._docker.image(name=self.iname)
                assert self._dockerimage

        self.state = 'run'

    @workflowOperation
    def run(self):

        dockercontainer = self._docker.container(name=self.cname)
        cport = 80

        if not dockercontainer:

            assert self.cname
            assert self.iname
            assert self.directory

            container_volume = '/data/%s' % self.cname

            info = {
                'name': self.cname,
                'image': self.iname,
                'ports': {
                    cport: ('127.0.0.1', 0),
                },
                'volumes': {
                    '/apps/xio': '/apps/xio',
                    self.directory: '/apps/app',
                    container_volume: '/data'
                }
            }
            dockercontainer = self._docker.run(**info)
            assert dockercontainer

        else:
            if not dockercontainer.running:
                dockercontainer.start()

        portmapping = dockercontainer.about().get('port')  # receive {32776: 8080}
        for k, v in portmapping.items():
            if v == cport:
                self.endpoint = 'http://127.0.0.1:%s' % k
                self.port = k

        assert self.endpoint

        self.state = 'running'

    def test(self):
        dockercontainer = self._docker.container(self.cname)
        return dockercontainer.execute('python -m unittest app/tests.py')

    def logs(self):
        dockercontainer = self._docker.container(self.cname)
        return dockercontainer.logs()

    def request(self, method, path, query):
        """ test for ihm admin only ?"""
        if self.endpoint:
            import xio
            cli = xio.client(self.endpoint)
            resp = cli.request(method, path, {})

            return resp.content  # tofix: tronqué si return direct
