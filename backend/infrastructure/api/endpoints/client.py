from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from infrastructure.mongo.client_handler import register_client, get_client

class Client(BaseModel):
    email: str
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
    
    try:
        client_id = register_client(
            client_data.email,
            client_data.payment_address,
            client_data.delivery_address,
            client_data.nip,
            client_data.orders,
            client_data.password,
            client_data.company_name
        )

        return {
            "info": f"Client '{client_data.email}' registered successfully",
            "client_id": client_id,
            "email": client_data.email,
            "payment_address": client_data.payment_address,
            "delivery_address": client_data.delivery_address,
            "nip": client_data.nip,
            "orders": client_data.orders,
            "password": client_data.password,
            "company_name": client_data.company_name,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clients/{client_id}")
async def get_client_endpoint(client_id: str):
    try:
        client = get_client(client_id)
        
        if not client:
            raise HTTPException(status_code=404, detail="Product not found")
        
        client_info = {
            "email": client["email"],
            "payment_address": client["payment_address"],
            "delivery_address": client["delivery_address"],
            "nip": client["nip"],
            "orders": client["orders"],
            "password": client["password"],
            "company_name": client["company_name"],
        }
        
        return {"client": client_info}
    
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
