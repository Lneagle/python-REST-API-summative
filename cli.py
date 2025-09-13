#!/usr/bin/env python3

import requests
import typer

server_url = 'http://127.0.0.1:5555/inventory'

app = typer.Typer()

def print_product(product):
    print(f"{product['id']}: {product['name']}")
    print(f"Quantity: {product['quantity']}")
    if product['brands']:
        print(f"Brands: {product['brands']}")
    if product['ingredients']:
        print(f"Ingredients: {product['ingredients']}")

@app.command()
def add_product(name: str, quantity: int):
    response = requests.post(server_url, json={'name': name, 'quantity': quantity})
    if response.status_code == 201:
        data = response.json()
        print(f"Product added: {data['name']}, quantity: {data['quantity']}")
    else:
        print (response.text)

@app.command()
def list_products():
    response = requests.get(server_url)
    data = response.json()
    if len(data) > 0:
        for item in data:
            print_product(item)
    else:
        print("No products in inventory")

@app.command()
def list_individual_product(id: int):
    response = requests.get(server_url + f'/{id}')
    if response.status_code == 200:
        print_product(response.json())
    else:
        print(response.text)

@app.command()
def update_product(id: int, name: str = '', quantity: int = None, brands: str = '', ingredients: str = ''):
    data = {}
    if name:
        data['name'] = name
    if quantity is not None:
        data['quantity'] = quantity
    if brands:
        data['brands'] = brands
    if ingredients:
        data['ingredients'] = ingredients
    response = requests.patch(server_url + f'/{id}', json=data)
    if response.status_code == 200:
        print_product(response.json())
    else:
        print(response.text)

@app.command()
def delete_product(id: int):
    response = requests.delete(server_url + f'/{id}')
    if response.status_code == 204:
        print(f"Product {id} deleted")
    else:
        print(response.text)

if __name__ == "__main__":
    app()