import functools

from fastapi import HTTPException
from sqlalchemy import exc


def no_result_found_handler():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args):
            try:
                return await func(*args)
            except exc.NoResultFound:
                raise HTTPException(status_code=404, detail="No such element!")

        return wrapped

    return wrapper


def async_value_error_handler():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))

        return wrapped

    return wrapper


def sync_value_error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    return wrapper
