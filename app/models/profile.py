from app import db

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.String(500))
    gender = db.Column(db.String(6))
    phone = db.Column(db.String(15))
    location = db.Column(db.String(500))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), unique=True, nullable=False)

    def __init__(self, first_name, last_name, bio, gender, phone,location,user_id):
        self.first_name=first_name,
        self.last_name=last_name,
        self.bio = bio
        self.gender = gender
        self.phone = phone
        self.location = location
        self.user_id=user_id

    def __repr__(self):
        return f'<Profile of User {self.user.username}>'