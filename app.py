from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate

from dotenv import load_dotenv

#load env
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Migrations

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

    def as_dict(self):
        return {'product_id': self.product_id, 'name': self.name, 'description': self.description}

@app.before_first_request
def create_tables():
    db.create_all()

# CREATE
@app.route('/', methods=['POST'])
def create_product():
    data = request.json
    if not data or 'product_id' not in data:
        abort(400, description="product_id is required")
    product = Product(product_id=data['product_id'], name=data.get('name', ''), description=data.get('description', ''))
    db.session.add(product)
    db.session.commit()
    return jsonify(product.as_dict()), 201

# READ
@app.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        abort(404)
    return jsonify(product.as_dict())

# UPDATE
@app.route('/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        abort(404)
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    db.session.commit()
    return jsonify(product.as_dict())

# DELETE
@app.route('/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        abort(404)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
