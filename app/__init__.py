from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configure CORS
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

    app.config.from_object('config.Config')
    if 'SECRET_KEY' not in app.config:
        raise ValueError("SECRET_KEY not found in config")
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY')

    jwt = JWTManager(app)
    db.init_app(app)
    migrate.init_app(app, db)

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
            response.headers.add("Access-Control-Allow-Headers", "*")
            response.headers.add("Access-Control-Allow-Methods", "*")
            return response

    with app.app_context():
        from .routes import main as main_blueprint
        from .task_manangement.task import task_bp
        from .project_management.project import project_bp

        app.register_blueprint(main_blueprint)
        app.register_blueprint(task_bp, url_prefix='/task')
        app.register_blueprint(project_bp, url_prefix='/project')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)