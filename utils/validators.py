import re
from fastapi import HTTPException

def validate_image_file(filename: str):
    allowed_extensions = ['.png', '.jpg', '.jpeg']
    if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only PNG, JPG, and JPEG are allowed."
        )
    return True
