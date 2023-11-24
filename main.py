from fastapi import FastAPI
from routers import transcription, users #,files
from database.connection import Session

app = FastAPI()
app.include_router(transcription.router)
app.include_router(users.user_router)
app.include_router(users.test_router)

@app.get('/')
async def health_check():
    return "Ok"

@app.get('/check_database')
async def check_database():
    try:
        #SessionLocal
        Session
        print("**** Conectado ao banco de dados.")
        return ("**** Conectado ao banco de dados.")
    except Exception as er:
        print(" #### Erro de conexão com o banco de dados: \n", er)
        return None
