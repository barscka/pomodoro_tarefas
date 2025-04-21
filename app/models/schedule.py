from app.extensions import db
from datetime import datetime

class Schedule(db.Model):
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    scheduled_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos (usando back_populates)
    activity = db.relationship('Activity', back_populates='schedules')
    user = db.relationship('User', back_populates='schedules')
    
    def __repr__(self):
        return f'<Schedule {self.id} for {self.scheduled_date}>'