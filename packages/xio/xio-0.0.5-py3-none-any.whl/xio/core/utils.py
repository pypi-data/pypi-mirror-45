#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from functools import wraps

from .lib.crypto.common import (
    sha256,
    sha3_keccak_256
)

from .lib.utils import (
    urlparse,
    jsonld,
    jsonldlist,
    str_to_bytes,
    decode_hex,
    encode_hex,
    to_string,
    to_bytes,
    is_int,
    is_string,
    generateuid,
    mktime,
    md5,
    sha1,
    coroutine,
    spawn,
    thread,
    process
)


def require(condition, message):
    if not condition:
        try:
            code = int(message)
            message = None
        except:
            code = 500
            message = message
        raise Exception(code)


def about(src):
    from xio.core.resource import extractAbout
    return extractAbout(src)


def cache(ttl=0):

    def _cache(func):

        if not hasattr(func, '_xio_cache'):
            func._xio_cache = dict()

        @wraps(func)
        def _(*args, **kwargs):
            now = int(time.time())
            cacheuid = str((args, kwargs))
            cached = func._xio_cache.get(cacheuid)
            if cached:
                result = cached.get('result')
                created = cached.get('created')
                if (now - created < ttl):
                    return result

            result = func(*args, **kwargs)
            func._xio_cache[cacheuid] = {
                'created': now,
                'result': result
            }
            return result
        return _

    return _cache
