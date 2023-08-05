#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xio.core.app.app import App
from xio.core.peers import Peers
from xio.core.lib.utils import is_string, urlparse
from xio.core.lib.logs import log


def network(*args, **kwargs):
    return Network.factory(*args, **kwargs)


class Network(App):

    peers = None

    def __init__(self, id=None, **kwargs):

        App.__init__(self, **kwargs)
        self.peers = Peers()
        self.network = self
        self.log = log

