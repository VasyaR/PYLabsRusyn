from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError
from app.db import db_session
from app.models import Student, Mark, Subject
from flask_bcrypt import Bcrypt

mod = Blueprint('student', __name__, url_prefix='/student')
bcrypt = Bcrypt()

@mod.route('/', methods=['POST'])
def add_student():
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
def get_student(student_id):
    same_id = db_session.query(Student).filter(Student.id == student_id)
    if same_id.count() > 0:
        res = {}
        res["first_name"] = same_id.first().first_name
        res["last_name"] = same_id.first().last_name
        res["university_id"] = same_id.first().university_id
        return jsonify(res), 200
    return jsonify({'message': 'The student was not found'}), 404

@mod.route('/<int:student_id>', methods=['POST'])
def update_student(student_id):
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
def delete_student(student_id):
    same_id = db_session.query(Student).filter(Student.id == student_id)
    if same_id.count() > 0:
        db_session.delete(same_id.first())
        db_session.commit()
        return "", 204
    return jsonify({'message': 'The student was not found'}), 404

@mod.route("/<int:student_id>/rating", methods=['GET'])
def get_student_rating(student_id):
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
    if mark.count() > 0:
        return jsonify({"points": mark.first().points, "teacher_id": mark.first().teacher_id}), 200
    return jsonify({'message': 'The mark was not found'}), 404

@mod.route("/<int:student_id>/subject/<int:subject_id>/points", methods=['POST'])
def update_student_subject_points(student_id, subject_id):
    try:
        class PointSchema(Schema):
            year = fields.Int(required=True)
            semester = fields.Int(required=True)
            points = fields.Int(required=True)
            teacher_id = fields.Int(required=True)
        PointSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    year = request.json.get('year')
    semester = request.json.get('semester')
    if not (db_session.query(Student).filter(Student.id == student_id).count() == 0 or db_session.query(Subject).filter(Subject.id == subject_id).count() == 0):
        mark = db_session.query(Mark).filter(Mark.student_id == student_id, Mark.subject_id == subject_id, Mark.year == year, Mark.semester == semester)
        if mark.count() > 0:
            mark = mark.first()
            mark.points = request.json.get('points')
            mark.teacher_id = request.json.get('teacher_id') # check if teacher is the same(maybe)
        else:
            mark = Mark(student_id = student_id, subject_id = subject_id, year = year, semester = semester, points = request.json['points'], teacher_id = request.json['teacher_id'])
            db_session.add(mark)
        db_session.commit()
        return jsonify("The mark was updated"), 201
    return jsonify({'message': 'The student or the subject was not found'}), 404