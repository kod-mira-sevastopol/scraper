import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

Base = declarative_base()

from src.modal.models import Config
def create_session():
    db_url = os.getenv("DATABASE_URL_LOCAL")
    engine = create_engine(db_url)
    engine.connect()
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    return Session()


create_session()


def get_config(session):
    result = session.query(Config).filter_by(id=1).first()
    print(f"{result=}")
    return result


def set_config(session, expires_at, expires_in, access_token):
    config = session.query(Config).filter_by(id=1).first()
    print(config)
    config.expires_at = expires_at
    config.expires_in = expires_in
    config.access_token = access_token
    session.commit()
    return config