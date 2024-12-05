from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Prediction
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
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(file_path)

    # Preprocess and predict
    img = image.load_img(file_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])

    predicted_disease = get_disease_info(predicted_class)

    # Save to database
    disease_id = predicted_disease['id']
    new_prediction = Prediction(
        user_id=current_user.id,
        disease_id=disease_id,
        image_path=file_path,
        prediction=predicted_disease['name']
    )
    db.session.add(new_prediction)
    db.session.commit()

    return jsonify({
        'message': 'Prediction successful',
        'disease': predicted_disease,
        'image_path': file_path
    }), 201


def get_disease_info(predicted_class):
    disease = SkinDisease.query.filter_by(id=predicted_class+1).first()
    if disease:
        return {'id': disease.id, 'name': disease.name, 'description': disease.description}
    else:
        return {'id': None, 'name': 'Unknown', 'description': 'No information available'}
