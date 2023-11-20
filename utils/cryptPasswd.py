from passlib.context import CryptContext
from decouple import config
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

#schemes='sha256_crypt'
#schemes='bcrypt'

# Função para criar um hash de senha
def create_password_hash(password: str):
    #CryptContext(schemes=['sha256_crypt'])
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

# Função para verificar uma senha em texto claro com seu hash
def verify_password(plain_password: str, hashed_password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], depreacted="auto")
    return pwd_context.verify(plain_password, hashed_password)