import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db

class ProductServiceIntegrationTest(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_full_crud(self):
        # Create
        res = self.client.post('/products', json={'product_id': 'P100', 'name': 'Plan A', 'description': 'Basic'})
        self.assertEqual(res.status_code, 201)

        # Read
        res = self.client.get('/products/P100')
        data = res.get_json()
        self.assertEqual(data['name'], 'Plan A')

        # Update
        res = self.client.put('/products/P100', json={'name': 'Plan A+', 'description': 'Updated'})
        data = res.get_json()
        self.assertEqual(data['name'], 'Plan A+')

        # Delete
        res = self.client.delete('/products/P100')
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
