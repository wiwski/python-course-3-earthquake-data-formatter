from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Earthquake(Base):
    __tablename__ = 'earthquakes'
    id = Column(Integer, primary_key=True)
    time=Column(DateTime)
    latitude=Column(Float)
    longitude=Column(Float)
    depth=Column(Float)
    mag=Column(Float)

    def __repr__(self):
       return "<Earthquake({}, {0:.2f}, {0:.2f}>".format(self.time.strftime("%d %b %Y %H:%M:%S"),
                                                         self.latitude,
                                                         self.longitude)

def create_tables(engine):
    Base.metadata.create_all(engine)