import config
from flask import Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "troll"
app.config["SQLALCHEMY_DATABASE_STR"] = "postgresql://admin:admin@localhost/pp" 
if config.is_testing:
    app.config["SQLALCHEMY_DATABASE_STR"] = 'sqlite:///test.db' 
from app.views import admin
from app.views import student
from app.views import teacher
from app.views import subject
from app.views import university
app.register_blueprint(admin.mod)
app.register_blueprint(student.mod)
app.register_blueprint(teacher.mod)
app.register_blueprint(subject.mod)
app.register_blueprint(university.mod)
