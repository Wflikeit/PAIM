from domain.exceptions import ProductNotFoundError, RepositoryError
from infrastructure.api.endpoints.product_router import router as product_router
from infrastructure.api.endpoints.client_router import router as client_router
from infrastructure.api.endpoints.auth_router import router as admin_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request, Depends

from infrastructure.api.exception_handler import repository_exception_handler
from infrastructure.containers import Container

#
# def check_json_content_type(request: Request):
#     if request.method in ["POST", "PUT", "PATCH"]:
#         content_type = request.headers.get("Content-Type", "")
#
#         if "multipart/form-data" in content_type:
#             return
#
#         if content_type != "application/json":
#             raise HTTPException(status_code=400, detail="Content-Type must be application/json")
#
# app = FastAPI(dependencies=[Depends(check_json_content_type)])
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

app.include_router(product_router, prefix="/api", tags=["products"])
app.include_router(client_router, prefix="/api", tags=["clients"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])

app.add_exception_handler(RepositoryError, repository_exception_handler)
