from PIL import Image
import io
import os
from typing import Optional, Tuple

class ImageService:
    @staticmethod
    def process_image(
        content: bytes,
        quality: int = 80,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None
    ) -> Tuple[io.BytesIO, str]:
        image = Image.open(io.BytesIO(content))
        
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        if max_width or max_height:
            image = ImageService._resize_image(image, max_width, max_height)
        
        output = io.BytesIO()
        image.save(output, format="WEBP", quality=quality, method=6)
        output.seek(0)
        
        temp_file = "temp_compressed.webp"
        with open(temp_file, "wb") as f:
            f.write(output.getvalue())
            
        return output, temp_file

    @staticmethod
    def _resize_image(
        image: Image.Image,
        max_width: Optional[int],
        max_height: Optional[int]
    ) -> Image.Image:
        original_width, original_height = image.size
        
        if max_width and max_height:
            ratio = min(max_width / original_width, max_height / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
        elif max_width:
            ratio = max_width / original_width
            new_width = max_width
            new_height = int(original_height * ratio)
        else:
            ratio = max_height / original_height
            new_width = int(original_width * ratio)
            new_height = max_height
            
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)