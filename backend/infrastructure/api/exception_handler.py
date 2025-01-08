from http.client import HTTPException
from fastapi import HTTPException, status
from starlette.responses import JSONResponse
from domain.exceptions import RepositoryError


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