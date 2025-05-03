import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, jsonify, request

# Initialize Flask app
app = Flask(__name__)

# Path to your Firebase Admin SDK credentials JSON file
cred = credentials.Certificate('global-item-firebase-adminsdk-fbsvc-d0a37e65a7.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://global-item-default-rtdb.europe-west1.firebasedatabase.app/'  # Replace with your Firebase database URL
})

# Function to get the current global item count
def get_item_count():
    ref = db.reference('global_item_count')
    return ref.get() or 0  # Default to 0 if no count exists

# Function to update the global item count
def set_item_count(new_count):
    ref = db.reference('global_item_count')
    ref.set(new_count)  # Sets the global item count in Firebase to the new count

# Route to get the current global item count
@app.route('/get_item_count', methods=['GET'])
def get_count():
    count = get_item_count()
    return jsonify({'count': count})

# Route to increment the global item count
@app.route('/increment_item_count', methods=['POST'])
def increment_count():
    try:
        current_count = get_item_count()
        new_count = current_count + 1
        set_item_count(new_count)
        return jsonify({'new_count': new_count})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# Route for the root URL (optional)
@app.route('/')
def home():
    return "Welcome to the Global Item Count Server!"

# Start the Flask server
if __name__ == '__main__':
    # Debug mode is set to true for easier development (auto-reload on changes).
    # Set `debug=False` in production environments.
    app.run(host='0.0.0.0', port=5000, debug=True)  # Open the server to listen on all interfaces.
