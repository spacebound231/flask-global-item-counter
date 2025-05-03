import os
from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Get Mongo URI from .env
mongo_uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client["sample_mflix"]
collection = db.items  # Use 'items' collection

# GET item count
@app.route('/get_item_count', methods=['GET'])
def get_item_count():
    doc = collection.find_one({})
    count = doc['count'] if doc else 0
    return jsonify({"count": count})

# POST to increment item count
@app.route('/increment_item_count', methods=['POST'])
def increment_item_count():
    collection.update_one({}, {'$inc': {'count': 1}}, upsert=True)
    doc = collection.find_one({})
    return jsonify({"new_count": doc['count']})

# Home route
@app.route('/')
def home():
    return "MongoDB Item Counter is running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
