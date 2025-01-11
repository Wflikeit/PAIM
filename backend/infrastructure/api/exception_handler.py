from fastapi import HTTPException, status
from starlette.responses import JSONResponse
from domain.exceptions import RepositoryError, BusinessLogicError


async def repository_exception_handler(request, exc: RepositoryError):
    return JSONResponse(
        status_code=404,
        content=exc.to_dict(),
    )


def create_credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def business_logic_exception_handler(request, exc: BusinessLogicError):
    return JSONResponse(
        status_code=409,
        content=exc.to_dict(),
    )
