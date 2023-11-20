import re
from pydantic import BaseModel, validator
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    email: str
    email_verified_at: datetime
    password: str
    remember_token: str
    #created_at = Column('created_at', DateTime, nullable=False)
    #updated_at = Column('updated_at', DateTime, nullable=True)
    role_id: int



    @validator('name')
    def validate_username(cls, value):
        if not re.match('^([a-z]|[0-9]|@)+$', value):
            raise ValueError('Username format invalid')

        return value

class File(BaseModel):
    id: int
    user_id: int
    display_name: str
    file_path: str
    file_name: str
    status: int

class Transcription(BaseModel):
    id: int
    user_id: int
    file_id: int
    name: str
    text: str
    transcribed_at: datetime
    type: int
