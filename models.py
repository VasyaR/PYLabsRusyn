from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import * 

Base = declarative_base()
engine = create_engine(url='postgresql+pg8000://postgres:123@localhost:5432/postgres')
Session = sessionmaker(bind=engine)

class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    login = Column(String(25), nullable=False)
    password = Column(String(256), nullable=False)

class Universities(Base):
    __tablename__ = "universities"
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    name = Column(String(60), nullable=False)
    address = Column(String(150), nullable=False)

class Teachers(Base):
    __tablename__ = "teachers"
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    login = Column(String(25), nullable=False)
    password = Column(String(256), nullable=False)

class Subjects(Base):
    __tablename__ = "subjects"
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    
class Marks(Base):
    __tablename__ = "marks"
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    mark = Column(Integer, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    
class TeachersSubjects(Base):
    __tablename__ = "teachers_subjects"
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)