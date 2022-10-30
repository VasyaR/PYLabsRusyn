from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref
from sqlalchemy import * 

Base = declarative_base()
engine = create_engine(url='postgresql+pg8000://postgres:123@localhost:5432/postgres')
Session = sessionmaker(bind=engine)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    university_id = Column(Integer, ForeignKey('universities.id', ondelete='CASCADE'), nullable=False)
    login = Column(String(25), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    university = relationship("University", backref=backref("students", passive_deletes=True))
    

class University(Base):
    __tablename__ = "universities"
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    name = Column(String(60), nullable=False, unique=True)
    address = Column(String(150), nullable=False)

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    university_id = Column(Integer, ForeignKey('universities.id', ondelete='CASCADE'), nullable=False)
    login = Column(String(25), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    university = relationship("University", backref=backref("teachers", passive_deletes=True))

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    
class Mark(Base):
    __tablename__ = "marks"
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    points = Column(Integer, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    year = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)
    student = relationship("Student", backref=backref("marks", passive_deletes=True))
    subject = relationship("Subject", backref=backref("marks", passive_deletes=True))
    teacher = relationship("Teacher", backref=backref("marks", passive_deletes=True))
    
class TeachersSubjects(Base):
    __tablename__ = "teachers_subjects"
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    teacher = relationship("Teacher", backref=backref("teachers_subjects", passive_deletes=True))
    subject = relationship("Subject", backref=backref("teachers_subjects", passive_deletes=True))

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    login = Column(String(25), nullable=False, unique=True)
    password = Column(String(256), nullable=False)