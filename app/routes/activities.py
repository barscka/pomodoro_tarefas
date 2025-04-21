from datetime import datetime, date
from flask import Blueprint, request, jsonify
from sqlalchemy import func
import random
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
    
    
@activities_bp.route('/random', methods=['GET'])
def get_random_activity():
    today = date.today()
    
    # Consulta para atividades não executadas hoje
    subquery = db.session.query(
        Activity.category_id,
        func.count(Activity.id).label('cat_count')
    ).filter(
        func.date(Activity.last_executed) == today
    ).group_by(
        Activity.category_id
    ).subquery()

    available_activities = Activity.query.filter(
        (func.date(Activity.last_executed) != today) | 
        (Activity.last_executed.is_(None))
    ).outerjoin(
        subquery, Activity.category_id == subquery.c.category_id
    ).filter(
        (subquery.c.cat_count < 2) | 
        (subquery.c.cat_count.is_(None))
    ).all()

    if not available_activities:
        return jsonify({'error': 'No activities available today'}), 404
    print(available_activities)
    selected = random.choice(available_activities)
    
    # Atualiza registro
    selected.last_executed = datetime.now()
    selected.executions_today += 1
    db.session.commit()

    return jsonify({
        'id': selected.id,
        'name': selected.name,
        'duration': 60,
        'preparation_time': 5,
        'category': selected.category.name
    })

@activities_bp.route('/<int:activity_id>/complete', methods=['POST'])
def complete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    
    # Cria registro no histórico
    history = History(
        activity_id=activity.id,
        user_id=1,  # Substituir por current_user.id quando tiver autenticação
        start_time=datetime.now() - timedelta(minutes=65),
        end_time=datetime.now(),
        duration=60,
        notes=request.json.get('notes', '')
    )
    
    db.session.add(history)
    db.session.commit()
    
    return jsonify({
        'message': 'Activity completed successfully',
        'activity_id': activity.id
    })