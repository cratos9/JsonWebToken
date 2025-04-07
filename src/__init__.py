from flask import Flask
from src.databases.conection import db
import os
from dotenv import load_dotenv
from src.routes.index import bp as index_bp
from src.routes.authentication_user import bp as auth_bp

load_dotenv()

def create_app():
    
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite',
        DEBUG=os.getenv('DEBUG')
    )
    
    db.init_app(app)
    
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    
    with app.app_context():
        db.create_all()
    
    return app