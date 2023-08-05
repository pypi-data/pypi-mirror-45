#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import OrderedDict
import uuid
import sys
import hashlib
import binascii
from functools import wraps
import os
import pwd
import time
import os.path

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from .data.data import jsonld, jsonldlist

if sys.version_info.major == 2:

    import codecs

    def str_to_bytes(value):
        if isinstance(value, (bytes, bytearray)):
            return value
        else:
            return bytes(value)

    def decode_hex(s):
        if isinstance(s, bytearray):
            s = str(s)
        if not isinstance(s, (str, unicode)):
            raise TypeError('require str or unicode')
        return s.decode('hex')

    def encode_hex(s):
        if isinstance(s, bytearray):
            s = str(s)
        if not isinstance(s, (str, unicode)):
            raise TypeError('require instance of str or unicode')
        return s.encode('hex')

else:

    def str_to_bytes(value):
        if isinstance(value, bytearray):
            value = bytes(value)
        if isinstance(value, bytes):
            return value
        return bytes(value, 'utf-8')

    def decode_hex(s):
        if isinstance(s, str):
            return bytes.fromhex(s)
        if isinstance(s, (bytes, bytearray)):
            return binascii.unhexlify(s)
        raise TypeError('require instance of str or bytes')

    def encode_hex(b):
        if isinstance(b, str):
            b = bytes(b, 'utf-8')
        if isinstance(b, (bytes, bytearray)):
            return str(binascii.hexlify(b), 'utf-8')
        raise TypeError('require instance of str or bytes')


def to_string(value):
    if value != None:
        if isinstance(value, (bytes, bytearray)):
            value = value.decode()
        else:
            value = str(value)
    else:
        value = ''
    return value


def to_bytes(value):
    return str_to_bytes(value)


def is_int(i):
    try:
        assert not is_string(i)
        i = int(i)
        return True
    except:
        return False


def is_string(s):
    try:
        return isinstance(s, basestring)
    except NameError:
        return isinstance(s, str)


def generateuid():
    return uuid.uuid4().hex


def mktime(dt):

    try:
        from dateutil.parser import parse
        dt = parse(dt)
    except:
        import datetime
        dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    return int(time.mktime(dt.timetuple()))


def md5(*args):
    assert args
    parts = [to_string(txt) for txt in args]
    txt = ''.join(parts)
    return hashlib.md5(to_bytes(txt)).hexdigest()


def sha1(*args):
    assert args
    parts = [to_string(txt) for txt in args]
    txt = ''.join(parts)
    return hashlib.sha1(to_bytes(txt)).hexdigest()


def coroutine(func):

    def _(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return _


def spawn(func):
    """
    defer function using global handler (gevent, asyncio, ...)
    """

    import gevent

    @wraps(func)
    def _(*args, **kwargs):
        return gevent.spawn(func, *args, **kwargs)

    return _


def thread(func):

    from threading import Thread

    @wraps(func)
    def _(*args, **kwargs):
        t = Thread(target=func, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        return t

    return _


def process(func):

    from multiprocessing import Process

    @wraps(func)
    def _(*args, **kwargs):
        p = Process(target=func, args=args, kwargs=kwargs)
        p.start()
        return p

    return _
