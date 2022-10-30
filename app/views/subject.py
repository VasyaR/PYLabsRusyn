from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError
from app.db import db_session
from app.models import Subject, TeachersSubjects, Mark
from flask_bcrypt import Bcrypt

mod = Blueprint('subject', __name__, url_prefix='/subject')

@mod.route('/', methods=['POST'])
def add_subject():
    try:
        class SubjectSchema(Schema):
            name = fields.Str(required=True)
            teacher_ids = fields.List(fields.Int(), required=True)

        SubjectSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    subject = Subject(name = request.json['name'])
    db_session.add(subject)
    db_session.commit()
    for teacher_id in request.json['teacher_ids']:
        teacher_subject = TeachersSubjects(teacher_id = teacher_id, subject_id = subject.id)
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
def update_subject(subject_id):
    try:
        class SubjectSchema(Schema):
            name = fields.Str(required=True)
            teacher_ids = fields.List(fields.Int(), required=True)

        SubjectSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    same_id = db_session.query(Subject).filter(Subject.id == subject_id)
    if same_id.count() > 0:

        same_id.first().name = request.json['name']
        db_session.commit()
        for teacher_subject in db_session.query(TeachersSubjects).filter(TeachersSubjects.subject_id == subject_id):
            db_session.delete(teacher_subject)
        db_session.commit()
        for teacher_id in request.json['teacher_ids']:
            teacher_subject = TeachersSubjects(teacher_id = teacher_id, subject_id = subject_id)
            db_session.add(teacher_subject)
        db_session.commit()
        return jsonify({'message': 'The subject was updated'}), 200
    return jsonify({'message': 'The subject was not found'}), 404

@mod.route('/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    same_id = db_session.query(Subject).filter(Subject.id == subject_id)
    if same_id.count() > 0:
        db_session.delete(same_id.first())
        db_session.commit()
        return "", 204
    return jsonify({'message': 'The subject was not found'}), 404
