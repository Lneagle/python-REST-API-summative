# Inventory Management CLI
This inventory management system consists of a server which maintains the inventory data and a CLI to interact with the server

## Installation
Use pipenv to install required packages
```bash
pipenv install
```

## Usage
Start the server:
```bash
python server.py
```

Run the CLI:
```bash
# Lists products in inventory
python cli.py list-products

# Adds product to inventory (requires product name and quantity)
python cli.py add-product "oreos" 10

# Lists individual product (requires product id)
python cli.py list-individual-product 1

# Updates individual product (requires product id plus any of: name, quantity, brands, ingredients
python cli.py update-product 1 --name "Oreos" --quantity 50 --brands "Nabisco" --ingredients "sugar, flour, etc."

# Deletes product (requires product id)
python cli.py delete-product 1
```

`add-product` uses the [Open Food Facts](https://world.openfoodfacts.org/) API to search for product names, brands, and ingredients and add them to the inventory

## Future Considerations
Currently, `add-product` uses the first search result for the user-entered term to determine the product name and information to enter into the inventory.  Future updates could improve this process to allow users to choose from more search results.
