from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///earthquakes.db', echo=True)


def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
