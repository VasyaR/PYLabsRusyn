from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError
from app.db import db_session
from app.models import Teacher, TeachersSubjects, Subject, University
from flask_bcrypt import Bcrypt
from app import app
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
jwt = JWTManager(app)

mod = Blueprint('teacher', __name__, url_prefix='/teacher')
bcrypt = Bcrypt()

@mod.route('/', methods=['POST'])
@jwt_required()
def add_teacher():
    if get_jwt_identity()["role"] != "admin":
    	return jsonify({'error': 'Not enough permission'}), 403
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
    teacher = Teacher(first_name = request.json['info']['first_name'], last_name = request.json['info']['last_name'], university_id = request.json['info']['university_id'], login = request.json['login'], password = bcrypt.generate_password_hash(request.json['password']).decode('utf8'))
    db_session.add(teacher)
    db_session.commit()
    for subject_id in request.json['info']['subject_ids']:
        teacher_subject = TeachersSubjects(teacher_id = teacher.id, subject_id = subject_id)
        db_session.add(teacher_subject)

    db_session.commit()
    return jsonify(teacher.id), 200

@mod.route('/<int:teacher_id>', methods=['GET'])
@jwt_required()
def get_teacher(teacher_id):
    if get_jwt_identity()["role"] != "admin":
    	if not (get_jwt_identity()["role"] == "teacher" and get_jwt_identity()["id"] == teacher_id):
    		return jsonify({"error": "Not enough permission"}), 403
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
@jwt_required()
def update_teacher(teacher_id):
    if get_jwt_identity()["role"] != "admin":
    	if not (get_jwt_identity()["role"] == "teacher" and get_jwt_identity()["id"] == teacher_id):
    		return jsonify({"error": "Not enough permission"}), 403
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
@jwt_required()
def delete_teacher(teacher_id):
    if get_jwt_identity()["role"] != "admin":
    	return jsonify({'error': 'Not enough permission'}), 403
    same_id = db_session.query(Teacher).filter(Teacher.id == teacher_id)
    if same_id.count() > 0:
        db_session.delete(same_id.first())
        db_session.commit()
        return jsonify("The teacher was deleted"), 200
    return jsonify({'message': 'The teacher was not found'}), 404
    
@mod.route("/login", methods=["POST"])
def login():
	class Teacherinfo(Schema):
		login = fields.Str(required=True)
		password = fields.Str(required=True)
	try:
		if not request.json:
			raise ValidationError('No input data provided')
		Teacherinfo().load(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400
		
	db_teacher = db_session.query(Teacher).filter(Teacher.login == request.json['login']).first()
	if db_teacher is None:
        	return jsonify({'message': 'User not found'}), 404
	
	if not bcrypt.check_password_hash(db_teacher.password, request.json['password']):
        	return jsonify({'message': 'Incorrect password'}), 401
        
	teacher_identity = {"id": db_teacher.id, "role": "teacher"}
	access_token = create_access_token(identity=teacher_identity)
	return jsonify({'token': access_token}), 200
    	
@mod.route('/logout', methods=['GET'])
@jwt_required()
def logout():
	return jsonify({'message': 'Logged out'}), 200
