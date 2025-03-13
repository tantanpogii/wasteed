
from flask import Flask, request, jsonify
from gradio_client import Client, handle_file

# Initialize Flask app
app = Flask(__name__)

# Initialize Gradio Client
client = Client("cyrustristan/wasteed")

@app.route('/predict', methods=['POST'])
def predict():
    try:
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
