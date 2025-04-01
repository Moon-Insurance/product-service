import pytest
import os
import requests
import json

# Set the base URL for your deployed service; defaults to localhost if not provided.
BASE_URL = os.getenv('BASE_URL', 'http://localhost:5005')

# Sample test data for a product
test_product = {
    "product_id": "P111",
    "name": "Product 1",
    "description": "This is product 1"
}

@pytest.fixture(scope='function', autouse=True)
def cleanup_database():
    """
    Ensure cleanup after each test by deleting the test product.
    This fixture runs after each test (due to autouse=True).
    """
    yield  # Run the test first
    # Send a DELETE request to remove the test product
    requests.delete(f"{BASE_URL}/{test_product['product_id']}")

def test_create_product():
    response = requests.post(f"{BASE_URL}/", json=test_product)
    assert response.status_code == 201
    data = response.json()
    assert data['product_id'] == test_product['product_id']

def test_get_product():
    # Insert product first
    create_resp = requests.post(f"{BASE_URL}/", json=test_product)
    assert create_resp.status_code == 201

    response = requests.get(f"{BASE_URL}/{test_product['product_id']}")
    assert response.status_code == 200
    data = response.json()
    assert data['product_id'] == test_product['product_id']

def test_update_product():
    # Insert product first
    create_resp = requests.post(f"{BASE_URL}/", json=test_product)
    assert create_resp.status_code == 201

    update_data = {"description": "Product 01 updated"}
    response = requests.put(f"{BASE_URL}/{test_product['product_id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['description'] == update_data['description']

def test_delete_product():
    # Insert product first
    create_resp = requests.post(f"{BASE_URL}/", json=test_product)
    assert create_resp.status_code == 201

    response = requests.delete(f"{BASE_URL}/{test_product['product_id']}")
    assert response.status_code == 200
    assert response.json()['message'] == 'Product deleted'

    # Verify deletion: a GET request should return 404
    get_resp = requests.get(f"{BASE_URL}/{test_product['product_id']}")
    assert get_resp.status_code == 404
