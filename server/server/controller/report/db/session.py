# -*- coding:UTF-8 -*-
# @Time : 2024/3/6 12:01
# @Author : 寻梦
# @File : session
# @Project : langchain-ChatBA
from functools import wraps
from contextlib import contextmanager
from server.controller.report.db.base import Qiye_SessionLocal
from sqlalchemy.orm import Session

'''
回滚配置
'''

@contextmanager
def session_scope() -> Session:
    """上下文管理器用于自动获取 Session, 避免错误"""
    session = Qiye_SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def with_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with session_scope() as session:
            try:
                result = f(session, *args, **kwargs)
                session.commit()
                return result
            except:
                session.rollback()
                raise

    return wrapper


def get_db() -> Qiye_SessionLocal:
    db = Qiye_SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db0() -> Qiye_SessionLocal:
    db = Qiye_SessionLocal()
    return db
