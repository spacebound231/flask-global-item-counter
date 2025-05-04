from flask import Flask, jsonify, request
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

# POST route to update or insert an item count
@app.route('/update_item_count', methods=['POST'])
def update_item_count():
    data = request.get_json()  # Get the item name and count from the request
    item_name = data.get('name')
    item_count = data.get('count')

    if item_name and item_count is not None:
        # Try to find the item in the database
        item = collection.find_one({"name": item_name})
        if item:
            # If the item exists, update its count
            collection.update_one({"name": item_name}, {'$inc': {'count': item_count}})
        else:
            # If the item doesn't exist, create a new entry
            collection.insert_one({"name": item_name, "count": item_count})

        # Fetch the updated item to confirm
        updated_item = collection.find_one({"name": item_name})
        return jsonify({"name": updated_item["name"], "new_count": updated_item["count"]}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
