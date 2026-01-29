import pytest
from fastapi import UploadFile
from io import BytesIO
from app.core.storage import save_file, validate_file, validate_image_content
from PIL import Image


def create_test_image():
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


def test_validate_file_valid():
    img_bytes = create_test_image()
    file = UploadFile(filename="test.jpg", file=img_bytes)
    file.content_type = "image/jpeg"
    
    try:
        validate_file(file)
        assert True
    except Exception:
        pytest.fail("Valid file should not raise exception")


def test_validate_file_invalid_type():
    file = UploadFile(filename="test.pdf", file=BytesIO(b"fake pdf"))
    file.content_type = "application/pdf"
    
    with pytest.raises(Exception):
        validate_file(file)


def test_validate_image_content_valid():
    img_bytes = create_test_image()
    content = img_bytes.read()
    img_bytes.seek(0)
    
    try:
        validate_image_content(content)
        assert True
    except Exception:
        pytest.fail("Valid image should not raise exception")


def test_validate_image_content_invalid():
    invalid_content = b"not an image"
    
    with pytest.raises(Exception):
        validate_image_content(invalid_content)


@pytest.mark.asyncio
async def test_save_file(temp_upload_dir):
    img_bytes = create_test_image()
    file = UploadFile(filename="test.jpg", file=img_bytes)
    file.content_type = "image/jpeg"
    
    import os
    os.environ["UPLOAD_DIR"] = temp_upload_dir
    
    file_path = await save_file(file)
    
    assert file_path is not None
    assert os.path.exists(file_path)

