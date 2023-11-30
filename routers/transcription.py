from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
import os
from pydantic import BaseModel
import database.connection_db as connection_db
from utils.common import transcribe_file
from utils.transcription import TranscriptionUseCases
from utils.schemas import Transcription
from sqlalchemy.orm import Session
from utils.depends import get_db_session

router = APIRouter()


class TranscriptionRequest(BaseModel):
    file_id: str
    model: str
    transcription_id: str

class TranscriptionModel(BaseModel):
    file_id: str
    model: str
    user_id: str
    name: str
@router.get('/transcription')
#async def get_transcription(transcription_request: TranscriptionRequest):
async def get_transcription(
        transcription: Transcription,
        db_session: Session = Depends(get_db_session),
):
    try:
        transc = TranscriptionUseCases(db_session=db_session)
        result = transc.get_transcription(transcription=transcription)
        print('get_transcription OK: ', result )
        return {
            'response': result,
            'status': status.HTTP_200_OK
        }

    except Exception as er:
        raise HTTPException(status_code= 500, detail= f"Erro interno do servidor: {er}")

@router.post('/transcribe_')
async def post_transcribe_(
        transcription: TranscriptionModel,
        db_session: Session = Depends(get_db_session),
):
    try:
        transc = TranscriptionUseCases(db_session=db_session)

        transc.insert_transcription(transcription.user_id, transcription.file_id)


        return JSONResponse(
            content={'msg': 'success'},
            status_code=status.HTTP_201_CREATED
        )
    except Exception as er:
        print(er)
        raise HTTPException(status_code= 500, detail= f" Erro interno do servidor: {er}")

@router.post('/transcribe')
async def post_transcribe(transcription_request: TranscriptionModel):
    try:
        db = connection_db.Connect()
        file_data = db.select_file_by_id(transcription_request.file_id)
        print(file_data)
        if file_data:
            full_filepath = file_data['file_path'] + file_data['file_name']


            print("###: ",full_filepath)
            result = transcribe_file(filepath=full_filepath)
            db = connection_db.Connect()
            db.insert_transcription(file_data['file_id'], user_id=transcription_request.user_id, name=transcription_request.name, transcription_text=result['text'], model=transcription_request.model)

            return result
            '''
            #file_exists = os.path.isfile(full_filepath)
            #if file_exists:
            #else:
                print("Arquivo não encontrado")
                raise HTTPException(status_code=404, detail="Arquivo não encontrado")
            '''
        else:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado no banco de dados")

    except Exception as er:
        print(er)
        raise HTTPException(status_code= 500, detail= f"Erro interno do servidor: {er}")