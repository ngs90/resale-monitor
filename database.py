from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
import datetime 
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()

# session to interact with database
Session = sessionmaker(bind=engine)
session = Session()

class UserSubscription(Base):
    __tablename__ = 'user_subscription'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_psid = Column(String, nullable=False)
    register_datetime = Column(DateTime, default=datetime.datetime.now(datetime.UTC))

class TicketAvailability(Base):
    __tablename__ = 'ticket_availability'
    id = Column(Integer, primary_key=True, autoincrement=True)
    availability_datetime = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    availability = Column(Integer, nullable=False)

# create tables if not exists 
Base.metadata.create_all(engine)




