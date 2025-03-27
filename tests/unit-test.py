import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, Product  # Ensure you import the necessary modules from your app

os.environ['DATABASE_URI'] = 'sqlite:///:memory:'

class ProductServiceUnitTest(unittest.TestCase):
    def setUp(self):
        # Configure the app to use an in-memory SQLite database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///:memory:')  # In-memory database
        app.config['TESTING'] = True  # Enable testing mode
        self.app = app.test_client()  # Create a test client for making requests
        with app.app_context():
            db.create_all()  # Create all tables in the in-memory database

    def tearDown(self):
        # Remove any session and drop all tables after the test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_product(self):
        # Test the product creation endpoint
        response = self.app.post('/products', json={
            'product_id': 'P001', 'name': 'Insurance Plan', 'description': 'Life Insurance'
        })
        self.assertEqual(response.status_code, 201)  # Check if the status code is 201 (Created)
        data = response.get_json()  # Get the response data as JSON
        self.assertEqual(data['product_id'], 'P001')  # Check if the product_id is as expected

if __name__ == '__main__':
    unittest.main()
