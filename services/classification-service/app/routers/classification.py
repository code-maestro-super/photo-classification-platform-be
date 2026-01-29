from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.classification import classify_image
from app.schemas.classification import ClassificationResponse
from app.core.logging import logger

router = APIRouter(prefix="/api/v1", tags=["classification"])


@router.post("/classify", response_model=ClassificationResponse)
async def classify_image_endpoint(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    try:
        image_bytes = await file.read()
        
        if len(image_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file"
            )
        
        result = classify_image(image_bytes)
        return ClassificationResponse(**result)
    
    except ValueError as e:
        logger.error(f"Classification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process image"
        )

