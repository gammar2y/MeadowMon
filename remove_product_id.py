from pymongo import MongoClient

# MongoDB connection URI
uri = "mongodb+srv://meadowmonbusiness:NXVwZOXBQChb01uj@meadowmon.zcf42.mongodb.net/MeadowMon?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(uri)
db = client.MeadowMon
products_collection = db.products

# Remove the product_id field from documents with null product_id
result = products_collection.update_many(
    {"product_id": None},
    {"$unset": {"product_id": ""}}
)

print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents.")

# Use aggregation pipeline to update documents
pipeline = [
    {
        "$set": {
            "id": "$product_id"
        }
    },
    {
        "$unset": "product_id"
    }
]

# Perform the update
result = products_collection.update_many({}, pipeline)

print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents.")