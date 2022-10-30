from flask import Flask
app = Flask(__name__)

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