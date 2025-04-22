from flask import Flask
from app.routes.api import api_bp

from dotenv import load_dotenv
import os
from app.extensions import db, migrate, jwt
# Registre blueprints (importe dentro da função para evitar circular imports)
from app.routes.main_routes import bp as main_bp
from app.routes.activities import activities_bp
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Inicialize extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app