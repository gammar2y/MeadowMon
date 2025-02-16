import json
import os
from pymongo import MongoClient

# MongoDB connection URI
uri = "mongodb+srv://meadowmonbusiness:NXVwZOXBQChb01uj@meadowmon.zcf42.mongodb.net/MeadowMon?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(uri)
db = client.MeadowMon
products_collection = db.products

# Path to the products.json file
json_file_path = os.path.join('products.json')

# Verify the JSON file path
print(f"Loading products from: {json_file_path}")

# Read the JSON file
try:
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Failed to decode JSON file. {str(e)}")
    exit(1)

# Extract products from the JSON data
products = data.get('products', [])

# Verify the products data
print(f"Found {len(products)} products in the JSON file.")

# Load products into the database
for product_data in products:
    print(f"Loading product: {product_data['name']}")
    products_collection.update_one(
        {'id': product_data['id']},
        {'$set': product_data},
        upsert=True
    )

print("Products have been loaded into the database.")