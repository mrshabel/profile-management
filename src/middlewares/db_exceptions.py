from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.logger import logger


async def db_exceptions_handler(request: Request, call_next):
    """An error handling middleware for all database exceptions"""
    try:
        return await call_next(request)
    except Exception as e:
        if isinstance(e, ForeignKeyViolationError):
            err, status = str(e).split("\n")[1], 400
        elif isinstance(e, UniqueViolationError):
            err, status = str(e).split("\n")[1], 409
        else:
            err, status = "Something went wrong", 500

        logger.error(msg=e)
        return JSONResponse(content=err, status_code=status)


# def sanitize_foreign_key_error_message(e: ForeignKeyViolationError):
#     msg: str = ""
#     e.DETAIL
