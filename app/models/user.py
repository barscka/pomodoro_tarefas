from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relacionamentos (usando back_populates)
    activities = db.relationship('Activity', back_populates='user', lazy=True)
    schedules = db.relationship('Schedule', back_populates='user', lazy=True)
    histories = db.relationship('History', back_populates='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'