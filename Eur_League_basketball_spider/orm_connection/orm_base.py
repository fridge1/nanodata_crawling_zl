#重写orm方案
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
BaseModel = declarative_base()

class BaseModelExt(object):
    #创建引擎
    @classmethod
    def init_db(cls, engine):
        BaseModel.metadata.create_all(engine)
    BaseModel.init_db = init_db
    #删除引擎
    @classmethod
    def drop_db(cls, engine):
        BaseModel.metadata.drop_all(engine)
    BaseModel.drop_db = drop_db
    #查询是否有key
    @classmethod
    def get_by_key(cls, session, key, value, columns=None, lock_mode=None):
        if hasattr(cls, key):
            scalar = False
            if columns:
                if isinstance(columns, (tuple, list)):
                    query = session.query(*columns)
                else:
                    scalar = True
                    query = session.query(columns)
            else:
                query = session.query(cls)
            if lock_mode:
                query = query.with_lockmode(lock_mode)
            query = query.filter(getattr(cls, key) == value)
            if scalar:
                return query.scalar()
            return query.first()
        return None

    BaseModel.get_by_key = get_by_key

    @classmethod
    def get_all(cls, session, columns=None, offset=None, limit=None, order_by=None, lock_mode=None):
        if columns:
            if isinstance(columns, (tuple, list)):
                query = session.query(*columns)
            else:
                query = session.query(columns)
                if isinstance(columns, str):
                    query = query.select_from(cls)
        else:
            query = session.query(cls)
        if order_by is not None:
            if isinstance(order_by, (tuple, list)):
                query = query.order_by(*order_by)
            else:
                query = query.order_by(order_by)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        return query.all()

    BaseModel.get_all = get_all

    @classmethod
    def count_all(cls, session, lock_mode=None):
        query = session.query(func.count('*')).select_from(cls)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        return query.scalar()

    BaseModel.count_all = count_all

    @classmethod
    def exist(cls, session, _id, lock_mode=None):
        if hasattr(cls, 'id'):
            query = session.query(func.count('*')).select_from(cls).filter(cls.id == _id)
            if lock_mode:
                query = query.with_lockmode(lock_mode)
            return query.scalar() > 0
        return False

    BaseModel.exist = exist

    @classmethod
    def set_attr(cls, session, _id, attr, value):
        if hasattr(cls, 'id'):
            session.query(cls).filter(cls.id == _id).update({
                attr: value
            })
            session.commit()

    BaseModel.set_attr = set_attr

    @classmethod
    def set_attrs(cls, session, _id, attrs):
        if hasattr(cls, 'id'):
            session.query(cls).filter(cls.id == _id).update(attrs)
            session.commit()

    BaseModel.set_attrs = set_attrs

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    BaseModel.to_dict = to_dict

    @classmethod
    def upsert(cls, session, keys, default, extra_data=None, auto_commit=True):
        has_change = False
        if isinstance(keys, list):
            q = session.query(cls)
            for key in keys:
                q = q.filter(
                    getattr(cls, key) == default[key]
                )
            ins = q.first()
        else:
            ins = session.query(cls).filter(
                getattr(cls, keys) == default[keys]
            ).first()
        if not ins:
            ins = cls(**default)
            session.add(ins)
            has_change = True
        else:
            for k, v in default.items():
                if v != getattr(ins, k):
                    setattr(ins, k, v)
                    has_change = True
        if has_change:
            if extra_data:
                for k, v in extra_data.items():
                    setattr(ins, k, v)
        if auto_commit:
            session.commit()
        return has_change, ins

    BaseModel.upsert = upsert

    @classmethod
    def creat(cls, session, default):
        ins = cls(**default)
        session.add(ins)
        session.commit()
        return ins

    BaseModel.creat = creat

    @classmethod
    def inter(cls, session, key, per_page=1000):
        min_q = session.query(cls).order_by(
            getattr(cls, key).asc()
        ).first()

        max_q = session.query(cls).order_by(
            getattr(cls, key).desc()
        ).first()

        min_id = getattr(min_q, key)
        max_id = getattr(max_q, key)

        start_id = min_id
        while start_id <= max_id:
            for x in session.query(cls).filter(
                    getattr(cls, key).between(start_id, start_id + per_page)
            ):
                yield x
            start_id += per_page

    BaseModel.inter = inter

