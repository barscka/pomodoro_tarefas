from flask import Blueprint, jsonify, request
from app.extensions import db  # Importe db do extensions
from app.models.activity import Activity  # Importe diretamente o modelo

bp = Blueprint('activities', __name__, url_prefix='/api/activities')

@bp.route('/', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'duration': a.duration
    } for a in activities])