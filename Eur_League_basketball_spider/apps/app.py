# -*- coding: utf-8 -*-
from apps.config import config
from orm_connection.orm_session import MysqlSvr
class AppCtx(object):
    ENV_LOCAL = 'local'
    ENV_DEVELOPMENT = 'development'
    ENV_PRODUCTION = 'production'
    ENV_DEFAULT = ENV_LOCAL

    env = ENV_DEVELOPMENT
    echo = False
    proxy = False
    @classmethod
    def set_env(cls, env):
        if env in [cls.ENV_DEVELOPMENT, cls.ENV_PRODUCTION, cls.ENV_LOCAL]:
            cls.env = env
        else:
            cls.env = cls.ENV_DEFAULT

    @classmethod
    def get_env(cls):
        return cls.env

    @classmethod
    def set_echo(cls, echo):
        cls.echo = echo
        MysqlSvr.set_echo(cls.echo)

    @classmethod
    def get_config(cls, key):
        return config.get(cls.env).get(key)
