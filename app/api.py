from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Form
from fastapi.responses import FileResponse
from .models import apply_style
from .schemas import StyleOptions
from uuid import uuid4
import os

router = APIRouter()

# Directory to store uploaded and processed images
UPLOAD_DIR = "uploads/"
PROCESSED_DIR = "processed/"

@router.post("/style-transfer/")
async def style_transfer(
    file: UploadFile = File(...), 
    style: str = Form("anime"), 
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    # Save uploaded image
    file_ext = file.filename.split('.')[-1]
    if not file_ext in ("jpg", "jpeg", "png"):
        raise HTTPException(status_code=400, detail="Image format not supported.")
    
    image_id = str(uuid4())
    upload_path = os.path.join(UPLOAD_DIR, f"{image_id}.{file_ext}")
    
    with open(upload_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Process image in the background
    background_tasks.add_task(apply_style, upload_path, style)
    
    return {"message": "Image uploaded successfully", "image_id": image_id}

@router.get("/result/{image_id}")
async def get_result(image_id: str):
    processed_path = os.path.join(PROCESSED_DIR, f"{image_id}.png")
    if not os.path.exists(processed_path):
        raise HTTPException(status_code=404, detail="Result not ready yet.")
    
    return FileResponse(processed_path)