from sqlalchemy import create_engine
from sqlalchemy.orm import query, Session, scoped_session, sessionmaker

from orm_connection.base_svr import BaseSvr

#从orm目录下导入需要的模型py
from orm_connection.eur_basketball import *

class SafeQuery(query.Query):
    def __init__(self, entities, session=None):
        super().__init__(entities, session)

    def first(self):
        try:
            return super().first()
        except Exception:
            self.session.rollback()
            raise

    def filter(self, *criterion):
        try:
            return super().filter(*criterion)
        except Exception:
            self.session.rollback()
            raise

    def filter_by(self, **kwargs):
        try:
            return super().filter_by(**kwargs)
        except Exception:
            self.session.rollback()
            raise

    def order_by(self, *criterion):
        try:
            return super().order_by(*criterion)
        except Exception:
            self.session.rollback()
            raise

    def one(self):
        try:
            return super().one()
        except Exception:
            self.session.rollback()
            raise

    def all(self):
        try:
            return super().all()
        except Exception:
            self.session.rollback()
            raise

    def limit(self, limit):
        try:
            return super().limit(limit)
        except Exception:
            self.session.rollback()
            raise

    def count(self):
        try:
            return super().count()
        except Exception:
            self.session.rollback()
            raise

    def delete(self, synchronize_session='evaluate'):
        try:
            return super().limit(synchronize_session)
        except Exception:
            self.session.rollback()
            raise

    def exists(self):
        try:
            return super().exists()
        except Exception:
            self.session.rollback()
            raise

    def join(self, *props, **kwargs):
        try:
            return super().join(*props, **kwargs)
        except Exception:
            self.session.rollback()
            raise

    def outerjoin(self, *props, **kwargs):
        try:
            return super().outerjoin(*props, **kwargs)
        except Exception:
            self.session.rollback()
            raise

    def union(self, *q):
        try:
            return super().union(*q)
        except Exception:
            self.session.rollback()
            raise

    def __iter__(self):
        try:
            return super().__iter__()
        except Exception:
            self.session.rollback()
            raise


class SafeSession(Session):
    def __init__(self, bind=None, autoflush=True, expire_on_commit=True,
                 _enable_transaction_accounting=True,
                 autocommit=False, twophase=False,
                 weak_identity_map=True, binds=None, extension=None,
                 info=None,
                 query_cls=SafeQuery):
        super().__init__(
            bind=bind,
            autoflush=autoflush,
            expire_on_commit=expire_on_commit,
            _enable_transaction_accounting=_enable_transaction_accounting,
            autocommit=autocommit, twophase=twophase,
            weak_identity_map=weak_identity_map, binds=binds, extension=extension,
            info=info,
            query_cls=query_cls
        )

    def query(self, *entities, **kwargs):
        try:
            return super().query(*entities, **kwargs)
        except Exception:
            self.rollback()
            raise

    def commit(self):
        try:
            return super().commit()
        except Exception:
            self.rollback()
            raise


class MysqlSvr(BaseSvr):
    echo = False
    env = 'development'

    instances = {}
    engines = {}
    #连接地址处理
    configs = {
        'local'      : {
            'local'    : 'mysql+pymysql://root:720718zl@127.0.0.1/nana?charset=utf8mb4&autocommit=true',
            # 'spx_sites': 'mysql+pymysql://root:root@127.0.0.1/leisu_dev?charset=utf8&autocommit=true',
        },
        #公网
        'development': {
            'spider_zl': 'mysql+pymysql://spider_zl:0EDbIRtu4JPGdiQnu3kvXxiOMDMjejow@rm-bp1ov656aj80p2ie8uo.mysql.rds.aliyuncs.com/spider_zl?charset=utf8mb4&autocommit=true',
        },
        #内网
        'production': {
            'spider_yx': 'mysql+pymysql://spider_yx:xfAS5W6fwc6F0IZp@rm-bp1ov656aj80p2ie8.mysql.rds.aliyuncs.com/spider_yx?charset=utf8mb4&autocommit=true',
        },

    }

    @classmethod
    def set_echo(cls, echo):
        cls.echo = echo

    @classmethod
    def set_env(cls, env):
        cls.env = env

    @classmethod
    def get_engine(cls, name):
        instance = cls.engines.get(name)
        if instance is None:
            config = cls.configs[cls.env][name]
            cls.engines[name] = instance = create_engine(config, echo=cls.echo)
        return instance

    @classmethod
    def get(cls, name):
        instance = cls.instances.get(name)
        if instance is None:
            cls.instances[name] = instance = scoped_session(
                sessionmaker(
                    bind=cls.get_engine(name),
                    class_=SafeSession
                )
            )
        return instance()


if __name__ == '__main__':
    #设置服务器为目标,连接服务器引擎
    MysqlSvr.set_env('development')
    BaseModelExt.init_db(MysqlSvr.get_engine('spider_zl'))
    # 设置环境为本地,连接本地引擎
    # MysqlSvr.set_env('local')
    # BaseModelExt.init_db(MysqlSvr.get_engine('local'))