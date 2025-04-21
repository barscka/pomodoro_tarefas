from flask import Blueprint
from app.routes.auth import auth_bp
from app.routes.categories import categories_bp
from app.routes.activities import activities_bp

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(auth_bp, url_prefix='/auth')
api_bp.register_blueprint(categories_bp, url_prefix='/categories')
api_bp.register_blueprint(activities_bp, url_prefix='/activities')