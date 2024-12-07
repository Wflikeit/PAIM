from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from infrastructure.mongo.product_handler import upload_product, get_product, get_image
from fastapi.responses import StreamingResponse
from io import BytesIO

router = APIRouter()

@router.post("/upload")
async def upload_product_endpoint(
    name: str = Form(...),
    price: float = Form(...),
    country_of_origin: str = Form(...),
    description: str = Form(...),
    fruit_or_vegetable: str = Form(...),
    file: UploadFile = File(...),
    expiry_date: str = Form(...),
):
    try:
        file_data = await file.read()
        
        product_id = upload_product(name, price, country_of_origin, description, fruit_or_vegetable, file_data, expiry_date, file.filename)
        
        return {"info": f"Product '{name}' uploaded successfully", "product_id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/products/{product_id}")
async def get_product_endpoint(product_id: str):
    try:
        product = get_product(product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        image_id = product.get("imageId")
        image_data = get_image(image_id)
        if not image_data:
            raise HTTPException(status_code=404, detail="Image not found")
        
        product_info = {
            "name": product["name"],
            "price": product["price"],
            "country_of_origin": product["country_of_origin"],
            "description": product["description"],
            "fruit_or_vegetable": product["fruit_or_vegetable"],
            "imageId": image_id,
            "expiry_date": product["expiry_date"],
        }
        
        return {"product": product_info}
    
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images/{image_id}")
async def get_product_endpoint(image_id: str):
    try:
        image_data = get_image(image_id)
        
        if not image_data:
            raise HTTPException(status_code=404, detail="Image not found")
        
        return StreamingResponse(image_data, media_type="image/jpeg", headers={"Content-Disposition": f"attachment; filename={image_data.filename}"})
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
