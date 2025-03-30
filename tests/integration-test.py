from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool
import pytest
import os
import sys
import json


# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, Product

@pytest.fixture(scope='module')
def test_client():
    """Fixture to set up a clean test database and provide a test client."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',"sqlite:///:memory:" )  # Use local DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'poolclass': NullPool  # Disable pooling, ensuring a single connection
    }
    with app.app_context():
        db.drop_all()  # Drop all tables before running tests
        db.create_all()  # Recreate tables for fresh start

        yield app.test_client()  # Provide the test client for testing

        db.session.remove()
        db.drop_all()  # Cleanup after all tests

@pytest.fixture(scope='function', autouse=True)
def cleanup_database():
    """Ensure the database is clean before each test."""
    with app.app_context():
        db.session.query(Product).delete()  # Remove all Sale records before each test
        db.session.commit()


test_prodcut = {
    "product_id" : "P111",
    "name" : "Product 1",
    "description": "This is product 1"
}

def test_create_product(test_client):
    response = test_client.post('/', data=json.dumps(test_prodcut), content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['product_id'] == test_prodcut['product_id']

def test_get_product(test_client):
    test_client.post('/', data=json.dumps(test_prodcut), content_type='application/json')  # Insert data first
    response = test_client.get(f"/{test_prodcut['product_id']}")
    assert response.status_code == 200
    data = response.get_json()
    assert data['product_id'] == test_prodcut['product_id']

def test_update_product(test_client):
    test_client.post('/', data=json.dumps(test_prodcut), content_type='application/json')  # Insert data first
    update_data = {"description": "Product 01 updated"}
    response = test_client.put(f"/{test_prodcut['product_id']}", data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['description'] == update_data['description']

def test_delete_product(test_client):
    test_client.post('/', data=json.dumps(test_prodcut), content_type='application/json')  # Insert data first
    response = test_client.delete(f"/{test_prodcut['product_id']}")
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Product deleted'

    response = test_client.get(f"/{test_prodcut['product_id']}")  # Verify deletion
    assert response.status_code == 404
