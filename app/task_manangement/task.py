from flask import Blueprint, request, jsonify
from ..models import AddTask, db
from ..decorator import auth_required

task_bp = Blueprint('task', __name__)

@task_bp.route('/create_task', methods=['POST'])
@auth_required
def create_task():
    req_json = request.get_json()
    if not req_json:
        return jsonify({'error': 'Request Body cannot be empty'}), 400
    return add_task(req_json)

def add_task(json):
    try:
        find_duplicate = AddTask.query.filter_by(title=json.get('title')).first()
        if find_duplicate:
            return jsonify({'error': 'Task with the same title already exists'}), 400
        new_task = AddTask(
            title=json.get('title'),
            project_id=json.get('project_id'),
            priority=json.get('priority'),
            description=json.get('description'),
            due_date=json.get('due_date'),
            status=json.get('status')
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@task_bp.route('/get_tasks', methods=['GET'])
@auth_required
def get_tasks():
    project_id = request.args.get('project_id')
    if not project_id:
        return jsonify({'error': 'Project ID is required'}), 400
    try:
        all_tasks = AddTask.query.filter_by(project_id=project_id).all()
        if not all_tasks:
            return jsonify({'message': 'No tasks found'}), 200
        tasks_json = [{
            'id': task.id,
            'title': task.title,
            'project_id': task.project_id,
            'priority': task.priority,
            'description': task.description,
            'due_date': task.due_date,
            'status': task.status
        } for task in all_tasks]
        return jsonify({'message': tasks_json}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@task_bp.route('/update_task', methods=['PUT'])
@auth_required
def update_task():
    req_json = request.get_json()
    task_id = request.args.get('task_id')
    if not task_id:
        return jsonify({'error': 'Task ID is required'}), 400
    return update_task_helper(req_json, task_id)

def update_task_helper(json, task_id):
    task_to_update = AddTask.query.get(task_id)
    if not task_to_update:
        return jsonify({'error': 'Task not found'}), 404
    try:
        task_to_update.title = json.get('title', task_to_update.title)
        task_to_update.description = json.get('description', task_to_update.description)
        task_to_update.status = json.get('status', task_to_update.status)
        task_to_update.priority = json.get('priority', task_to_update.priority)
        task_to_update.due_date = json.get('due_date', task_to_update.due_date)
        db.session.commit()
        return jsonify({'message': 'Task updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@task_bp.route('/delete_task', methods=['DELETE'])
@auth_required
def delete_task():
    task_id = request.args.get('task_id')
    if not task_id:
        return jsonify({'error': 'Task ID not provided'}), 400
    task = AddTask.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@task_bp.route('/new', methods=['GET'])
@auth_required
def new():
    return jsonify({'message': 'Task Management System'})