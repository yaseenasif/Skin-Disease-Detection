from app.extensions import db
import datetime

class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    disease_id = db.Column(db.Integer, db.ForeignKey('skin_diseases.id'), nullable=True)
    image_path = db.Column(db.String(255), nullable=False)
    prediction = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    disease = db.relationship('SkinDisease', backref='predictions', lazy=True)
