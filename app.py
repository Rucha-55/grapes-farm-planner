import os
from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2

app = Flask(__name__)

# Load the model
model = load_model("grape_model.h5")

# Class labels for grape diseases
class_names = ['Black Rot', 'Leaf Blight', 'Healthy', 'ESCA']

# Disease Information Dictionary
disease_info = {
    'Black Rot': {
        'symptoms': [
            'Circular brown lesions on leaves',
            'Dark sunken spots on fruit',
            'Fruit shriveling and drying on vines'
        ],
        'pesticides': ['Mancozeb', 'Myclobutanil', 'Captan'],
        'prevention': ['Prune infected parts', 'Ensure good air circulation']
    },
    'Leaf Blight': {
        'symptoms': ['Yellowish-brown spots on leaves', 'Leaf curling'],
        'pesticides': ['Streptomycin Sulfate', 'Copper Oxychloride'],
        'prevention': ['Remove fallen leaves', 'Use resistant varieties']
    },
    'Healthy': {
        'symptoms': ['Lush green leaves', 'Healthy fruit production'],
        'pesticides': ['Neem Oil Spray', 'Sulfur Dust'],
        'prevention': ['Optimal watering', 'Regular plant inspection']
    },
    'ESCA': {
        'symptoms': ['Wood discoloration', 'Sudden wilting'],
        'pesticides': ['Fluazinam', 'Carbendazim'],
        'prevention': ['Avoid wounding vines', 'Proper irrigation techniques']
    }
}

# Set upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def preprocess_image(image_path, target_size=(224, 224)):
    img = load_img(image_path, target_size=target_size)
    x = img_to_array(img)
    x = x.astype('float32') / 255.
    x = np.expand_dims(x, axis=0)
    return x

def is_grape_leaf_image(image_path):
    """
    Modified function to detect grape leaves specifically.
    """
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        return False, "Could not read image file"
    
    # Convert to HSV color space for better color analysis
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Green ranges to capture various grape leaf colors
    green_ranges = [
        # Standard green range
        (np.array([25, 30, 30]), np.array([95, 255, 255])),
        # Yellowish-green (some grape varieties)
        (np.array([10, 30, 30]), np.array([30, 255, 255])),
        # Darker green (common in many grape varieties)
        (np.array([40, 30, 15]), np.array([90, 255, 100]))
    ]
    
    combined_mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    
    # Combine all green masks
    for lower_green, upper_green in green_ranges:
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        combined_mask = cv2.bitwise_or(combined_mask, green_mask)
    
    # Calculate percentage of potential leaf-colored pixels
    green_percentage = np.sum(combined_mask > 0) / (combined_mask.shape[0] * combined_mask.shape[1])
    
    # Convert to grayscale for texture analysis
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Check for human skin tones - common in human/animal images
    # Define skin color range in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 150, 255], dtype=np.uint8)
    skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
    skin_percentage = np.sum(skin_mask > 0) / (skin_mask.shape[0] * skin_mask.shape[1])
    
    # Define blue color range (common in clothing/jeans)
    lower_blue = np.array([90, 50, 50], dtype=np.uint8)
    upper_blue = np.array([130, 255, 255], dtype=np.uint8)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    blue_percentage = np.sum(blue_mask > 0) / (blue_mask.shape[0] * blue_mask.shape[1])
    
    # If significant skin tone or blue detected, likely not a leaf
    if skin_percentage > 0.15 or blue_percentage > 0.25:
        return False, "The image appears to contain skin tones or clothing colors rather than grape leaf structure"
    
    # Check for leaf texture using edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    # Look for the characteristic pattern of leaf veins
    edge_percentage = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
    
    # Apply texture analysis
    grid_size = 32
    height, width = gray.shape
    std_devs = []
    
    for y in range(0, height, grid_size):
        for x in range(0, width, grid_size):
            # Define region
            region = gray[y:min(y+grid_size, height), x:min(x+grid_size, width)]
            if region.size > 0:
                std_devs.append(np.std(region))
    
    # Calculate texture variation
    if std_devs:
        texture_variation = np.mean(std_devs)
    else:
        texture_variation = 0
    
    # Look for grape leaf specific characteristics:
    # - Palmate shape
    # - Serrated edges
    # - Characteristic vein pattern
    
    # Core criteria for grape leaf detection
    if green_percentage > 0.15:  # Must have significant green content
        if edge_percentage > 0.02 and texture_variation > 5:  # Must have vein-like edges and texture
            return True, "Grape leaf structure detected based on color, veins, and texture"
    
    # Find contours for shape analysis
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    significant_contours = [c for c in contours if cv2.contourArea(c) > (img.shape[0] * img.shape[1] * 0.1)]
    
    # Check for geometric regularity (common in human-made objects)
    if significant_contours:
        largest_contour = max(significant_contours, key=cv2.contourArea)
        perimeter = cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, 0.04 * perimeter, True)
        
        # Grape leaves often have 5-7 lobes, so looking for complex shapes
        if len(approx) > 6:
            # Check for aspect ratio - grape leaves typically have specific proportions
            x, y, w, h = cv2.boundingRect(largest_contour)
            aspect_ratio = float(w) / h if h > 0 else 0
            
            # Grape leaves typically have aspect ratios close to 1 (roundish) 
            if 0.7 < aspect_ratio < 1.3 and green_percentage > 0.08 and texture_variation > 5:
                return True, "Grape leaf structure detected based on shape and color"
    
    # Final check - very high green content might still be a grape leaf despite other factors
    if green_percentage > 0.4 and skin_percentage < 0.05 and blue_percentage < 0.05:
        return True, "Grape leaf structure detected based on predominant green color"
    
    return False, "The image doesn't appear to contain a grape leaf structure"

