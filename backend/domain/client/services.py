from domain.client.model import Client
from infrastructure.client.client_repository import register_client_db, get_client_db
from typing import Optional
from fastapi import HTTPException, status

def register_client(client_data: Client):
    
    client_id = register_client_db(client_data)
    
    return {
            "info": f"Client '{client_data.email}' registered successfully",
            "client_id": client_id,
        }

def get_client(client_id: str) -> Optional[dict]:
    client = get_client_db(client_id)
    client_info = {}

    if client:
        client_info = {
                "email": client["email"],
                "payment_address": client["payment_address"],
                "delivery_address": client["delivery_address"],
                "nip": client["nip"],
                "orders": client["orders"],
                "password": client["password"],
                "company_name": client["company_name"],
            }
        
    if not client_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )
        
    return {"client": client_info}