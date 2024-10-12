from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(username=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/api/some_protected_route', methods=['GET'])
@jwt_required()
def some_protected_route():
    user_id = get_jwt_identity()
    return jsonify({'message': 'This is a protected route', 'user_id': user_id})
