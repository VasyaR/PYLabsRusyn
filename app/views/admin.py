from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError
from app.db import db_session
from app.models import Admin
from flask_bcrypt import Bcrypt

mod = Blueprint('admin', __name__, url_prefix='/admin')
bcrypt = Bcrypt()

@mod.route('/', methods=['POST'])
def add_admin():
    try:
        class CredentialsSchema(Schema):
            login = fields.Str(required=True)
            password = fields.Str(required=True)
        
        CredentialsSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    same_login = db_session.query(Admin).filter(Admin.login == request.json['login'])
    if same_login.count() > 0:
        return jsonify({'message': 'Admin with this login already exists'}), 400
    admin = Admin(login = request.json['login'], password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'))
    db_session.add(admin)
    db_session.commit()
    return jsonify(admin.id), 200

@mod.route('/<int:admin_id>', methods=['POST'])
def update_admin(admin_id):
    try:
        class AdminPasswordSchema(Schema):
            password = fields.Str(required=True)
        
        AdminPasswordSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    same_id = db_session.query(Admin).filter(Admin.id == admin_id)
    if same_id.count() > 0:
        same_id.first().password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        db_session.commit()
        return jsonify("The admin was updated"), 201
    return jsonify({'message': 'The admin was not found'}), 404

@mod.route('/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    same_id = db_session.query(Admin).filter(Admin.id == admin_id)
    if same_id.count() > 0:
        db_session.delete(same_id.first())
        db_session.commit()
        return "", 204
    return jsonify({'message': 'The admin was not found'}), 404

@mod.route('/login', methods=['POST'])
def login():
    return jsonify("not implemented")

@mod.route('/logout', methods=['GET'])
def logout():
    return jsonify("not implemented")