from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from models import *
import pg8000


def loadSession():
    engine = create_engine("postgresql+pg8000://postgres:123@localhost:5432/postgres", echo=True)
    
    metadata = MetaData(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

if __name__ == "__main__":
    session = loadSession()

    university = Universities(name='Lviv Polytechnic', address='Stepana Bandery Street, 12, Lviv, Lviv region, 79000')
    student = Students(first_name='Oleksandr', last_name='Yovbak', university_id=1, login='probablyskela', password='1232143')
    student2 = Students(first_name='Oleksandr', last_name='Yovbak', university_id=1, login='probablyskela', password='1232143')
    student3 = Students(first_name='Oleksandr', last_name='Yovbak', university_id=1, login='probablyskela', password='1232143')
    teacher = Teachers(first_name='Oleg', last_name='Skip', university_id=1, login='olegskip', password='123')

    session.add(university)
    session.commit()

    session.add(student)
    session.add(student2)
    session.add(student3)
    session.commit()

    session.add(teacher)
    session.commit()
    subject = Subjects(name = 'Math')
    session.add(subject)
    session.commit() # 123
    mark = Marks(student_id = 1, teacher_id = 1, subject_id=1, mark = 5)
    session.add(mark)
    session.commit()
    res = session.query(Marks).all()