#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests

try:
    import ipfsApi
except:
    import ipfsapi as ipfsApi

IPFS_HOST = '127.0.0.1'
#IPFS_HOST = 'https://ipfs.infura.io'
IPFS_PORT = 5001
IPFS_LOCAL_GATEWAY_PORT = 9001

IPFS_GATEWAYS = [
    'https://ipfs.io/ipfs/',
    'https://ipfs.infura.io/',
]


def _toStr(b):
    return b.decode() if isinstance(b, bytes) else str(b)


class Handler:

    def __init__(self, path, **kwargs):
        self.basepath = path

    def __call__(self, req):

        url = 'https://ipfs.io/ipfs/' + self.basepath + '/' + req.path

        r = requests.get(url, timeout=10, verify=False)
        status = r.status_code
        content = r.content if not r.encoding else r.text

        req.response.status = status
        req.response.headers = r.headers
        content_type = req.response.headers.get('Content-Type')
        if content_type == 'application/json' and is_string(content):
            content = json.loads(content)

        return content


class Connector:

    def __init__(self, endpoint=None):
        if endpoint == 'local':
            host = '127.0.0.1'
            port = IPFS_PORT
            IPFS_GATEWAYS.insert(0, 'http://%s:%s/ipfs/' % (host, IPFS_LOCAL_GATEWAY_PORT))
        elif endpoint == 'infura':
            host = 'https://ipfs.infura.io'
            port = IPFS_PORT
        elif endpoint:
            info = endpoint.split(':')
            host = info.pop(0)
            port = int(info.pop(0)) if info else IPFS_PORT
            IPFS_GATEWAYS.insert(0, 'http://%s:%s/ipfs/' % (IPFS_HOST, IPFS_LOCAL_GATEWAY_PORT))
        else:
            host = IPFS_HOST
            port = IPFS_PORT
            IPFS_GATEWAYS.insert(0, 'http://%s:%s/ipfs/' % (IPFS_HOST, IPFS_LOCAL_GATEWAY_PORT))

        self.host = host
        self.port = port
        self.conn = ipfsApi.Client(self.host, self.port)

    def about(self):
        return {
            'conn': self.conn,
            'endpoint': (self.host, self.port),
            'gateways': IPFS_GATEWAYS
        }

    def handler(self, uri):
        return Handler(uri)

    def account(self, *args, **kwargs):
        return Account(self, *args, **kwargs)

    def pin(self, hash):
        return self.conn.pin_add(hash)

    def pin_ls(self):
        return self.conn.pin_ls()

    def pin_rm(self, hash):
        return self.conn.pin_rm(hash)

    def cat(self, hash=None):
        # bug ipfsapi which unable to handle timeout
        print('...ipfs cat', hash)

        res = self.conn.cat(hash)
        return res

    def get(self, ipfshash, timeout=20):
        ipfshash = _toStr(ipfshash)
        for gateway in IPFS_GATEWAYS:
            url = '%s/%s' % (gateway, ipfshash)
            try:
                print('...ipfs get', url)
                r = requests.get(url, timeout=timeout, verify=False)
                status = r.status_code
                content = r.content if not r.encoding else r.text
                return content
            except Exception as err:
                print('...ipfs get ... ERROR', err)

    def broadcast(self, ipfshash):
        ipfshash = _toStr(ipfshash)
        for gateway in IPFS_GATEWAYS:
            url = '%s/%s' % (gateway, ipfshash)
            try:
                print('ipfs call', url)
                r = requests.get(url, timeout=5, verify=False)
                print('ipfs broadcast ok', gateway)
            except Exception as err:
                print('ipfs broadcast failed', gateway)

    def add(self, data=None, filepath=None):
        """
        bug ipfsapi si filepath est un chemin complet
        """
        if filepath:
            with open(filepath) as f:
                result = self.conn.add(filepath)  # attention ipfsApi buggué
        else:
            import os
            import uuid

            #import tempfile
            #f = tempfile.NamedTemporaryFile()
            tmpfilename = str(uuid.uuid4())
            try:
                f = open(tmpfilename, 'w')
                f.write(data)
                f.close()  # attention le fichier doit etre fermé avant de le passer a ipfs
                result = self.conn.add(tmpfilename)  # attention ipfsApi buggué
            except Exception as err:
                result = None
            os.remove(tmpfilename)
        return result.get('Hash') if result else None
