#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

products = []

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(products)

@app.route('/inventory/<int:id>')
def get_product(id):
    product = next((p for p in products if p['id'] == id), None)
    return jsonify(product) if product else ('Product not found', 404)

@app.route('/inventory', methods=['POST'])
def add_product():
    data = request.get_json()
    product_name = data.get('name')
    product_quantity = data.get('quantity')
    product_id = max((p['id'] for p in products), default=0) + 1
    new_product = {"id": product_id, "name": product_name, "quantity": product_quantity}
    products.append(new_product)
    return jsonify(new_product), 201

@app.route('/inventory/<int:id>', methods=['PATCH'])
def update_product(id):
    data = request.get_json()
    product_index = next((index for (index, p) in enumerate(products) if p['id'] == id), None)
    if product_index == None:
        return ('Product not found', 404)
    if "name" in data:
        products[product_index]["name"] = data["name"]
    if "quantity" in data:
        products[product_index]["quantity"] = data["quantity"]
    return jsonify(products[product_index]), 200
    

@app.route('/inventory/<int:id>', methods=['DELETE'])
def delete_product(id):
    product_index = next((index for (index, p) in enumerate(products) if p['id'] == id), None)
    if product_index == None:
        return ('Product not found', 404)
    products.pop(product_index)
    return ("Product deleted", 204)

if __name__ == '__main__':
    app.run(port=5555, debug=True)