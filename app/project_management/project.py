from flask import Blueprint, jsonify, request
from ..models import Project, db
from ..decorator import auth_required
import datetime
project_bp = Blueprint('project', __name__)

@project_bp.route('/', methods=['GET', 'POSt', 'PUT'])
@auth_required
def project_management():
    req_json = request.get_json()
    user_id = request.args.get('user_id')
    if request.method == 'GET':
        projects = Project.query.filter_by(user_id=user_id).all()
        project_list = []
        for project in projects:
            project_list.append({
                'id': project.id,
                'title': project.title,
                'created_at': project.created_at,
                'user_id' : user_id
            })
        return jsonify({'project_list': project_list}), 200

    if request.method == 'POST':
        project = Project.query.filter_by(title=req_json['title']).first()
        if project:
            return jsonify({'message': 'Project with this title already exists'}), 400
        new_project = Project(user_id=user_id, title=req_json['title'], created_at=datetime.datetime.now())
        db.session.add(new_project)
        db.session.commit()
        return jsonify({'message': 'Project created successfully'}), 201


@project_bp.route('/remove_project')
@auth_required
def remove_project():
    pass 