from flask import request, jsonify
from app import app, db
from app.models import Task
from flask_jwt_extended import jwt_required

@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def add_task():
    data = request.get_json()
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def list_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'status': task.status} for task in tasks])