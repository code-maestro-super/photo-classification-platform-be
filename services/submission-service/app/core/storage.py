import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from PIL import Image
from app.core.config import settings


def ensure_upload_dir():
    upload_path = Path(settings.upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)
    return upload_path


def validate_file(file: UploadFile) -> None:
    if file.content_type not in settings.allowed_file_types_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(settings.allowed_file_types_list)}"
        )


def validate_image_content(content: bytes) -> None:
    try:
        from io import BytesIO
        image = Image.open(BytesIO(content))
        image.verify()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file"
        )


async def save_file(file: UploadFile) -> str:
    validate_file(file)
    
    file.file.seek(0)
    content = await file.read()
    
    if len(content) > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {settings.max_file_size} bytes"
        )
    
    validate_image_content(content)
    
    upload_dir = ensure_upload_dir()
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = upload_dir / unique_filename
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    return str(file_path)


def get_file_path(filename: str) -> str:
    return os.path.join(settings.upload_dir, filename)

