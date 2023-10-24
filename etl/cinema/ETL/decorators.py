from functools import wraps
from contextlib import contextmanager
from db.config import engine
from sqlalchemy.orm import sessionmaker
import logging as logger
import time


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=20):
    """
    if something is wrong it relaunch the functions
    """
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            current_sleep_time = start_sleep_time
            while True:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    logger.info(f"Error: {str(e)}. Retrying in {current_sleep_time} seconds.")
                    time.sleep(current_sleep_time)
                    current_sleep_time = min(current_sleep_time * factor, border_sleep_time)
        return inner
    return func_wrapper


def coroutine(func):
    """
    this decorator allows to next 
    coroutine in the generator functions
    """
    @wraps(func)
    def inner(*args, **kwargs):
        fn = func(*args, **kwargs)
        next(fn)
        return fn
    return inner


@contextmanager
def session_scope():
    SessionLocal = sessionmaker(engine, expire_on_commit=False, autoflush=True)
    """
    begin session for database access.
    and yield it
    """
    with SessionLocal.begin() as session:
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise


def create_session(func):
    """
    Create session for database access.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        with session_scope() as session:
            kwargs["session"] = session
        result = func(*args, **kwargs)
        return result
    return inner
