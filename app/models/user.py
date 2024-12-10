import datetime
from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    profile = db.relationship('Profile', backref='user', uselist=False, lazy=True)

    def __init__(self, email, username, password,created_date):
        self.email = email
        self.username = username
        self.password = password
        self.created_date = created_date

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
        }

    def __repr__(self):
        return f'<User {self.username}>'
    
    def is_active(self):
        return True
    
    def is_logged_in(self):
        return self.id
    
    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id