from app.extensions import db

class SkinDisease(db.Model):
    __tablename__ = 'skin_diseases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    treatment = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<SkinDisease {self.name}>"
