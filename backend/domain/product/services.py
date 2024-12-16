from domain.product.model import Product
from infrastructure.product.product_repository import upload_product_to_db, get_product_from_db, get_image_from_db
from fastapi.responses import StreamingResponse
from typing import Optional
from fastapi import HTTPException, status


async def upload_product(product_data: Product) -> dict:

    if not product_data:
        raise HTTPException(status_code=400, detail="Product data is missing")

    image_data = await product_data.file.read()

    if not image_data:
        raise HTTPException(status_code=400, detail="Image data is invalid or empty")

    product_id = upload_product_to_db(
        name=product_data.name,
        price=product_data.price,
        country_of_origin=product_data.country_of_origin,
        description=product_data.description,
        fruit_or_vegetable=product_data.fruit_or_vegetable,
        expiry_date=product_data.expiry_date,
        image_data=image_data,
    )

    return {"info": f"Product '{product_data.name}' uploaded successfully", "product_id": product_id}


def get_product(product_id: str):
    product = get_product_from_db(product_id)
    product_info = {}

    if product:
        product_info = {
                "name": product["name"],
                "price": product["price"],
                "country_of_origin": product["country_of_origin"],
                "description": product["description"],
                "fruit_or_vegetable": product["fruit_or_vegetable"],
                "expiry_date": product["expiry_date"],
                "imageId": product["imageId"],
            }
        
    if not product_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        
    return {"product": product_info}

def get_image(product_id: str) -> Optional[StreamingResponse]:
    product = get_product_from_db(product_id)

    image_response = None

    if product:
        image_data = get_image_from_db(product["imageId"])

        image_response = StreamingResponse(image_data, media_type="image/jpeg", headers={"Content-Disposition": f"attachment; filename={image_data.filename}"})

    if not image_response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Image for product with id {product_id} not found"
            )
    
    return image_response
