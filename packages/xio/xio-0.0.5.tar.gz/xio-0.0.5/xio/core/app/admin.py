#!/usr/bin/env python
# -*- coding: utf-8 -*--

from xio.core.utils import spawn


def enhance(app):

    @app.bind('www/xio/admin/bin')
    def _(req):
        for cmd, res in app.get('bin')._children.items():
            yield {
                'name': cmd,
                'about': res._about
            }

    @app.bind('www/xio/admin/bin/:cmd')
    # @spawn
    def _(req):
        # http://toastdriven.com/blog/2011/jul/31/gevent-long-polling-you/
        cmd = req.context.get(':cmd')
        handler = app.get('bin').get(cmd)
        return handler.request(req).content

    @app.bind('www/xio/admin/about')
    def _(req):
        return app._about

    @app.bind('www/xio/admin/info')
    def _(req):
        import xio
        from threading import current_thread

        key = req.query.get('key')
        if key:
            return key

        result = {
            'req': req._debug(),
        }
        # check env
        import os
        envos = dict()
        for k, v in os.environ.items():
            envos[k] = v

        result['env'] = {
            'thread': current_thread(),
            'os': envos,
            'xio': xio.context,
            'req.context': req.context
        }

        # check redis
        result['redis'] = app.redis
        return result

    @app.bind('www/xio/admin/services')
    def _(req):
        import copy
        services = copy.deepcopy(app._about.get('services', {}))
        for conf in services:
            name = conf.get('name')
            conf.update({
                'client': app.get('services').get(name)
            })

        return services

    @app.bind('www/xio/admin/services/:name')
    def _(req):
        name = req.context.get(':name')
        service = app.get('services').get(name)
        return service.request(req)

    @app.bind('www/xio/admin/peers')
    def _(req):
        for peer in app.peers.select():
            row = peer.data
            row['@id'] = peer.uid
            yield row

    @app.bind('www/xio/admin/peers/:id')
    def _(req):
        """
        options: "*"
        """

        print('===============', req)
        peerid = req.context.get(':id')
        peer = app.peers.get(peerid)

        assert peer
        print(peer)
        method = req.xmethod or req.method
        return peer.request(method, req.path, req.input)

    @app.bind('www/xio/admin/redis')
    def _(req):

        r = app.redis

        if req.CLEAR:
            for key in r.keys('*'):
                r.delete(key)
            yield 'cleared'

        for key in r.keys():
            row = {
                '@id': key
            }
            yield row

    @app.bind('www/xio/admin/stats')
    def _(req):
        service = app.service('stats')
        return service.select()

    @app.bind('www/xio/admin/logs')
    def _(req):
        import xio
        return xio.log.show()
