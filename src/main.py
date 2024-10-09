from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from src.style_transfer_app import StyleTransferApp
from io import BytesIO
from PIL import Image

app = FastAPI()

@app.post("/stylize")
async def stylize_image(image: UploadFile = File(...), style: str = 'pixar'):
    """
    API endpoint to apply a style to an uploaded image.
    :param image: Uploaded image file
    :param style: Desired style ('pixar', 'pixel_art', 'vice', 'anime')
    :return: Stylized image as a StreamingResponse
    """
    if style not in ['pixar', 'pixel_art', 'vice', 'anime']:
        raise HTTPException(status_code=400, detail="Invalid style choice.")
    
    try:
        # Read uploaded image
        image_data = await image.read()
        input_image = Image.open(BytesIO(image_data)).convert("RGB")
        
        # Instantiate the application and apply the style
        app_instance = StyleTransferApp(input_image, style)
        stylized_image = app_instance.run()

        # Save the image to a buffer to return as response
        buffer = BytesIO()
        stylized_image.save(buffer, format="PNG")
        buffer.seek(0)

        # Return the image as a streaming response
        return StreamingResponse(buffer, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stylizing image: {e}")