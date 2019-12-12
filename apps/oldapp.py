from spx_msg.svr.mysql_svr import MysqlSvr
import os
import time

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
