from starlette.responses import JSONResponse
from domain.exceptions import RepositoryError


async def repository_exception_handler(request, exc: RepositoryError):
    return JSONResponse(
        status_code=404,
        content=exc.to_dict(),
    )
