from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from typing import Optional
from mangum import Mangum
from app.services.image_service import ImageService
import os

app = FastAPI(title="API de Compresión de Imágenes")

@app.post("/compress")
async def compress_image(
    file: UploadFile = File(...),
    quality: Optional[int] = 80,
    max_width: Optional[int] = None,
    max_height: Optional[int] = None
):
    content = await file.read()
    _, temp_file = ImageService.process_image(content, quality, max_width, max_height)
    
    response = FileResponse(
        temp_file,
        media_type="image/webp",
        filename=f"{file.filename.split('.')[0]}.webp"
    )
    
    def cleanup():
        try:
            os.remove(temp_file)
        except:
            pass
            
    response.background = cleanup
    return response

handler = Mangum(app)