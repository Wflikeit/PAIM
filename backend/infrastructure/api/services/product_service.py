from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from infrastructure.mongo.product_handler import upload_product as db_upload_product, get_product as db_get_product, get_image

async def upload_product(item: Upload_product_request, file: UploadFile):
    try:
        file_data = await file.read()
        product_id = db_upload_product(
            item.name,
            item.price,
            item.country_of_origin,
            item.description,
            item.fruit_or_vegetable,
            file_data,
            item.expiry_date,
            file.filename
        )
        return {"info": f"Product '{item.name}' uploaded successfully", "product_id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_product(product_id: str):
    try:
        product = db_get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def stream_product_image(image_id: str):
    try:
        image_data = get_image(image_id)
        if not image_data:
            raise HTTPException(status_code=404, detail="Image not found")
        return StreamingResponse(
            image_data,
            media_type="image/jpeg",
            headers={"Content-Disposition": f"attachment; filename={image_data.filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
