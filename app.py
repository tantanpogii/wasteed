from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from gradio_client import Client, handle_file
import os

# Initialize Flask app
app = Flask(__name__)

# Enable CORS on all routes or specify for particular routes
CORS(app)  # This will allow all domains. For security, you can specify allowed origins.

# Initialize Gradio Client
client = Client("cyrustristan/wasteed")

# Set your API key (or store it in an environment variable)
API_KEY = os.getenv('API_KEY', 'my-secure-api-key')  # Store your actual API key here or use environment variables

# Function to check if the API key is valid
def check_api_key(request):
    api_key = request.headers.get('X-API-KEY')
    if api_key != API_KEY:
        return False
    return True

@app.route('/predict', methods=['POST'])
def predict():
    # Check for API key in request headers
    if not check_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # Get data from the request
        data = request.get_json()
        image_url = data['image_url']
        
        # Make a prediction using Gradio
        result = client.predict(
            image=handle_file(image_url),
            conf=0.3,  # Confidence threshold
            api_name="/predict"
        )
        
        # Return the result from Gradio
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
