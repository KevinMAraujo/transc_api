from datetime import datetime, timedelta
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import select
from jose import jwt, JWTError
from decouple import config

from database.models import UserModel
from utils.schemas import User


from passlib.context import CryptContext
#import cryptPasswd

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

crypt_context = CryptContext(schemes=['sha256_crypt'])

class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def user_registrer(self, user: User):
        db_user = self.db_session.scalar(select(User).where(User.name == user.name or User.email == user.email))
        #db_user = self.db_session.scalar(select(User).where(User.email == user.email))
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User or email already exists'
            )
        user_model = UserModel(
            #id=
            name=user.name,
            email=user.email,
            email_verified_at = user.email_verified_at,
            password= crypt_context.hash(user.password),
            remember_token = user.remember_token,
            # created_at = Column('created_at', DateTime, nullable=False)
            # updated_at = Column('updated_at', DateTime, nullable=True)
            role_id = user.role_id
        )
        try:


            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists'
            )
        except Exception as er:
            print('##### Error: ', er)


    def user_login(self, user: User, expires_in: int = 30):
        user_on_db = self.db_session.query(UserModel).filter_by(name=user.name).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )

        exp = datetime.utcnow() + timedelta(minutes=expires_in)

        payload = {
            'sub': user.name,
            'exp': exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'exp': exp.isoformat()
        }

    def verify_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )

        user_on_db = self.db_session.query(UserModel).filter_by(name=data['sub']).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'

            )