from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Get Mongo URI from .env
mongo_uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client["sample_mflix"]
collection = db.items  # Use 'items' collection

# POST to update item count and mutation
@app.route('/update_item_count', methods=['POST'])
def update_item_count():
    data = request.get_json()
    
    if not data or 'name' not in data or 'count' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    item_name = data['name']
    count = data['count']
    mutation = data.get('mutation', "No mutation")  # Default to "No mutation" if not provided

    # Update the item in the database
    result = collection.update_one(
        {"name": item_name},  # Filter by item name
        {
            "$inc": {"count": count},  # Increment the count field
            "$set": {"mutation": mutation}  # Set the mutation value
        },
        upsert=True  # If the item does not exist, it will be created
    )
    
    if result.modified_count > 0:
        return jsonify({"message": "Item count and mutation updated successfully"})
    else:
        return jsonify({"message": "Item already up to date or created"}), 200

# Home route
@app.route('/')
def home():
    return "MongoDB Item Counter is running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
