from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Prediction, SkinDisease
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
import uuid
import numpy as np

predict_bp = Blueprint('predict_bp', __name__)

# Load your .keras model (adjust the path as needed)
model = load_model('app/trained_models/efficientNet_model.keras')

# Folder to save uploaded images
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@predict_bp.route('/predict', methods=['POST'])
@login_required
def predict_skin_disease():
    try:
        # Check if file is present in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        # Check if the file has a valid name
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Generate a unique filename and save the file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        try:
            file.save(file_path)
        except Exception as e:
            return jsonify({'error': 'Failed to save the file', 'details': str(e)}), 500

        # Preprocess the image
        try:
            img = image.load_img(file_path, target_size=(224, 224))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
        except Exception as e:
            return jsonify({'error': 'Failed to preprocess the image', 'details': str(e)}), 500

        # Predict the disease
        try:
            predictions = model.predict(img_array)
            predicted_class = np.argmax(predictions[0])
            predicted_disease = get_disease_info(predicted_class)
        except Exception as e:
            return jsonify({'error': 'Model prediction failed', 'details': str(e)}), 500

        # Save the prediction to the database
        try:
            disease_id = predicted_disease['id']
            new_prediction = Prediction(
                user_id=current_user.id,
                disease_id=disease_id,
                image_path=file_path,
                prediction=predicted_disease['name']
            )
            db.session.add(new_prediction)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Rollback the transaction on error
            return jsonify({'error': 'Failed to save prediction to the database', 'details': str(e)}), 500

        # Return the prediction result
        return jsonify({'disease': predicted_disease}), 201

    except Exception as e:
        # Catch-all for unexpected errors
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


def get_disease_info(predicted_class):
    disease = SkinDisease.query.filter_by(id=predicted_class + 1).first()
    if disease:
        return {'id': disease.id, 'name': disease.name, 'description': disease.description, 'treatment': disease.treatment}
    else:
        return {'id': None, 'name': 'Unknown', 'description': 'No information available', 'treatment': 'NA'}


@predict_bp.route('/predictions', methods=['GET'])
@login_required
def get_user_predictions():
    """
    Retrieve all predictions for the currently logged-in user.
    """
    predictions = Prediction.query.filter_by(user_id=current_user.id).all()

    if not predictions:
        return jsonify({'message': 'No predictions found for this user'}), 404

    result = []
    for pred in predictions:
        disease_info = {
            'id': pred.disease.id if pred.disease else None,
            'name': pred.disease.name if pred.disease else 'Unknown',
            'description': pred.disease.description if pred.disease else 'No information available'
        }
        result.append({
            'id': pred.id,
            'image_path': pred.image_path,
            'prediction': pred.prediction,
            'created_at': pred.created_at,
            'disease': disease_info
        })

    return jsonify(result), 200
