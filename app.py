#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

products = []

def search_for_products(keyword):
    product_name = keyword
    product_brands = ''
    product_ingredients = ''
    api_url = f'https://world.openfoodfacts.org/cgi/search.pl?search_terms={keyword}&lc=en&json=1&fields=product_name,brands,ingredients_text&page_size=1'
    
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data['count'] > 0:
            products = data.get('products')
            if products:
                product_info = products[0]
                name = product_info.get('product_name')
                brands = product_info.get('brands')
                ingredients = product_info.get('ingredients_text')
                if name:
                    product_name = name
                if brands:
                    product_brands = brands
                if ingredients:
                    product_ingredients = ingredients
    else:
        print(response)         
    return (product_name, product_brands, product_ingredients)


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
    search_term = data.get('name')
    product_quantity = data.get('quantity')
    product_id = max((p['id'] for p in products), default=0) + 1
    
    (product_name, product_brands, product_ingredients) = search_for_products(search_term)
    
    new_product = {"id": product_id, "name": product_name, "brands": product_brands, "ingredients": product_ingredients, "quantity": product_quantity}
    
    products.append(new_product)
    return jsonify(new_product), 201

@app.route('/inventory/<int:id>', methods=['PATCH'])
def update_product(id):
    data = request.get_json()
    product_index = next((index for (index, p) in enumerate(products) if p['id'] == id), None)

    if product_index == None:
        return ('Product not found', 404)
    for key in data:
        products[product_index][key] = data[key]

    return jsonify(products[product_index]), 200
    

@app.route('/inventory/<int:id>', methods=['DELETE'])
def delete_product(id):
    product_index = next((index for (index, p) in enumerate(products) if p['id'] == id), None)

    if product_index == None:
        return ('Product not found', 404)
    products.pop(product_index)
    
    return ('Product deleted', 204)

if __name__ == '__main__':
    app.run(port=5555, debug=True)