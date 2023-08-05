#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import xio
import sys
from pprint import pprint

user = xio.user()

class TestCases(unittest.TestCase):

    def test_method(self):
        req = xio.request('POST', '/')
        assert req.POST
        assert not req.GET
        assert req.data == {}
        assert req.method=='POST'

    def test_xmethod(self):
        req = xio.request('CUSTOMEMETHOD', '/')
        assert req.method=='POST'
        assert req.xmethod=='CUSTOMEMETHOD'
        assert req.CUSTOMEMETHOD
        assert req.POST
        assert not req.GET

    def test_headers(self):
        req = xio.request('POST', '/', headers={'SomeHeader': '123'})
        assert req.headers.get('SomeHeader')=='123'

    def test_auth(self):
        req = xio.request('POST', '/', headers={'Authorization': 'Bearer %s' % user.key.token})
        assert req.client
        assert req.client.id == user.id
        pprint(req._debug())

    def test_require(self):
        req = xio.request('POST', '/')
        try:
            req.require('scope','123')
            raise Exception('fail')
        except:
            pass


if __name__ == '__main__':

    unittest.main()
