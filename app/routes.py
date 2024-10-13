from flask import request, jsonify, render_template, Blueprint
from app import db
from app.models import Task, Category, User
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('login.html')

@main_bp.route('/todolist', methods=['GET'])
def home_page():
    return render_template('index.html')

@main_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.email)
        return jsonify(access_token=access_token), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@main_bp.route('/api/tasks', methods=['POST'])
@jwt_required()
def add_task():
    data = request.get_json()
    
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    if not data.get('category_id'):
        return jsonify({'error': 'Category is required'}), 400

    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    new_task = Task(
        title=data['title'], 
        category_id=data['category_id'], 
        user_id=user.id
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({
        'message': 'Task added successfully',
        'id': new_task.id,
        'title': new_task.title,
        'category_id': new_task.category_id,
        'user_id': new_task.user_id,
        'completed': new_task.completed
    }), 201

@main_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    if 'completed' in data:
        task.completed = data['completed']
    
    db.session.commit()
    return jsonify({
        'message': 'Task updated successfully',
        'id': task.id,
        'completed': task.completed
    })

@main_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task deleted successfully'})

@main_bp.route('/api/tasks', methods=['GET'])
@jwt_required()
def list_tasks():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404

    tasks = Task.query.filter_by(user_id=user.id).all()
    
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'completed': task.completed,
        'category_id': task.category_id
    } for task in tasks])

@main_bp.route('/api/categories', methods=['GET'])
@jwt_required()
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': category.id,
        'title': category.title,
        'img': category.img
    } for category in categories])

@main_bp.route('/api/categories/<int:category_id>/tasks', methods=['GET'])
@jwt_required()
def tasks_by_category(category_id):
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404

    tasks = Task.query.filter_by(category_id=category_id, user_id=user.id).all()
    
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'completed': task.completed,
        'category_id': task.category_id
    } for task in tasks])
