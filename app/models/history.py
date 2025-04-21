from app.extensions import db
from datetime import datetime

class History(db.Model):
    __tablename__ = 'histories'
    
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # Em minutos
    notes = db.Column(db.Text)
    
    activity = db.relationship('Activity', back_populates='histories')
    user = db.relationship('User', back_populates='histories')
    
    def __repr__(self):
        return f'<History {self.id} of {self.activity_id}>'