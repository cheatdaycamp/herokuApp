#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import environ as envimport bottle
from bottle import default_app, request, route, response, get
from sys import argv


DEBUG = os.environ.get("DEBUG")
bottle.debug(True)

@get('/')
def index():
    response.content_type = 'text/plain; charset=utf-8'
    ret =  'Hello world, I\'m process #%s!\n\n' % os.getpid()
    ret += 'Request vars:\n'
    for k, v in request.environ.items():
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    ret += '\n'
    ret += 'Environment vars:\n'

    for k, v in env.items():
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    return ret

if DEBUG:
	bottle.run(host='localhost', port=7000)
else:
	bottle.run(host='0.0.0.0', port=argv[1])
