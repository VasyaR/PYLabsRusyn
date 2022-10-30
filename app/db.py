from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from app.models import *
import pg8000


engine = create_engine("postgresql+pg8000://postgres:123456@localhost:5432/postgres", echo=True)

metadata = MetaData(engine)
Session = sessionmaker(bind=engine)
db_session = Session()
