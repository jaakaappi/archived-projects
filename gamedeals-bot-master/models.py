from sqlalchemy import Column, ForeignKey, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True)
    datetime_registered = Column(DateTime, nullable=False)


class LogEntry(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    channel_id = Column(Integer, ForeignKey('channel.id'))
    channel = relationship(Channel)
    level = Column(Integer, nullable=False, default=1)
    message = Column(String, nullable=False)


engine = create_engine('sqlite:///db.db')
Base.metadata.create_all(engine)


def drop_and_create_all():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)
