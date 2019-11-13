import sys


def parse_options():
    options = dict()

    op = ''
    for val in sys.argv[1:]:
        if val[0:2] == '--':
            op = val[2:]
        elif val[0:1] == '-':
            op = val[1:]
        else:
            if not op:
                continue
            options[op] = val
    return options


import asyncio
import time

from nats.aio.client import Client
from stan.aio.client import Client as STAN


class BaseSvr(object):
    env = 'development'

    @classmethod
    def set_env(cls, env):
        cls.env = env

class NatsSvr(BaseSvr):
    env = 'development'

    instances = {}
    stan_instances = {}
    configs = {
        'local'      : {
            'nats'    : {
                'servers' : ["nats://nats.namincs.com:4222"],
                'user'    : 'nana',
                'password': 'aa123456',
            },
            'hub.nats': {
                'servers' : ["nats://hub.nats.namincs.com:4222"],
                'user'    : 'nana',
                'password': 'aa123456',
            },
        },
        'development': {'nats': {
            'servers' : ["nats://nats.namincs.com:4222"],
            'user'    : 'nana',
            'password': 'aa123456',
        },
            'hub.nats'        : {
                'servers' : ["nats://hub.nats.namincs.com:4222"],
                'user'    : 'nana',
                'password': 'aa123456',
            }, 'local'        : {
                'host'    : '127.0.0.1',
                'port'    : 6379,
                'password': '',
                'db'      : 0
            },
        },
        'production' : {
            'nats'    : {
                'servers' : ["nats://nats.namincs.com:4222"],
                'user'    : 'nana',
                'password': 'aa123456',
            },
            'hub.nats': {
                'servers' : ["nats://hub.nats.namincs.com:4222"],
                'user'    : 'nana',
                'password': 'aa123456',
            },
        }
    }

    @classmethod
    def set_env(cls, env):
        cls.env = env

    @classmethod
    async def get(cls, name='nats', loop=None):
        instance = cls.instances.get(name)
        if instance is None:
            config = cls.configs[cls.env][name]
            client = Client()
            await client.connect(
                io_loop=loop or asyncio.get_event_loop(),
                servers=config['servers'],
                user=config['user'],
                password=config['password']
            )
            cls.instances[name] = instance = client
        return instance

    @classmethod
    async def get_stan(cls, name='nats', cluster_id='cluster', client_id='', loop=None):
        key = '%s_%s_%s' % (name, cluster_id, client_id)
        instance = cls.stan_instances.get(key)
        if instance is None:
            instance = STAN()
            if not client_id:
                client_id = "%s_%s" % (cls.env, int(time.time()*1000))
            nc = await cls.get(name=name, loop=loop)
            await instance.connect(cluster_id=cluster_id, client_id=client_id, nats=nc)

            cls.stan_instances[key] = instance

        return instance