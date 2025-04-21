from app.extensions import db
from datetime import datetime

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer, default=60)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_executed = db.Column(db.DateTime)  # Data/hora da última execução
    executions_today = db.Column(db.Integer, default=0)  # Contador de execuções hoje
    # Relacionamentos (todos usando back_populates)
    category = db.relationship('Category', back_populates='activities')
    user = db.relationship('User', back_populates='activities')
    schedules = db.relationship('Schedule', back_populates='activity', lazy=True)
    histories = db.relationship('History', back_populates='activity', lazy=True)
    
    def __repr__(self):
        return f'<Activity {self.name}>'