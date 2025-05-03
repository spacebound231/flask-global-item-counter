import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# MongoDB URI from environment variable
mongo_uri = os.getenv("MONGO_URI")

# Initialize MongoClient
client = MongoClient(mongo_uri)

# Database and collection
db = client.get_database()  # Get the default database
collection = db.items  # Assuming you want to work with the 'items' collection

# Flask routes
app = Flask(__name__)

@app.route('/get_item_count', methods=['GET'])
def get_item_count():
    # Count the number of documents in the 'items' collection
    count = collection.count_documents({})
    return jsonify({"count": count})

@app.route('/increment_item_count', methods=['POST'])
def increment_item_count():
    # Increment the 'count' field in the first document (or create one if it doesn't exist)
    collection.update_one({}, {'$inc': {'count': 1}}, upsert=True)
    return jsonify({"message": "Item count incremented successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
