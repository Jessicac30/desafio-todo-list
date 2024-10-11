from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    print("Database tables created.")

def create_user():
    username = 'jess@gmail.com'
    password = '123'
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()
    print('User created successfully!')

if __name__ == '__main__':
    create_user()