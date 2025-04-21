from flask import Blueprint, request, jsonify
from app.models.category import Category
from app.extensions import db

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'description': cat.description,
        'color': cat.color
    } for cat in categories])

@categories_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    if Category.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Category already exists'}), 400
    
    new_category = Category(
        name=data['name'],
        description=data.get('description', ''),
        color=data.get('color', '#FFFFFF')
    )
    
    db.session.add(new_category)
    db.session.commit()
    
    return jsonify({
        'id': new_category.id,
        'name': new_category.name,
        'description': new_category.description,
        'color': new_category.color
    }), 201

@categories_bp.route('/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
def category_operations(category_id):
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'color': category.color
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        if 'name' in data and data['name'] != category.name:
            if Category.query.filter_by(name=data['name']).first():
                return jsonify({'error': 'Category name already exists'}), 400
            category.name = data['name']
        
        if 'description' in data:
            category.description = data['description']
        
        if 'color' in data:
            category.color = data['color']
        
        db.session.commit()
        return jsonify({'message': 'Category updated successfully'})
    
    elif request.method == 'DELETE':
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'})