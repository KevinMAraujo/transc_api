from passlib.context import CryptContext

# Crie um objeto de contexto para criptografia de senha
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criar um hash de senha
def create_password_hash(password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

# Função para verificar uma senha em texto claro com seu hash
def verify_password(plain_password: str, hashed_password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)