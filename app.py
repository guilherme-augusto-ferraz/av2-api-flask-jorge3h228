from flask import Flask
from database import init_db, db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    from routes.users import users_bp
    from routes.registros import registros_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(registros_bp)

    @app.route('/')
    def index():
        return {'status': 'ok', 'message': 'API av2-api-flask'}

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
