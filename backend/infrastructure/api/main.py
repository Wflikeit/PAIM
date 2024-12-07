# api/main.py
from fastapi import FastAPI
from infrastructure.api.endpoints.product import router as product_router
from infrastructure.api.endpoints.client import router as client_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
