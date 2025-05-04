import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get Mongo URI from environment
mongo_uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client["sample_mflix"]           # Replace with your DB name if different
collection = db.items                 # 'items' collection

# Home route
@app.route('/')
def home():
    return "✅ MongoDB Item Counter is running."

# (Optional) Get total count from the first item found
@app.route('/get_item_count', methods=['GET'])
def get_item_count():
    doc = collection.find_one({})
    count = doc['count'] if doc else 0
    return jsonify({"count": count})

# ✅ Handle batch updates from Roblox
@app.route('/increment_item_count', methods=['POST'])
def increment_item_count():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of items"}), 400

    for item in data:
        name = item.get('name')
        count = item.get('count', 0)
        mutation = item.get('mutation', "none")

        if name:
            collection.update_one(
                {"name": name},
                {
                    "$inc": {"count": count},
                    "$set": {"mutation": mutation}
                },
                upsert=True
            )

    return jsonify({"message": "Batch update successful"}), 200

# Run app on Render or locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
