from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from services.product_service import upload_product, get_product, stream_product_image

router = APIRouter()

@router.post("/upload")
async def upload_product_endpoint(item: Upload_product_request, file: UploadFile):
    return await upload_product(item, file)

@router.get("/products/{product_id}")
async def get_product_endpoint(product_id: str):
    return await get_product(product_id)

@router.get("/images/{image_id}")
async def get_image_endpoint(image_id: str):
    return await stream_product_image(image_id)
