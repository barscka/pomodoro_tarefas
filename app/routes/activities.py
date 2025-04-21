from flask import Blueprint, request, jsonify
from app.models.activity import Activity
from app.models.category import Category
from app.models.user import User
from app.extensions import db

activities_bp = Blueprint('activities', __name__)

@activities_bp.route('/', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([{
        'id': act.id,
        'name': act.name,
        'description': act.description,
        'duration': act.duration,
        'category_id': act.category_id,
        'user_id': act.user_id,
        'created_at': act.created_at
    } for act in activities])

@activities_bp.route('/', methods=['POST'])
def create_activity():
    data = request.get_json()
    
    required_fields = ['name', 'user_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Verificar se usuário existe
    if not User.query.get(data['user_id']):
        return jsonify({'error': 'User not found'}), 404
    
    # Verificar se categoria existe (se fornecida)
    if 'category_id' in data and not Category.query.get(data['category_id']):
        return jsonify({'error': 'Category not found'}), 404
    
    new_activity = Activity(
        name=data['name'],
        description=data.get('description', ''),
        duration=data.get('duration', 60),
        category_id=data.get('category_id'),
        user_id=data['user_id']
    )
    
    db.session.add(new_activity)
    db.session.commit()
    
    return jsonify({
        'id': new_activity.id,
        'name': new_activity.name,
        'description': new_activity.description,
        'duration': new_activity.duration,
        'category_id': new_activity.category_id,
        'user_id': new_activity.user_id,
        'created_at': new_activity.created_at
    }), 201

@activities_bp.route('/<int:activity_id>', methods=['GET', 'PUT', 'DELETE'])
def activity_operations(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': activity.id,
            'name': activity.name,
            'description': activity.description,
            'duration': activity.duration,
            'category_id': activity.category_id,
            'user_id': activity.user_id,
            'created_at': activity.created_at
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        if 'name' in data:
            activity.name = data['name']
        
        if 'description' in data:
            activity.description = data['description']
        
        if 'duration' in data:
            activity.duration = data['duration']
        
        if 'category_id' in data:
            if not Category.query.get(data['category_id']):
                return jsonify({'error': 'Category not found'}), 404
            activity.category_id = data['category_id']
        
        db.session.commit()
        return jsonify({'message': 'Activity updated successfully'})
    
    elif request.method == 'DELETE':
        db.session.delete(activity)
        db.session.commit()
        return jsonify({'message': 'Activity deleted successfully'})