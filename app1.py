import os
from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2
import base64
from PIL import Image
from io import BytesIO

# Set environment variable to disable OneDNN optimizations to avoid warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = Flask(__name__)

# Load the model
model = load_model("grape_model.h5")
# Compile the model to address the warning about metrics
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

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

def detect_fruit(image_path):
    """
    Detect if the image contains fruit-like structures based on color and shape.
    Returns: (is_fruit, message)
    """
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        return False, "Could not read image file"
    
    # Convert to different color spaces for better analysis
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Fruit color ranges in HSV
    fruit_color_ranges = [
        # Red (like apples, strawberries) - need 2 ranges because red wraps around in HSV
        (np.array([0, 70, 50]), np.array([10, 255, 255])),
        (np.array([170, 70, 50]), np.array([180, 255, 255])),
        # Orange (like oranges, peaches)
        (np.array([10, 70, 50]), np.array([30, 255, 255])),
        # Yellow (like lemons, bananas)
        (np.array([25, 50, 50]), np.array([35, 255, 255])),
        # Purple (like plums, grapes)
        (np.array([130, 30, 30]), np.array([160, 255, 255])),
    ]
    
    combined_fruit_mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    
    # Combine all fruit color masks
    for color_range in fruit_color_ranges:
        if len(color_range) == 2:  # Normal range
            lower_bound, upper_bound = color_range
            color_mask = cv2.inRange(hsv, lower_bound, upper_bound)
            combined_fruit_mask = cv2.bitwise_or(combined_fruit_mask, color_mask)
    
    # Calculate percentage of fruit-colored pixels
    fruit_color_percentage = np.sum(combined_fruit_mask > 0) / (combined_fruit_mask.shape[0] * combined_fruit_mask.shape[1])
    
    # Convert to grayscale for shape detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use thresholding to create binary image
    _, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)
    
    # Find contours for shape analysis
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Look for circular/oval shapes (common in fruits)
    circular_shapes = 0
    total_area = img.shape[0] * img.shape[1]
    
    for contour in contours:
        # Filter small contours
        if cv2.contourArea(contour) < total_area * 0.05:
            continue
            
        # Calculate circularity
        perimeter = cv2.arcLength(contour, True)
        area = cv2.contourArea(contour)
        if perimeter > 0:
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            
            # Circles have circularity close to 1
            if 0.6 < circularity < 1.4:
                circular_shapes += 1
                
                # Check if this circular shape has fruit colors
                mask = np.zeros(gray.shape, np.uint8)
                cv2.drawContours(mask, [contour], 0, 255, -1)
                fruit_colored_pixels = cv2.bitwise_and(mask, combined_fruit_mask)
                fruit_color_in_circle = np.sum(fruit_colored_pixels > 0) / max(1, np.sum(mask > 0))
                
                # If circular shape with high fruit color content
                if fruit_color_in_circle > 0.3 and fruit_color_percentage > 0.15:
                    return True, "The image appears to contain fruit-like structure with typical fruit colors"
    
    # High concentration of fruit colors without clear circular shape might still be fruit
    if fruit_color_percentage > 0.4:
        # Check texture - fruits often have smoother texture than leaves
        texture_variance = np.var(blurred)
        if texture_variance < 1000:  # Smoother textures have lower variance
            return True, "The image contains a high concentration of fruit colors with smooth texture"
    
    return False, "No fruit-like structures detected"

def is_grape_leaf_image(image_path):
    """
    Modified function to detect grape leaves specifically.
    First checks if the image contains fruit.
    """
    # First check if image contains fruits
    is_fruit, fruit_message = detect_fruit(image_path)
    if is_fruit:
        return False, fruit_message
    
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

