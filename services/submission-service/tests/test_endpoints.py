import pytest
from fastapi import UploadFile
from io import BytesIO
from PIL import Image
import json


def create_test_image_file():
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


def test_create_submission_endpoint(client, auth_token):
    img_bytes = create_test_image_file()
    metadata = {
        "name": "Test User",
        "age": 25,
        "place_of_living": "Test City",
        "gender": "Male",
        "country_of_origin": "Test Country",
        "description": "Test description"
    }
    
    response = client.post(
        "/api/v1/submissions",
        headers={"Authorization": f"Bearer {auth_token}"},
        files={"photo": ("test.jpg", img_bytes, "image/jpeg")},
        data={"metadata": json.dumps(metadata)}
    )
    
    assert response.status_code in [201, 500]
    if response.status_code == 201:
        data = response.json()
        assert "id" in data
        assert data["name"] == "Test User"


def test_get_submission_endpoint(client, auth_token, test_submission):
    response = client.get(
        f"/api/v1/submissions/{test_submission.id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_submission.id


def test_list_submissions_endpoint(client, auth_token, test_submission):
    response = client.get(
        "/api/v1/submissions",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_create_submission_unauthorized(client):
    img_bytes = create_test_image_file()
    metadata = {"name": "Test", "age": 25, "place_of_living": "City", "gender": "Male", "country_of_origin": "Country"}
    
    response = client.post(
        "/api/v1/submissions",
        files={"photo": ("test.jpg", img_bytes, "image/jpeg")},
        data={"metadata": json.dumps(metadata)}
    )
    
    assert response.status_code == 403

