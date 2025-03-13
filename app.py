from flask import Flask, request, jsonify
from gradio_client import Client, handle_file

# Initialize Flask app
app = Flask(__name__)

# Initialize Gradio Client
client = Client("cyrustristan/wasteed")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Handle image file upload
        image = request.files['image']
        
        # Save the image temporarily to process it
        image_path = "/tmp/uploaded_image.jpg"
        image.save(image_path)

        # Make a prediction using Gradio
        result = client.predict(
            image=handle_file(image_path),
            conf=0.3,  # Confidence threshold
            api_name="/predict"
        )

        # Return the result from Gradio (image URL or processed image)
        processed_image_url = f"https://wasteed.onrender.com/{result}"  # Assuming this is the URL
        return jsonify({"image_url": processed_image_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
