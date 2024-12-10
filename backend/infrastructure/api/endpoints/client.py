from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr
from services.client_service import upload_client, get_client

class Client(BaseModel):
    email: EmailStr
    payment_address: str
    delivery_address: str
    nip: str
    orders: str
    password: str
    company_name: str

router = APIRouter()

@router.post("/register")
async def upload_client_endpoint(client_data: Client, request: Request):
    if request.headers.get("Content-Type") != "application/json":
        raise HTTPException(status_code=400, detail="Content-Type must be application/json")
    return await upload_client(client_data)

@router.get("/clients/{client_id}")
async def get_client_endpoint(client_id: str):
    return await get_client(client_id)
