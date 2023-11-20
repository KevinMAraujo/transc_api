import os
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import  datetime
from fastapi.exceptions import HTTPException
from fastapi import status
from database.models import TranscriptionModel
from utils.schemas import Transcription
from utils.common import transcribe_file

from utils.schemas import File
from database.models import FileModel
from utils.files import FileUseCases


class TranscriptionUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_transcription(self, transcription: Transcription):

        transc_on_db = self.db_session.query(TranscriptionModel).filter_by(file_id=transcription.file_id).first()

        if transc_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        try:


            return transc_on_db

        except Exception as er:
            print("ERROR: ", er)
    def insert_transcription(self, transcription: Transcription):
        transcription_model = TranscriptionModel(
            user_id=transcription.user_id,
            file_id=transcription.file_id,
            name=transcription.name,
            text=transcription.text,
            transcribed_at=datetime.utcnow(),
            type=transcription.type
        )
        try:

            file_data = self.db_session.query(FileModel).filter_by(id=transcription_model.file_id).first()
            if file_data is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Arquivo não encontrado'
                )
            print(file_data)

            if file_data:
                full_filepath = file_data.file_path + '/' + file_data.file_name
                print('### full_filepath: ', full_filepath)
                file_exists = os.path.isfile(full_filepath)

                if file_exists:
                    result = transcribe_file(filepath=full_filepath)
                    print(f'### Result {result}')
                    transcription_model.text = result
                    self.db_session.add(transcription_model)
                    self.db_session.commit()

                    return f'Registro Inserido: {result}'

                else:
                    print("Arquivo não encontrado")
                    raise HTTPException(status_code=404, detail="Arquivo não encontrado")


        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Transcription already exists'
            )
    def update_transcription(self, transcription: Transcription):
        pass
    '''def get_items(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Item).offset(skip).limit(limit).all()'''