from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from app.models import *
from app import app
import config

engine = create_engine(app.config['SQLALCHEMY_DATABASE_STR'], echo=False)
metadata = Base.metadata
Session = sessionmaker(bind=engine)
db_session = Session()

if config.is_testing:
    metadata.drop_all(engine)
    metadata.create_all(engine)
