from flask import Flask
from database import init_db, db
try:
    from flask_jwt_extended import JWTManager
except Exception:
    # Fallback shim for environments without flask_jwt_extended installed.
    # It provides a minimal interface used by this app (constructor and init_app).
    class JWTManager:
        def __init__(self, app=None):
            if app is not None:
                self.init_app(app)
        def init_app(self, app):
            # no-op fallback; in production install flask_jwt_extended
            setattr(app, '_jwt_manager_shim', True)
import os


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # JWT secret - in production keep this in environment variables
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'change-me-secret')
    # Use same secret for session cookies in UI
    app.secret_key = os.environ.get('SECRET_KEY', app.config['JWT_SECRET_KEY'])

    # Initialize JWT
    jwt = JWTManager(app)

    # Import blueprints (this will import models so SQLAlchemy metadata is populated)
    from routes.users import users_bp
    from routes.registros import registros_bp
    from routes.compras_routes import compras_bp

    # Now initialize DB (create tables) after models have been imported
    init_db(app)

    app.register_blueprint(users_bp)
    app.register_blueprint(registros_bp)
    app.register_blueprint(compras_bp)

    @app.route('/')
    def index():
        return {'status': 'ok', 'message': 'API av2-api-flask'}

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
