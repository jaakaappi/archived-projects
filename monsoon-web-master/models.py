import serial
from datetime import datetime, timedelta
from random import uniform
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, DateTime, String

Base = declarative_base()


class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    plant_name = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime)

    def __init__(self, name, value, timestamp):
        self.plant_name = name
        self.value = value
        self.timestamp = timestamp
