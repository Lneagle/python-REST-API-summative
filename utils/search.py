import requests

def search_for_products(keyword, fields):
    product_name = keyword
    product_brands = ''
    product_ingredients = ''
    api_fields = ','.join(fields)
    api_url = f'https://world.openfoodfacts.org/cgi/search.pl?search_terms={keyword}&lc=en&json=1&fields={api_fields}&page_size=1'
    print(api_url)
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