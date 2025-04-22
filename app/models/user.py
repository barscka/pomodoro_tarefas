from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    today_categories = db.Column(db.JSON, default=list)

    # Relacionamentos (usando back_populates)
    activities = db.relationship('Activity', back_populates='user', lazy=True)
    schedules = db.relationship('Schedule', back_populates='user', lazy=True)
    histories = db.relationship('History', back_populates='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

    def __repr__(self):
        return f'<User {self.username}>'