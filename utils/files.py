from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import  datetime
from fastapi.exceptions import HTTPException
from fastapi import status
from database.models import FileModel
from utils.schemas import File



class FileUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def get_file_by_id(self, file: File):
        file_on_db = self.db_session.query(FileModel).filter_by(id=file.id).first()

        if file_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Arquivo não encontrado'
            )
        try:
            return file_on_db
        except Exception as er:
            print("ERROR: ", er)