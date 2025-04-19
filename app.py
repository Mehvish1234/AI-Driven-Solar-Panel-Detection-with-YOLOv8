from flask import Flask, request, render_template, send_file, jsonify
from model import SolarPanelDetector
import io
import logging

app = Flask(__name__)
detector = SolarPanelDetector()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Read the image data
        image_data = file.read()
        
        # Process the image
        result_image = detector.process_image(image_data)
        
        # Return the processed image
        return send_file(
            io.BytesIO(result_image),
            mimetype='image/jpeg'
        )
    except Exception as e:
        logging.error(f"Error in detect endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 