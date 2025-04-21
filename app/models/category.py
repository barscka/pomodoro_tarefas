from app.extensions import db

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#FFFFFF')
    
    # Relacionamento com Activity (usando back_populates)
    activities = db.relationship('Activity', back_populates='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'