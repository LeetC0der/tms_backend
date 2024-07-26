from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    app.config.from_object('config.Config')
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY')
    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .routes import main as main_blueprint
        from .task_manangement.task import task_bp
        from .project_management.project import project_bp 
        app.register_blueprint(main_blueprint)
        app.register_blueprint(task_bp, url_prefix='/task')
        app.register_blueprint(project_bp, url_prefix='/project')
        db.create_all()

    return app

app = create_app()