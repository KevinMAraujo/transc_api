from fastapi import APIRouter, Depends, HTTPException
import os
from utils.common import transcription_audio
from pydantic import BaseModel
import utils.connect_db as connect_db

# from sqlalchemy.orm import Session
# from database import SessionLocal
# from fastapi.templating import Jinja2Templates
# template = Jinja2Templates(directory='templates')

router = APIRouter()


class TranscriptionRequest(BaseModel):
    audio_id: str
    model: str
    transcription_id: str


@router.get('/transcription_by_audio_id/{audio_id}')
async def get_transcription_by_audio_id(audio_id: str):
    pass


@router.get('/transcription_by_audio_id')
async def get_transcription_by_audio_id2(transcription_request: TranscriptionRequest):
    pass


@router.get('/transcription_by_transcription_id/{transcription_id}')
async def get_transcription_by_transcription_id(transcription_id: str):
    pass


@router.get('/transcription_by_transcription_id')
async def get_transcription_by_transcription_id(transcription_request: TranscriptionRequest):
    pass


@router.post('/transcribe_audio/{audio_id}')
async def transcribe_audio_by_id(audio_id: str):
    try:
        db = connect_db.Connect('')
        audio_data = db.select_audio_file_by_id(audio_id)
        if audio_data:
            audio_full_filepath = audio_data['file_path'] + '\\' + audio_data['filename']
            audio_file_exist = os.path.isfile(audio_full_filepath)

            if audio_file_exist:
                result = transcription_audio(filepath=audio_full_filepath)
                db.insert_transcription(audio_data['audio_id'], result['text'], 'base')
                return result
            else:
                raise HTTPException(status_code=404, detail="Arquivo de áudio não encontrado")

        else:
            raise HTTPException(status_code=404, detail="Arquivo de áudio não encontrado")

    except Exception as er:
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")


@router.post('/transcribe_audio')
async def transcribe_audio(transcription_request: TranscriptionRequest):
    try:
        db = connect_db.Connect('')
        audio_data = db.select_audio_file_by_id(transcription_request.audio_id)
        if audio_data:
            audio_full_filepath = audio_data['file_path'] + '\\' + audio_data['filename']
            audio_file_exist = os.path.isfile(audio_full_filepath)

            if audio_file_exist:
                result = transcription_audio(filepath=audio_full_filepath)
                db.insert_transcription(audio_data['audio_id'], result['text'], transcription_request.model)
                return result
            else:
                raise HTTPException(status_code=404, detail="Arquivo de áudio não encontrado")

        else:
            raise HTTPException(status_code=404, detail="Arquivo de áudio não encontrado")

    except Exception as er:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
