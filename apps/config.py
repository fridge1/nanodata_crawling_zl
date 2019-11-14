# -*- coding: utf-8 -*-
# import logging.config
import redis

config = {
    'local'      : {
        'zeromq': {
            'host'    : '',

        },
    },
    'development': {
        'zeromq': {
            'host'    : '',
            'port'    : 0,
            'username': b'',
            'password': b'',
        },
    },
    'production' : {
        'zeromq': {
            'host'    : '',
            'port'    : 0,
            'username': b'',
            'password': b'',
        },
    },
}