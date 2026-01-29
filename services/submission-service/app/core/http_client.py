import httpx
from typing import Optional
from app.core.config import settings
from app.core.logging import logger


async def call_classification_service(image_path: str) -> Optional[dict]:
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            with open(image_path, "rb") as f:
                files = {"file": f}
                response = await client.post(
                    f"{settings.classification_service_url}/api/v1/classify",
                    files=files
                )
                response.raise_for_status()
                return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Classification service error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error calling classification service: {str(e)}")
        return None

