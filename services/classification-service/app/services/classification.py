from PIL import Image
import numpy as np
from typing import Dict, Any
from io import BytesIO


def preprocess_image(image: Image.Image) -> np.ndarray:
    image = image.convert("RGB")
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    return img_array


def classify_image(image_bytes: bytes) -> Dict[str, Any]:
    try:
        image = Image.open(BytesIO(image_bytes))
        img_array = preprocess_image(image)
        
        avg_brightness = np.mean(img_array)
        color_variance = np.var(img_array)
        dominant_color = np.mean(img_array, axis=(0, 1))
        
        categories = []
        confidence_scores = []
        
        if avg_brightness > 0.7:
            categories.append("bright")
            confidence_scores.append(0.85)
        elif avg_brightness < 0.3:
            categories.append("dark")
            confidence_scores.append(0.80)
        else:
            categories.append("medium")
            confidence_scores.append(0.75)
        
        if color_variance > 0.1:
            categories.append("colorful")
            confidence_scores.append(0.70)
        else:
            categories.append("monochrome")
            confidence_scores.append(0.65)
        
        if dominant_color[0] > 0.6:
            categories.append("warm_tone")
            confidence_scores.append(0.60)
        elif dominant_color[2] > 0.6:
            categories.append("cool_tone")
            confidence_scores.append(0.60)
        
        primary_category = categories[0] if categories else "unknown"
        avg_confidence = np.mean(confidence_scores) if confidence_scores else 0.5
        
        return {
            "category": primary_category,
            "categories": categories,
            "confidence": round(float(avg_confidence), 2),
            "details": {
                "brightness": round(float(avg_brightness), 3),
                "color_variance": round(float(color_variance), 3),
                "dominant_colors": [round(float(c), 3) for c in dominant_color]
            }
        }
    except Exception as e:
        raise ValueError(f"Failed to classify image: {str(e)}")

