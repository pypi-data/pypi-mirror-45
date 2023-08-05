#!/usr/bin/env python
# -*- coding: utf-8 -*--
import xio
from xio.core import resource
from xio.core.resource import handleRequest

from xio.core.request import Request, Response

from xio.core.app.app import App
from xio.core.lib.logs import log
from xio.core.lib.utils import is_string, urlparse, generateuid

from .containers import Containers

import traceback
from pprint import pprint
import datetime
import os.path
import hashlib
import base64
import uuid

import time
import json

import sys
import collections


def node(*args, **kwargs):
    return Node.factory(*args, **kwargs)


class Node(App):

    def __init__(self, name=None, network=None, **kwargs):

        App.__init__(self, name, **kwargs)

        self.uid = generateuid()

        # to fix ... need to handle node connected to 0x... network or http:/// network
        self.network = self.connect(network) if network else None

        if self.network:
            try:
                self._about['network'] = self.network.about()
            except Exception as err:
                self.log.warning('self.network error', err)

        self.bind('www', self.renderWww)

        # service memdb
        import xio
        if self.redis:
            memdb = xio.db(name='xio', type='redis')
        else:
            memdb = xio.db()

        self.put('services/db', memdb)

        # fix peers (default python handler)
        from xio.core.peers import Peers
        self.peers = Peers(peer=self, db=memdb)

        # node sync
        node_heartbeat = xio.env.get('node_heartbeat', 300)
        self.schedule(node_heartbeat, self.sync)

        # containers sync
        node_peers_heartbeat = xio.env.get('node_peers_heartbeat', 300)
        self.schedule(node_peers_heartbeat, self.peers.sync)

        # init docker and container (require loaded services)
        try:
            from .ext.docker.service import DockerService
            self.put('services/docker', DockerService(self))
            self.containers = Containers(self, db=memdb)
            node_containers_heartbeat = xio.env.get('node_containers_heartbeat', 300)
            self.schedule(node_containers_heartbeat, self.containers.sync)
        except Exception as err:
            self.log.warning('self.docker error', err)

    def register(self, endpoints):

        if not isinstance(endpoints, list):
            endpoints = [endpoints]

        for endpoint in endpoints:
            return self.peers.register(endpoint)

    def getContainersToProvide(self):
        # fetch container to provide
        try:
            res = self.network.get('containers')
            return res.content or []
        except Exception as err:
            xio.log.error('unable to fetch containers to provide', err)

    def sync(self):
        self.containers.sync()

    def renderWww(self, req):
        """
        options: ABOUT,GET
        """

        self.log.info('NODE.RENDER', req)
        self.log.info(req.headers)

        # handle request which not require auth
        if not req.path and req.OPTIONS:
            return ''

        if not req.path and req.ABOUT:
            about = self._handleAbout(req)
            about['id'] = self.id  # fix id missing
            if self.network:
                about['network'] = self.network.about().content
            if req.client.peer:
                about['user'] = {'id': req.client.peer.id}
            return about

        # NODE DELIVERY
        if not req.path:

            if req.GET:

                # node peers
                peers = [peer.about().content for peer in self.peers.select()]
                return peers

            elif req.CHECK:
                req.require('scope', 'admin')
                return self._handleCheck(req)
            elif req.REGISTER:
                endpoint = req.data.get('endpoint', req.context.get('REMOTE_ADDR').split(':').pop())  # '::ffff:127.0.0.1'
                if not '://' in endpoint:
                    endpoint = 'http://%s' % endpoint
                return self.peers.register(endpoint)
            elif req.CHECKALL:
                return self.checkall()
            elif req.SYNC:
                return self.peers.sync()
            elif req.CLEAR:
                return self.peers.clear()
            elif req.EXPORT:
                return self.peers.export()

             # method not allowed
            raise Exception(405, 'METHOD NOT ALLOWED')

        assert req.path

        p = req.path.split('/')
        peerid = p.pop(0)
        assert peerid

        # forward /user to network
        if peerid == 'user':
            return self.network.request(req)

        log.info('==== DELIVERY REQUEST =====', req.method, req.xmethod)
        log.info('==== DELIVERY FROM =====', req.client.id, req.client.peer)
        log.info('==== DELIVERY TO   =====', peerid)

        peer = self.peers.get(peerid)

        assert peer, Exception(404)

        try:
            req.path = '/'.join(p)
            resp = peer.request(req)

            req.response.status = resp.status
            req.response.headers = resp.headers  # pb si header transferé tel quel ->
            req.response.content_type = resp.content_type
            req.response.ttl = resp.ttl
            return resp.content
        except Exception as err:
            traceback.print_exc()
            req.response.status = 500
            return None
