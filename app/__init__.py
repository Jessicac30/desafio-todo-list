from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import redis

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    r = redis.Redis(host='localhost', port=6379, db=0)

    with app.app_context():
        from app.auth import auth_bp
        app.register_blueprint(auth_bp)

        from app.routes import main_bp
        app.register_blueprint(main_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
