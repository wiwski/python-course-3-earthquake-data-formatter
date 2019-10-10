from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint

Base = declarative_base()


class Earthquake(Base):
    __tablename__ = 'earthquakes'
    id = Column(Integer, primary_key=True)
    time=Column(DateTime)
    latitude=Column(Float)
    longitude=Column(Float)
    depth=Column(Float)
    mag=Column(Float)
    __table_args__ = (UniqueConstraint('time', 'latitude', 'longitude'),)

    def __repr__(self):
       return "<Earthquake(id={0},{1:s}, {2:.2f}, {3:.2f}>".format(self.id,
                                                                   self.time.strftime("%d %b %Y %H:%M:%S"),
                                                                   self.latitude,
                                                                   self.longitude)


def create_tables(engine):
    Base.metadata.create_all(engine)
