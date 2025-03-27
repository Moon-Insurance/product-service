import unittest
from unittest.mock import patch, MagicMock

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class MockProduct:
    def __init__(self, product_id, name, description):
        self.product_id = product_id
        self.name = name
        self.description = description

    def as_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description
        }

class ProductServiceUnitTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('app.db.session.add')
    @patch('app.db.session.commit')
    @patch('app.Product')
    def test_create_product(self, MockProductClass, mock_commit, mock_add):
        # Create a mock product instance (use MockProduct instead of a dictionary)
        mock_product = MockProduct('P001', 'Insurance Plan', 'Life Insurance')

        # Configure the mock Product class to return the mock product
        MockProductClass.return_value = mock_product

        # Mock the query filter to return None (no existing product)
        MockProductClass.query.filter_by.return_value.first.return_value = None

        # Call the API
        response = self.app.post('/products', json={
            'product_id': 'P001', 'name': 'Insurance Plan', 'description': 'Life Insurance'
        })
        
        # Assertions
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['product_id'], 'P001')

        # Ensure mocks were called
        MockProductClass.assert_called_once()
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
