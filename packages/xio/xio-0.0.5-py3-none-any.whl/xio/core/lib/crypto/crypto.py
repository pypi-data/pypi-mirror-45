#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .common import *

import sys
import hashlib
import base64
import uuid
import json
import time

from .naclHandler import NaclHandler

try:
    # warning => segmentation fault if this import is in Key.account() !!!!!
    from xio.core.network.ext.ethereum.account import Account as ethereum_handler
except:
    ethereum_handler = None


def key(*args, **kwargs):
    return Key(*args, **kwargs)

__HANDLERS__ = {
    'xio': NaclHandler,
    'ethereum': ethereum_handler
}


class Key:

    def __init__(self, priv=None, token=None, seed=None):

        handler_cls = NaclHandler

        self._accounts = {}

        if token:
            self._handler = handler_cls  # no instance, only static method allowed
            self.private = None
            self.public = None
            self.token = token
            self.tokendata = self.recoverToken(token)
            self.address = self.tokendata.get('body').get('sub')
            self.encryption = None
        else:
            self._handler = handler_cls(private=priv, seed=seed)
            self.private = self._handler.private
            self.public = self._handler.public
            self.address = self.public
            self.encryption = self._handler.encryption
            self.token = self.generateToken() if not token else token
            assert len(self.private) == 64

        # fix id & token => utf8
        self.address = to_string(self.address)
        self.token = to_string(self.token)

    def account(self, scheme=None):
        """ to fix scheme vs network ??"""

        scheme = scheme or 'xio'
        if '/' in scheme:
            base, scheme = scheme.split('/')
            assert base == 'xio'
        assert scheme in __HANDLERS__, Exception('unhandled crypto scheme %s' % scheme)
        if scheme == 'xio':
            return self
        elif not scheme in self._accounts:
            handler = __HANDLERS__.get(scheme)
            assert handler
            account = handler(seed=self.private)
            self._accounts[scheme] = account
        return self._accounts.get(scheme)

    def encrypt(self, message, *args, **kwargs):
        return self.encryption.encrypt(message, *args, **kwargs)

    def decrypt(self, message, *args, **kwargs):
        return self.encryption.decrypt(message, *args, **kwargs)

    def sign(self, message):
        return self._handler.sign(message)

    def verify(self, message, sig):
        return self._handler.verify(message, sig)

    def generateToken(self, scheme=None, body=None):
        scheme = scheme or 'xio'
        h = self.account(scheme)

        iat = int(time.time())
        exp = iat + 3600
        iss = self.address if not scheme else self.account(scheme).address
        body = body or {'sub': to_string(iss)}
        body.update({
            "iss": to_string(iss),
            "jti": to_string(uuid.uuid4()),
            "iat": iat,
            "exp": exp,
        })
        header = {
            "typ": "JWT",
            "alg": scheme
        }
        header = json.dumps(header)
        body = json.dumps(body, sort_keys=True)
        sig = h.sign(body)
        token = b'.'.join((
            base64.urlsafe_b64encode(header.encode()),
            base64.urlsafe_b64encode(body.encode()),
            base64.urlsafe_b64encode(sig.encode())
        ))

        return token

    def recoverToken(self, token, scheme=None):
        token = str_to_bytes(token)
        headerstr, bodystr, sig = [base64.urlsafe_b64decode(part) for part in token.split(b'.')]

        header = json.loads(headerstr)
        body = json.loads(bodystr)
        sig = sig.decode('utf-8')

        scheme = header.get('alg')
        assert scheme
        h = self._handler if not scheme else self.account(scheme)
        assert h

        # check recover feature
        if hasattr(h, 'recover'):
            recovered_id = h.recover(bodystr.decode('utf-8'), sig)
            assert recovered_id
            assert recovered_id == body.get('iss')
        else:
            assert h.verify(bodystr, sig)
        return {
            'header': header,
            'body': body,
            'sig': sig,
        }
