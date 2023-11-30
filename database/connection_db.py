from decouple import config
from mysql.connector import connect
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime
from utils.cryptPasswd import create_password_hash, verify_password
class Connect(object):

    def __init__(self):
        self.connection = self.bd_connection()
        self.cursor = self.connection.cursor()
        #self.connection.close()

    def bd_connection(self):
        try:
            DATABASE_URL = config('DATABASE_URL')
            DB_USER = config('DB_USER')
            DB_PASSWORD = config('DB_PASSWORD')
            DB_HOST = config('DB_HOST')
            DB_NAME = config('DB_NAME')

            connection = connect(
                host = DB_HOST,
                user = DB_USER,
                passwd = DB_PASSWORD,
                database = DB_NAME
            )
            print("Banco de dados conectado.")
            return connection
        except Error as er:
            if er.errno == errorcode.ER_BAD_DB_ERROR:
                print("Banco de dados inexistente")
            elif er.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(f"Usuário e/ou senha de conexão incorretos. {er.msg}")
            else:
                print(f"Error: {er.msg}")


    def commit_db(self):
        try:
            if self.connection:
                self.connection.commit()
                print('Commit realizado.')
            else:
                print('Não há conexão com o banco.')
        except Error as er:
            print(f"Error: {er.msg}")


    def close_db(self):
        try:
            if self.connection:
                self.connection.close()
                print('Conexão fechada')
            else:
                print("Não a conexão aberta")
        except Error as er:
            print(f"Error: {er.msg}")

    def rollback_db(self):
        print("Não implementado")
        pass

    def execute_db(self):
        print("Não implementado")
        pass




    # Transcription
    # Função para inserir uma transcrição
    def insert_transcription(self, file_id, user_id, name, transcription_text, model):
        try:
            created_date = datetime.now().date()
            '''if self.connection:
                pass'''
            cursor = self.cursor
            sql = "INSERT INTO transcriptions (file_id, user_id, name, text, type, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (file_id, user_id, name, transcription_text, model, created_date)
            cursor.execute(sql, values)
            print("\n")
            print(cursor.rowcount, " registros inseridos.")
            print("\n")
            self.commit_db()

        except Error as er:
            #self.rollback_db()
            print(f"Erro ao inserir transcrição (BD): {er}")


        except Exception as er:
            print(f"Erro ao inserir transcricao: {er}")

    def select_transcription_by_file_id(self, file_id):
        try:
            pass
        except Exception as er:

            print(f"Erro ao selecionar a transcrição: {er}")


    # Usuarios
    def insert_user(self, username, email):
        pass

    def select_user_by_id(self, user_id):
        try:
            cursor = self.cursor
            sql = 'SELECT used_id, name, username, email, fone FROM users WHERE user_id = ?'
            values = (user_id)
            cursor.execute(sql, values)
            user = cursor.fetchone()
            if user:
                user_data = {
                    'user_id': user[0],
                    'name': user[1],
                    'username': user[2],
                    'email': user[3],
                }
                return user_data
            else:
                return None
        except Error as er:
            print(f"Erro ao selecionar usuarios (BD): {er}")
            return None

        except Exception as er:
            print(f"Erro ao selecionar usuario: {er}")
            return None

    # Files
    def select_file_by_id(self, file_id):
        try:
            cursor = self.cursor
            #sql = "SELECT file_id,filename, user_id, file_path, upload_date FROM files WHERE file_id = ?"
            sql = "SELECT id as file_id, user_id, display_name, file_path, file_name, status, created_at, updated_at FROM files WHERE id = %s"
            values = (file_id)
            print('Aqui')
            cursor.execute(f"SELECT id as file_id, user_id, display_name, file_path, file_name, status, created_at, updated_at FROM files WHERE id = {file_id}")

            file = cursor.fetchone()

            if file:
                file_data = {
                    'file_id': file[0],
                    'user_id': file[1],
                    'display_name': file[2],
                    'file_path': file[3],
                    'file_name': file[4],
                    'status': file[5],
                    'created_at': file[6],
                    'upload_date': file[7],
                }
                return file_data

            else:
                return None

        except Exception as er:
            print(f"Error: {er}")
            return None