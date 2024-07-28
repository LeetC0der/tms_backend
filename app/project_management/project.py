from flask import Blueprint, jsonify, request
from ..models import Project, db
from ..decorator import auth_required
import datetime
from flask_cors import cross_origin

project_bp = Blueprint('project', __name__)

@project_bp.route('/get_projects', methods=['GET'])
@auth_required
def get_projects():
    user_id = request.args.get('user_id')
    projects = Project.query.filter_by(user_id=user_id).all()
    project_list = [{'id': project.id, 'title': project.title, 'created_at': project.created_at, 'user_id': user_id} for project in projects]
    return jsonify({'project_list': project_list}), 200

@project_bp.route('/create_project', methods=['POST'])
@auth_required
def create_project():
    req_json = request.get_json()
    user_id = request.args.get('user_id')
    project = Project.query.filter_by(title=req_json['title']).first()
    if project:
        return jsonify({'message': 'Project title already exists, Try new one.'}), 400
    new_project = Project(user_id=user_id, title=req_json['title'], created_at=datetime.datetime.now())
    db.session.add(new_project)
    db.session.commit()
    return jsonify({'message': 'Project created successfully'}), 201

@project_bp.route('/remove_project', methods=['DELETE'])
@auth_required
def remove_project():
    # implement delete logic here
    pass