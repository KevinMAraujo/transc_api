from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from database.base import Base

class UserModel(Base):
    __tablename__='users'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column('name', String(50), nullable=False, unique=False)
    email = Column('email', String, nullable=False, unique=True)
    email_verified_at = Column('email_verified_at', DateTime, nullable=True)
    password = Column('password', String, nullable=False, unique=False)
    remember_token = Column('remember_token', String, nullable=True)
    #created_at = Column('created_at', DateTime, nullable=False)
    #updated_at = Column('updated_at', DateTime, nullable=True)
    role_id = Column('role_id', Integer, nullable=False, default=2)

class FileModel(Base):
    __tablename__ = 'files'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column('user_id', Integer, nullable=False)
    display_name = Column('display_name', String(150), nullable=False)

    file_path = Column('file_path', String, nullable=False)
    file_name = Column('file_name', String, nullable=False)
    status = Column('status', Integer, nullable=False, default=0)

class TranscriptionModel(Base):
    __tablename__ = 'transcriptions'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column('user_id', Integer, nullable=False)
    file_id = Column('file_id', Integer, nullable=False)
    name = Column('name', String(150), nullable=False)
    text = Column('text', String, nullable=True)
    transcribed_at = Column('transcribed_at', DateTime, nullable=True)
    type = Column('type', Integer, nullable=False, default=0)

