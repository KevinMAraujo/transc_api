from fastapi import APIRouter, Depends, HTTPException
import os
from utils.common import transcription_audio

from sqlalchemy.orm import Session
# from database import SessionLocal

from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import whisper
import ffmpeg
from fastapi import Request

template = Jinja2Templates(directory='templates')

import utils.connect_db as connect_db

router = APIRouter()




@router.post("/audio/filepath/{filepath}")
async def audio_filepath(filepath: str):
    result = transcription_audio(filepath=filepath)
    return result

@router.post("/audio/{id}")
async def audio_by_id(id: int):
    pass


@router.post("/audio/")
# def upload_audio(db: Session = Depends(SessionLocal)):
async def upload_audio():
    model_type = 'base'
    interval = ""
    model = whisper.load_model(model_type)

    # result = model.transcribe("./data/audio/audio_1.mp3")
    # return {"text": result['text']}
    result = transcription_audio(filepath='./data/audio/audio_1.mp3')
    return result
