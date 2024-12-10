from fastapi import HTTPException
from infrastructure.mongo.client_handler import register_client, get_client as fetch_client

async def upload_client(client_data: Client):
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
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_client(client_id: str):
    try:
        client = fetch_client(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return {"client": client}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
