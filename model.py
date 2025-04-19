import cv2
import numpy as np
from PIL import Image
import io
from ultralytics import YOLO
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SolarPanelDetector:
    def __init__(self, model_path='best.pt'):
        try:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            logger.info(f"Loading model from: {model_path}")
            self.model = YOLO(model_path)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
        
    def detect(self, image):
        try:
            # Convert image to RGB if it's not
            if isinstance(image, np.ndarray):
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            logger.info("Performing detection")
            # Perform detection
            results = self.model(image)
            
            # Plot the results on the image
            result_image = results[0].plot()
            
            # Convert back to BGR for OpenCV if needed
            if len(result_image.shape) == 3 and result_image.shape[2] == 3:
                result_image = cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)
            
            logger.info("Detection completed successfully")
            return result_image
        except Exception as e:
            logger.error(f"Error during detection: {str(e)}")
            raise

    def process_image(self, image_data):
        try:
            # Convert bytes to image
            image = Image.open(io.BytesIO(image_data))
            image = np.array(image)
            
            logger.info(f"Processing image of shape: {image.shape}")
            # Perform detection
            result_image = self.detect(image)
            
            # Convert to bytes for sending back
            _, buffer = cv2.imencode('.jpg', result_image)
            logger.info("Image processing completed successfully")
            return buffer.tobytes()
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise
