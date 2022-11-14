from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError
from app.db import db_session
from app.models import Student, Mark, Subject, University, TeachersSubjects
from flask_bcrypt import Bcrypt
from app import app
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
jwt = JWTManager(app)

mod = Blueprint('student', __name__, url_prefix='/student')
bcrypt = Bcrypt()

@mod.route('/', methods=['POST'])
@jwt_required()
def add_student():
    if get_jwt_identity()["role"] != "admin":
    	return jsonify({'error': 'Not enough permission'}), 403
    try:
        class CredentialsSchema(Schema):
            login = fields.Str(required=True)
            password = fields.Str(required=True)
            info = fields.Dict(required=True)
        class StudentSchema(Schema):
            first_name = fields.Str(required=True)
            last_name = fields.Str(required=True)
            university_id = fields.Int(required=True)

        CredentialsSchema().load(request.json)
        StudentSchema().load(request.json["info"])
    except ValidationError as err:
        return jsonify(err.messages), 400
    same_login = db_session.query(Student).filter(Student.login == request.json['login'])
    uni = db_session.query(University).filter(University.id == request.json["info"]["university_id"])
    if same_login.count() > 0:
        return jsonify({'message': 'Student with this login already exists'}), 400
    if uni.count() == 0:
        return jsonify({'message': 'University with this id does not exist'}), 400
    student = Student(login = request.json['login'], password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'), **request.json["info"])
    db_session.add(student)
    db_session.commit()
    return jsonify(student.id), 200

@mod.route('/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    if get_jwt_identity()["role"] != "admin":
    	if not (get_jwt_identity()["role"] == "student" and get_jwt_identity()["id"] == student_id):
    		return jsonify({"error": "Not enough permission"}), 403
    same_id = db_session.query(Student).filter(Student.id == student_id)
    if same_id.count() > 0:
        res = {}
        res["first_name"] = same_id.first().first_name
        res["last_name"] = same_id.first().last_name
        res["university_id"] = same_id.first().university_id
        return jsonify(res), 200
    return jsonify({'message': 'The student was not found'}), 404

@mod.route('/<int:student_id>', methods=['POST'])
@jwt_required()
def update_student(student_id):
    if get_jwt_identity()["role"] != "admin":
    	if not (get_jwt_identity()["role"] == "student" and get_jwt_identity()["id"] == student_id):
    		return jsonify({"error": "Not enough permission"}), 403
    try:
        class StudentPasswordSchema(Schema):
            password = fields.Str(required=True)
        
        StudentPasswordSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    same_id = db_session.query(Student).filter(Student.id == student_id)
    if same_id.count() > 0:
        same_id.first().password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        db_session.commit()
        return jsonify("The student was updated"), 201
    return jsonify({'message': 'The student was not found'}), 404

@mod.route('/<int:student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    if get_jwt_identity()["role"] != "admin":
    	return jsonify({'error': 'Not enough permission'}), 403
    same_id = db_session.query(Student).filter(Student.id == student_id)
    if same_id.count() > 0:
        db_session.delete(same_id.first())
        db_session.commit()
        return "", 204
    return jsonify({'message': 'The student was not found'}), 404

@mod.route("/<int:student_id>/rating", methods=['GET'])
@jwt_required()
def get_student_rating(student_id):
    if get_jwt_identity()["role"] != "admin":
    	if not (get_jwt_identity()["role"] == "student" and get_jwt_identity()["id"] == student_id):
    		return jsonify({"error": "Not enough permission"}), 403
    try:
        class DateSchema(Schema):
            year = fields.Int(required=True)
            semester = fields.Int(required=True)
        DateSchema().load(request.args)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if db_session.query(Student).filter(Student.id == student_id).count():
        year = int(request.args.get('year'))
        semester = int(request.args.get('semester'))
        marks = db_session.query(Mark).filter(Mark.student_id == student_id, Mark.year == year, Mark.semester == semester)
        res = []
        for mark in marks:
            res.append({
                "subject_id": mark.subject_id,
                "points": mark.points
            })
        return jsonify({"subjects": res}), 200
    return jsonify({'message': 'The student was not found'}), 404

@mod.route("/<int:student_id>/subject/<int:subject_id>/points", methods=['GET'])
@jwt_required()
def get_student_subject(student_id, subject_id):
    try:
        class DateSchema(Schema):
            year = fields.Int(required=True)
            semester = fields.Int(required=True)
        DateSchema().load(request.args)
    except ValidationError as err:
        return jsonify(err.messages), 400
    year = int(request.args.get('year'))
    semester = int(request.args.get('semester'))
    mark = db_session.query(Mark).filter(Mark.student_id == student_id, Mark.subject_id == subject_id, Mark.year == year, Mark.semester == semester)
    print("zxc")
    print(get_jwt_identity()["id"])
    if mark.count() > 0:
        if get_jwt_identity()["role"] != "admin":
            if not (get_jwt_identity()["role"] == "student" and get_jwt_identity()["id"] == student_id):
                if not (get_jwt_identity()["role"] == "teacher" and get_jwt_identity()["id"] == mark.first().teacher_id):
                    return jsonify({"error": "Not enough permission"}), 403
        return jsonify({"points": mark.first().points, "teacher_id": mark.first().teacher_id}), 200
    return jsonify({'message': 'The mark was not found'}), 404

@mod.route("/<int:student_id>/subject/<int:subject_id>/points", methods=['POST'])
@jwt_required()
def update_student_subject_points(student_id, subject_id):
    try:
        class PointSchema(Schema):
            year = fields.Int(required=True)
            semester = fields.Int(required=True)
            points = fields.Int(required=True)
        PointSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    year = request.json.get('year')
    semester = request.json.get('semester')
    if not (db_session.query(Student).filter(Student.id == student_id).count() == 0 or db_session.query(Subject).filter(Subject.id == subject_id).count() == 0):
        if get_jwt_identity()["role"] == "student" or get_jwt_identity()["role"] == "admin":
            return jsonify({"error": "Not enough permission"}), 403
        if get_jwt_identity()["role"] == "teacher":
            access_check_for_teacher = db_session.query(TeachersSubjects).filter(TeachersSubjects.subject_id == subject_id, TeachersSubjects.teacher_id == get_jwt_identity()["id"]).first()
            if access_check_for_teacher is None:
                return jsonify({"error": "Not enough permission"}), 403
        mark = db_session.query(Mark).filter(Mark.student_id == student_id, Mark.subject_id == subject_id, Mark.year == year, Mark.semester == semester)
        if mark.count() > 0:	
            mark = mark.first()
            mark.points = request.json.get('points')
            mark.teacher_id = get_jwt_identity()["id"] # check if teacher is the same(maybe)
        else:
            mark = Mark(student_id = student_id, subject_id = subject_id, year = year, semester = semester, points = request.json['points'], teacher_id = get_jwt_identity()["id"])
            db_session.add(mark)
        db_session.commit()
        return jsonify("The mark was updated"), 201
    return jsonify({'message': 'The student or the subject was not found'}), 404
    
@mod.route("/login", methods=["POST"])
def login():
	class Studentinfo(Schema):
		login = fields.Str(required=True)
		password = fields.Str(required=True)
	try:
		if not request.json:
			raise ValidationError('No input data provided')
		Studentinfo().load(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400
		
	db_student = db_session.query(Student).filter(Student.login == request.json['login']).first()
	if db_student is None:
        	return jsonify({'message': 'User not found'}), 404
	
	if not bcrypt.check_password_hash(db_student.password, request.json['password']):
        	return jsonify({'message': 'Incorrect password'}), 401
        
	student_identity = {"id": db_student.id, "role": "student"}
	access_token = create_access_token(identity=student_identity)
	return jsonify({'token': access_token}), 200
    	
@mod.route('/logout', methods=['GET'])
@jwt_required()
def logout():
	return jsonify({'message': 'Logged out'}), 200
    	
