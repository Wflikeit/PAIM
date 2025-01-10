import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from application.auth.auth import AuthService
from domain.exceptions import RepositoryError
from infrastructure.api.endpoints.admin_router import router as admin_router
from infrastructure.api.endpoints.auth_router import router as auth_router
from infrastructure.api.endpoints.client_router import router as client_router
from infrastructure.api.endpoints.product_router import router as product_router
from infrastructure.api.exception_handler import repository_exception_handler
from infrastructure.containers import Container

app = FastAPI()


container = Container()

app.container = container

# zapobieganie CORS
origins = [
    "http://localhost:5173",  # frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows your frontend to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(
    product_router,
    prefix="/api",
    tags=["products"],
)
app.include_router(
    client_router,
    prefix="/api",
    tags=["clients"],
)
app.include_router(
    admin_router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(AuthService.is_admin)],
)
app.include_router(auth_router, prefix="/auth", tags=["admin"])

app.add_exception_handler(RepositoryError, repository_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
