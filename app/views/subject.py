from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError
from app.db import db_session
from app.models import Subject, TeachersSubjects, Mark, Teacher
from flask_bcrypt import Bcrypt
from app import app
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
jwt = JWTManager(app)

mod = Blueprint('teacher', __name__, url_prefix='/teacher')
bcrypt = Bcrypt()

mod = Blueprint('subject', __name__, url_prefix='/subject')

@mod.route('/', methods=['POST'])
@jwt_required()
def add_subject():
    if get_jwt_identity()["role"] != "admin":
        return jsonify({'error': 'Not enough permission'}), 403
    try:
        class SubjectSchema(Schema):
            name = fields.Str(required=True)
            teacher_ids = fields.List(fields.Int(), required=True)

        SubjectSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    same_name = db_session.query(Subject).filter(Subject.name == request.json['name'])
    if same_name.count() > 0:
        return jsonify({'message': 'Subject with this name already exists'}), 400

    subject = Subject(name = request.json['name'])
    

    q = db_session.query(Teacher).filter(Teacher.id.in_(request.json['teacher_ids']))
    if q.count() != len(request.json['teacher_ids']):
        return jsonify({'message': 'Some of the teachers were not found'}), 400
        
    db_session.add(subject)
    for teacher in q:
        teacher_subject = TeachersSubjects(teacher_id = teacher.id, subject_id = subject.id)
        db_session.add(teacher_subject)
    
    db_session.commit()
    return jsonify(subject.id), 200

@mod.route('/<int:subject_id>', methods=['GET'])
def get_subject(subject_id):
    same_id = db_session.query(Subject).filter(Subject.id == subject_id)
    if same_id.count() > 0:
        return jsonify({
            "name": same_id.first().name,
            "teacher_ids": [teacher_subject.teacher_id for teacher_subject in db_session.query(TeachersSubjects).filter(TeachersSubjects.subject_id == subject_id)]
        }), 200
    return jsonify({'message': 'The subject was not found'}), 404

@mod.route('/<int:subject_id>', methods=['POST'])
@jwt_required()
def update_subject(subject_id):
    if get_jwt_identity()["role"] != "admin":
        return jsonify({'error': 'Not enough permission'}), 403
    try:
        class SubjectSchema(Schema):
            name = fields.Str(required=True)
            teacher_ids = fields.List(fields.Int(), required=True)

        SubjectSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    same_id = db_session.query(Subject).filter(Subject.id == subject_id)
    if same_id.count() > 0:
        if request.json['name'] != same_id.first().name:
            same_name = db_session.query(Subject).filter(Subject.name == request.json['name'])
            if same_name.count() > 0:
                return jsonify({'message': 'Subject with this name already exists'}), 400
        
        same_id.first().name = request.json['name']

        q = db_session.query(Teacher).filter(Teacher.id.in_(request.json['teacher_ids']))
        if q.count() != len(request.json['teacher_ids']):
            return jsonify({'message': 'Some of the teachers were not found'}), 400
        
        for teacher_subject in db_session.query(TeachersSubjects).filter(TeachersSubjects.subject_id == subject_id):
            db_session.delete(teacher_subject)

        for teacher_id in request.json['teacher_ids']:
            teacher_subject = TeachersSubjects(teacher_id = teacher_id, subject_id = subject_id)
            db_session.add(teacher_subject)
        db_session.commit()
        return jsonify({'message': 'The subject was updated'}), 200
    return jsonify({'message': 'The subject was not found'}), 404

@mod.route('/<int:subject_id>', methods=['DELETE'])
@jwt_required()
def delete_subject(subject_id):
    if get_jwt_identity()["role"] != "admin":
        return jsonify({'error': 'Not enough permission'}), 403
    same_id = db_session.query(Subject).filter(Subject.id == subject_id)
    if same_id.count() > 0:
        db_session.delete(same_id.first())
        db_session.commit()
        return "", 204
    return jsonify({'message': 'The subject was not found'}), 404