def detect_grape_disease_features(image_path):
    """
    Extract disease-specific features from grape leaf images to improve classification accuracy.
    Returns dictionary of disease-specific feature measurements.
    """
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Could not read image file"}
    
    # Convert to different color spaces
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Disease-specific color ranges
    # Black Rot: reddish-brown spots
    black_rot_ranges = [
        # Reddish-brown spots
        (np.array([0, 50, 50]), np.array([15, 255, 200])),  # Red
        (np.array([160, 50, 50]), np.array([180, 255, 200])),  # Red (wrapped)
        (np.array([10, 50, 20]), np.array([30, 200, 150]))   # Brown
    ]
    
    # Leaf Blight: yellowish-brown areas
    leaf_blight_ranges = [
        (np.array([20, 30, 50]), np.array([40, 255, 255])),  # Yellow
        (np.array([10, 40, 40]), np.array([30, 200, 150]))   # Brown-Yellow
    ]
    
    # ESCA: yellowish patches with dark borders
    esca_ranges = [
        (np.array([15, 30, 50]), np.array([35, 180, 220])),  # Yellow patches
        (np.array([0, 0, 0]), np.array([180, 50, 100]))      # Dark edges
    ]
    
    # Calculate disease feature percentages
    features = {}
    
    # Black Rot features
    black_rot_mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    for lower, upper in black_rot_ranges:
        mask = cv2.inRange(hsv, lower, upper)
        black_rot_mask = cv2.bitwise_or(black_rot_mask, mask)
    
    # Count spots (connected components)
    contours, _ = cv2.findContours(black_rot_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    small_spots = [c for c in contours if 10 < cv2.contourArea(c) < 500]  # Typical size for black rot spots
    
    features['black_rot_spot_count'] = len(small_spots)
    features['black_rot_color_percentage'] = np.sum(black_rot_mask > 0) / (black_rot_mask.shape[0] * black_rot_mask.shape[1])
    
    # Leaf Blight features 
    leaf_blight_mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    for lower, upper in leaf_blight_ranges:
        mask = cv2.inRange(hsv, lower, upper)
        leaf_blight_mask = cv2.bitwise_or(leaf_blight_mask, mask)
    
    features['leaf_blight_color_percentage'] = np.sum(leaf_blight_mask > 0) / (leaf_blight_mask.shape[0] * leaf_blight_mask.shape[1])
    
    # ESCA features
    esca_mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    for lower, upper in esca_ranges:
        mask = cv2.inRange(hsv, lower, upper)
        esca_mask = cv2.bitwise_or(esca_mask, mask)
    
    features['esca_color_percentage'] = np.sum(esca_mask > 0) / (esca_mask.shape[0] * esca_mask.shape[1])
    
    # Calculate texture features using L channel of LAB color space
    l_channel = lab[:,:,0]
    l_blur = cv2.GaussianBlur(l_channel, (5, 5), 0)
    texture_variance = np.var(l_blur)
    features['texture_variance'] = texture_variance
    
    # Edge density features (relevant for vein and spot patterns)
    edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 50, 150)
    features['edge_density'] = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
    
    # Green health percentage (healthy leaf typically has more green)
    green_mask = cv2.inRange(hsv, np.array([35, 30, 30]), np.array([85, 255, 255]))
    features['green_percentage'] = np.sum(green_mask > 0) / (green_mask.shape[0] * green_mask.shape[1])
    
    return features