@app.route('/')
def index():
    return render_template('index.html', diseases=class_names)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part', 'is_leaf': False})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file', 'is_leaf': False})
    
    if file:
        # Check if it's an image file
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({
                'error': 'File must be an image (PNG, JPG, JPEG)', 
                'is_leaf': False
            })
        
        # Save the file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Debug: Save original image dimensions
        original_img = cv2.imread(filepath)
        img_height, img_width = original_img.shape[:2]
        
        # Check if it appears to be a grape leaf image
        is_leaf, leaf_message = is_grape_leaf_image(filepath)
        
        if not is_leaf:
            result = {
                'prediction': 'Unsupported',
                'confidence': 0.0,
                'message': f'Unsupported image: {leaf_message}. Please upload an image of a grape leaf.',
                'is_leaf': False,
                'debug_info': {
                    'image_dimensions': f"{img_width}x{img_height}"
                }
            }
            return jsonify(result)
        
        # Preprocess and predict
        try:
            processed_image = preprocess_image(filepath)
            predictions = model.predict(processed_image)[0]
            
            # Get the predicted class
            predicted_class_index = np.argmax(predictions)
            predicted_disease = class_names[predicted_class_index]
            confidence = float(predictions[predicted_class_index])
            
            # Check for balanced distribution across classes, which might indicate a non-leaf image
            # If all classes have similar probabilities, it's likely an unrecognizable image
            probabilities = sorted(predictions)
            prob_diff = probabilities[-1] - probabilities[0]
            
            # If the confidence is too low or probabilities are very similar across classes
            if confidence < 0.4 or prob_diff < 0.2:
                result = {
                    'prediction': 'Unrecognized',
                    'confidence': confidence,
                    'message': 'This grape leaf image could not be classified with confidence. It may not be one of the supported leaf types.',
                    'is_leaf': True,
                    'debug_info': {
                        'image_dimensions': f"{img_width}x{img_height}",
                        'probabilities': [float(p) for p in predictions]
                    }
                }
            else:
                # Get disease information
                disease_data = disease_info.get(predicted_disease, {})
                symptoms = disease_data.get('symptoms', [])
                pesticides = disease_data.get('pesticides', [])
                prevention = disease_data.get('prevention', [])
                
                result = {
                    'prediction': predicted_disease,
                    'confidence': confidence,
                    'message': f'This grape leaf appears to have {predicted_disease} with {confidence:.2%} confidence.',
                    'is_leaf': True,
                    'disease_info': {
                        'symptoms': symptoms,
                        'pesticides': pesticides,
                        'prevention': prevention
                    },
                    'debug_info': {
                        'image_dimensions': f"{img_width}x{img_height}",
                        'probabilities': [float(p) for p in predictions]
                    }
                }
            
            return jsonify(result)
        
        except Exception as e:
            return jsonify({
                'error': str(e), 
                'is_leaf': False,
                'debug_info': {
                    'image_dimensions': f"{img_width}x{img_height}" if 'img_width' in locals() else "unknown"
                }
            })

if __name__ == '__main__':
    app.run(debug=True)