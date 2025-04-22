from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id if hasattr(user, 'id') else user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    from app.models.user import User
    identity = jwt_data["sub"]
    return User.query.get(identity)