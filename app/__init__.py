from flask import Flask, render_template
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
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    r = redis.Redis(host='localhost', port=6379, db=0)

    with app.app_context():
        from app.auth import auth_bp
        from app.models import User, Task
        app.register_blueprint(auth_bp)

        @app.route('/')
        def index():
            return render_template('index.html')

    return app