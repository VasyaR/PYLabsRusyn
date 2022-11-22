from sqlalchemy import func
from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError
from app.db import db_session
from app.models import University, Mark, Student
from flask_bcrypt import Bcrypt
from app import app
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
jwt = JWTManager(app)
bcrypt = Bcrypt()

mod = Blueprint('university', __name__, url_prefix='/university')

@mod.route('/', methods=['POST'])
@jwt_required()
def add_university():
    if get_jwt_identity()["role"] != "admin":
        return jsonify({'error': 'Not enough permission'}), 403
    try:
        class UniversitySchema(Schema):
            name = fields.Str(required=True)
            address = fields.Str(required=True)

        UniversitySchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    same_name = db_session.query(University).filter(University.name == request.json['name'])
    if same_name.count() > 0:
        return jsonify({'message': 'University with this name already exists'}), 400
    university = University(name = request.json['name'], address = request.json['address'])
    db_session.add(university)
    db_session.commit()
    return jsonify(university.id), 200

@mod.route('/', methods=['GET'])
def get_universities():
    universities = db_session.query(University).all()
    res = []
    for university in universities:
        res.append({
            'id': university.id,
            "name": university.name,
            "address": university.address
        })
    return jsonify(res), 200

@mod.route('/<int:university_id>', methods=['POST'])
@jwt_required()
def update_university(university_id):
    if get_jwt_identity()["role"] != "admin":
        return jsonify({'error': 'Not enough permission'}), 403
    try:
        class UniversitySchema(Schema):
            name = fields.Str(required=True)
            address = fields.Str(required=True)

        UniversitySchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    same_id = db_session.query(University).filter(University.id == university_id)
    if same_id.count() > 0:
        same_id.first().name = request.json['name']
        same_id.first().address = request.json['address']
        db_session.commit()
        return jsonify("The university was updated"), 201
    return jsonify({'message': 'The university was not found'}), 404

@mod.route('/<int:university_id>', methods=['DELETE'])
@jwt_required()
def delete_university(university_id):
    if get_jwt_identity()["role"] != "admin":
        return jsonify({'error': 'Not enough permission'}), 403
    same_id = db_session.query(University).filter(University.id == university_id)
    if same_id.count() > 0:
        db_session.delete(same_id.first())
        db_session.commit()
        return "", 204
    return jsonify({'message': 'The university was not found'}), 404

@mod.route('/<int:university_id>/rating', methods=['GET'])
def get_university_rating(university_id):
    try:
        class DateSchema(Schema):
            year = fields.Int(required=True)
            semester = fields.Int(required=True)
        DateSchema().load(request.args)
    except ValidationError as err:
        return jsonify(err.messages), 400
    same_id = db_session.query(University).filter(University.id == university_id)
    if same_id.count() > 0:
        rows = db_session.query(func.avg(Mark.points), Student).\
            join(Mark).group_by(Student.id).\
                filter(Student.university_id == university_id).\
                    filter(Mark.year == int(request.args['year'])).\
                        filter(Mark.semester == int(request.args['semester'])).all()
        res = []
        for row in rows:
            res.append({
                'points': row[0],
                'student': {
                    'first_name': row[1].first_name,
                    'last_name': row[1].last_name,
                    'university_id': row[1].university_id
                },
                'student_id': row[1].id
            })
        return jsonify({"rating": res}), 200
    return jsonify({'message': 'The university was not found'}), 404
