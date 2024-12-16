from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel
from domain.client.model import Client
from domain.client.services import register_client, get_client

router = APIRouter()

@router.post("/register")
async def upload_client_endpoint(client_data: Client):
    try:
        response = register_client(client_data)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clients/{client_id}")
async def get_client_endpoint(client_id: str):
    try:
        response = get_client(client_id)
        
        if not response:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return response
    
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
