from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError
from app.db import db_session
from app.models import Teacher, TeachersSubjects, Subject, University
from flask_bcrypt import Bcrypt

mod = Blueprint('teacher', __name__, url_prefix='/teacher')
bcrypt = Bcrypt()

@mod.route('/', methods=['POST'])
def add_teacher():
    try:
        class CredentialsSchema(Schema):
            login = fields.Str(required=True)
            password = fields.Str(required=True)
            info = fields.Dict(required=True)
        
        class TeacherSchema(Schema):
            first_name = fields.Str(required=True)
            last_name = fields.Str(required=True)
            university_id = fields.Int(required=True)
            subject_ids = fields.List(fields.Int(), required=True)
        
        CredentialsSchema().load(request.json)
        TeacherSchema().load(request.json["info"])
    except ValidationError as err:
        return jsonify(err.messages), 400
    same_login = db_session.query(Teacher).filter(Teacher.login == request.json['login'])
    uni = db_session.query(University).filter(University.id == request.json["info"]["university_id"])

    if same_login.count() > 0:
        return jsonify({'message': 'Teacher with this login already exists'}), 400
    if uni.count() == 0:
        return jsonify({'message': 'The university was not found'}), 400
    
    q = db_session.query(Subject).filter(Subject.id.in_(request.json['info']['subject_ids']))
    if q.count() != len(request.json['info']['subject_ids']):
        return jsonify({'message': 'Some of the subjects were not found'}), 400
    teacher = Teacher(first_name = request.json['info']['first_name'], last_name = request.json['info']['last_name'], university_id = request.json['info']['university_id'], login = request.json['login'], password = bcrypt.generate_password_hash(request.json['password']))
    db_session.add(teacher)
    db_session.commit()
    for subject_id in request.json['info']['subject_ids']:
        teacher_subject = TeachersSubjects(teacher_id = teacher.id, subject_id = subject_id)
        db_session.add(teacher_subject)

    db_session.commit()
    return jsonify(teacher.id), 200

@mod.route('/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    same_id = db_session.query(Teacher).filter(Teacher.id == teacher_id)
    if same_id.count() > 0:
        return jsonify({
            "first_name": same_id.first().first_name,
            "last_name": same_id.first().last_name,
            "university_id": same_id.first().university_id,
            "subject_ids": [teacher_subject.subject_id for teacher_subject in db_session.query(TeachersSubjects).filter(TeachersSubjects.teacher_id == teacher_id)]
        }), 200
    return jsonify({'message': 'The teacher was not found'}), 404

@mod.route('/<int:teacher_id>', methods=['POST'])
def update_teacher(teacher_id):
    try:
        class TeacherSchema(Schema):
            first_name = fields.Str(required=True)
            last_name = fields.Str(required=True)
            university_id = fields.Int(required=True)
            subject_ids = fields.List(fields.Int(), required=True)
        
        TeacherSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    same_id = db_session.query(Teacher).filter(Teacher.id == teacher_id)
    if same_id.count() > 0:
        uni = db_session.query(University).filter(University.id == request.json['university_id'])
        if uni.count() == 0:
            return jsonify({'message': 'University was not found'}), 404
        q = db_session.query(Subject).filter(Subject.id.in_(request.json['subject_ids']))
        if q.count() != len(request.json['subject_ids']):
            return jsonify({'message': 'Some of the subjects were not found'}), 400
        
        same_id.first().first_name = request.json['first_name']
        same_id.first().last_name = request.json['last_name']
        same_id.first().university_id = request.json['university_id']

        for teacher_subject in db_session.query(TeachersSubjects).filter(TeachersSubjects.teacher_id == teacher_id):
            db_session.delete(teacher_subject)
        for subject_id in request.json['subject_ids']:
            teacher_subject = TeachersSubjects(teacher_id = teacher_id, subject_id = subject_id)
            db_session.add(teacher_subject)
        db_session.commit()
        return jsonify("The teacher was updated"), 201
    return jsonify({'message': 'The teacher was not found'}), 404

@mod.route('/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    same_id = db_session.query(Teacher).filter(Teacher.id == teacher_id)
    if same_id.count() > 0:
        db_session.delete(same_id.first())
        db_session.commit()
        return jsonify("The teacher was deleted"), 200
    return jsonify({'message': 'The teacher was not found'}), 404

@mod.route('/login', methods=['POST'])
def login():
    return jsonify("not implemented"), 501

@mod.route("/logout", methods=['GET'])
def logout():
    return jsonify("not implemented"), 501