def predict_with_ensemble(image_path, model, class_names):
    """
    Use ensemble prediction with slight variations of the input image to improve accuracy.
    """
    # Original prediction
    orig_img = preprocess_image(image_path)
    orig_pred = model.predict(orig_img)[0]
    
    # Extract disease-specific features
    disease_features = detect_grape_disease_features(image_path)
    
    # Load the image for augmentation
    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Could not read image file"}
    
    augmented_images = []
    # Slight rotation
    for angle in [-5, 5]:
        h, w = img.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)
        temp_path = os.path.join(os.path.dirname(image_path), f"temp_rot_{angle}.jpg")
        cv2.imwrite(temp_path, rotated)
        augmented_images.append(preprocess_image(temp_path))
        os.remove(temp_path)  # Clean up temp file
    
    # Slight brightness adjustment
    for alpha in [0.9, 1.1]:  # Darker and brighter
        adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=0)
        temp_path = os.path.join(os.path.dirname(image_path), f"temp_bright_{alpha}.jpg")
        cv2.imwrite(temp_path, adjusted)
        augmented_images.append(preprocess_image(temp_path))
        os.remove(temp_path)  # Clean up temp file

    # Get predictions for all augmented images
    all_preds = [orig_pred]
    for aug_img in augmented_images:
        pred = model.predict(aug_img)[0]
        all_preds.append(pred)
    
    # Average the predictions
    avg_pred = np.mean(all_preds, axis=0)
    
    # Apply feature-based boosting for specific diseases
    # If we detect strong visual features for certain diseases, boost their probability
    if disease_features['black_rot_spot_count'] > 20 and disease_features['black_rot_color_percentage'] > 0.05:
        # Boost Black Rot probability
        black_rot_idx = class_names.index('Black Rot')
        avg_pred[black_rot_idx] *= 1.2  # 20% boost
    
    if disease_features['leaf_blight_color_percentage'] > 0.1 and disease_features['green_percentage'] < 0.5:
        # Boost Leaf Blight probability
        leaf_blight_idx = class_names.index('Leaf Blight')
        avg_pred[leaf_blight_idx] *= 1.15  # 15% boost
    
    if disease_features['esca_color_percentage'] > 0.1 and disease_features['texture_variance'] > 500:
        # Boost ESCA probability
        esca_idx = class_names.index('ESCA')
        avg_pred[esca_idx] *= 1.15  # 15% boost
    
    # Normalize predictions to sum to 1
    avg_pred = avg_pred / np.sum(avg_pred)
    
    # Get the predicted class
    predicted_class_index = np.argmax(avg_pred)
    predicted_disease = class_names[predicted_class_index]
    confidence = float(avg_pred[predicted_class_index])
    
    return {
        'prediction': predicted_disease,
        'confidence': confidence,
        'probabilities': [float(p) for p in avg_pred],
        'features': disease_features
    }

def save_base64_image(base64_data, upload_folder):
    """
    Decode base64 image data and save it to a file
    """
    # Strip the base64 prefix if present
    if "," in base64_data:
        base64_data = base64_data.split(",")[1]
    
    # Decode base64 data
    image_data = base64.b64decode(base64_data)
    
    # Generate a unique filename
    filename = f"camera_capture_{os.urandom(4).hex()}.jpg"
    filepath = os.path.join(upload_folder, filename)
    
    # Save the image
    with open(filepath, "wb") as f:
        f.write(image_data)
    
    return filepath

@app.route('/')
def index():
    return render_template('index.html', diseases=class_names)

@app.route('/predict', methods=['POST'])
def predict():
    # Check if request contains a file upload or base64 image data
    if 'file' in request.files:
        # Handle file upload
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file', 'is_leaf': False})
        
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
        
    elif 'image_data' in request.form:
        # Handle camera capture (base64 encoded image)
        try:
            base64_data = request.form['image_data']
            filepath = save_base64_image(base64_data, app.config['UPLOAD_FOLDER'])
        except Exception as e:
            return jsonify({
                'error': f'Error processing camera image: {str(e)}',
                'is_leaf': False
            })
    else:
        return jsonify({'error': 'No image provided (neither file upload nor camera capture)', 'is_leaf': False})
    
    # Debug: Save original image dimensions
    original_img = cv2.imread(filepath)
    if original_img is None:
        return jsonify({
            'error': 'Could not read image file',
            'is_leaf': False
        })
    
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
    
    # Predict using ensemble approach
    try:
        prediction_result = predict_with_ensemble(filepath, model, class_names)
        
        if 'error' in prediction_result:
            return jsonify({
                'error': prediction_result['error'], 
                'is_leaf': True
            })
        
        predicted_disease = prediction_result['prediction']
        confidence = prediction_result['confidence']
        
        # If the confidence is too low
        if confidence < 0.4:
            result = {
                'prediction': 'Unrecognized',
                'confidence': confidence,
                'message': 'This grape leaf image could not be classified with confidence. It may not be one of the supported leaf types.',
                'is_leaf': True,
                'debug_info': {
                    'image_dimensions': f"{img_width}x{img_height}",
                    'probabilities': prediction_result['probabilities'],
                    'features': prediction_result['features']
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
                    'probabilities': prediction_result['probabilities'],
                    'features': prediction_result['features']
                }
            }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': str(e), 
            'is_leaf': True,
            'debug_info': {
                'image_dimensions': f"{img_width}x{img_height}" if 'img_width' in locals() else "unknown"
            }
        })

# Optional route to test camera functionality
@app.route('/camera-test', methods=['GET'])
def camera_test():
    return render_template('camera.html')

if __name__ == '__main__':
    app.run(debug=True)