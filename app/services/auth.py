from datetime import datetime, timedelta, timezone
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.extensions import db

class AuthService:
    @staticmethod
    def register(username, email, password):
        # Verifica se o usuário já existe
        if User.query.filter_by(email=email).first():
            return {'message': 'Email already registered'}, 400
        
        # Cria o novo usuário
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return {'message': 'User created successfully'}, 201

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return {'message': 'Invalid credentials'}, 401
        
        # Cria os tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, 200

    @staticmethod
    def refresh_token(identity):
        new_token = create_access_token(identity=identity)
        return {'access_token': new_token}, 200