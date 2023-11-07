import sqlite3
import os
from passlib.context import CryptContext
from datetime import datetime
from utils.cryptPasswd import create_password_hash, verify_password

class Connect(object):

    def __init__(self, db_file_path: str):
        try:
            # Especifique o caminho para o arquivo do banco de dados SQLite
            db_file_path = './database/database2.db'
            db_exist = os.path.isfile(db_file_path)

            if db_exist:
                print("O arquivo do banco de dados já existe. Conectando ao banco de dados")
            else:
                print("Criando o banco de dados.")

            self.conn = sqlite3.connect(db_file_path)
            self.cursor = self.conn.cursor()

            # imprimindo nome do banco de dados
            print("Database: ", db_file_path)
            # Versao do SQLite
            self.cursor.execute('SELECT SQLITE_VERSION()')
            self.data = self.cursor.fetchone()
            print("SQLite Version: %s" % self.data)

        except sqlite3.Error as er:
            print("Erro ao abrir banco de dados. ", er)

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")

    # Função para inserir um usuário com senha criptografada
    def insert_user(self, username, email, password, fone):
        try:
            hashed_password = create_password_hash(password)

            cursor = self.cursor
            cursor.execute('''
                INSERT INTO Users (username, email, password, fone)
                VALUES (?, ?, ?, ?)
            ''', (username, email, hashed_password, fone))

            self.commit_db()
            return cursor.lastrowid #Retorna o ID do usuario inserido

        except sqlite3.Error as er:
            self.conn.rollback()  # Reverte a transação em caso de erro
            print("Erro ao inserir usuário: ", er)
            return None

    # Função para atualizar informações de um usuário
    def update_user(self, user_id, new_username = '', new_email='', new_password='', new_fone=''):
        '''
        Essa função precisa ser melhorada para atualizar apenas o campo desejado.
        '''
        try:
            hashed_password = ''
            if new_password != '':
                hashed_password = create_password_hash(new_password)

            print('Update User não implementado.')
            return None

            cursor = self.cursor
            cursor.execute('''
                UPDATE Users
                SET username = ?, email = ?, password = ?, fone= ?
                WHERE user_id = ?
            ''', (new_username, new_email, hashed_password, new_fone, user_id) )
            self.commit_db()


        except sqlite3.Error as er:
            self.conn.rollback()
            print("Erro ao atualizar usuário: ", er)
            return None

    # Função para inserir um arquivo de áudio
    def insert_audio_file(self, filename, user_id, file_path):
        try:
            upload_date = datetime.now().date()  # Obtém a data de upload atual
            cursor = self.cursor
            cursor.execute('''
                INSERT INTO Audio_files (filename, user_id, file_path, upload_date)
                VALUES (?, ?, ?, ?)
            ''', (filename, user_id, file_path, upload_date))
            self.commit_db()
            return cursor.lastrowid  # Retorna o ID do arquivo de áudio inserido

        except sqlite3.Error as er:
            self.conn.rollback()  # Reverte a transação em caso de erro
            print(f"Erro ao inserir arquivo de áudio: {er}")
            return None

    # Função para atualizar informações de um arquivo de áudio
    def update_audio_file(self, audio_id, new_filename, new_file_path):
        '''
              Essa função precisa ser melhorada para atualizar apenas o campo desejado.
        '''
        try:
            print('Update Audio não implementado.')
            return None

            cursor = conn.cursor()
            cursor.execute('''
                UPDATE audio_files
                SET filename = ?, file_path = ?
                WHERE audio_id = ?
            ''', (new_filename, new_file_path, audio_id))
            self.commit_db()
            print("Registro de Audio atualizado.")

        except Error as e:
            conn.rollback()  # Reverte a transação em caso de erro
            print(f"Erro ao atualizar arquivo de áudio: {e}")

    # Função para inserir uma transcrição
    def insert_transcription(self, audio_id, transcription_text, model):
        try:
            upload_date = datetime.now().date()  # Obtém a data de upload atual
            cursor = self.cursor
            cursor.execute('''
                INSERT INTO transcriptions (audio_id, transcription_text, transcribed_at, model)
                VALUES (?, ?, ?, ?)
            ''', (audio_id, transcription_text, upload_date, model))
            self.commit_db()
            return cursor.lastrowid  # Retorna o ID da transcrição inserida

        except sqlite3.Error as er:
            self.conn.rollback()  # Reverte a transação em caso de erro
            print(f"Erro ao inserir transcrição: {er}")
            return None

    # Função para atualizar uma transcrição
    def update_transcription(self, transcription_id, new_transcription_text):
        '''
            Essa função precisa ser melhorada para atualizar apenas o campo desejado.
        '''
        try:
            print('Update Transcription não implementado.')
            return None

            cursor = self.cursor
            cursor.execute('''
                UPDATE transcriptions
                SET transcription_text = ?
                WHERE transcription_id = ?
            ''', (new_transcription_text, transcription_id))
            self.commit_db()
            print("Registro de Transcription atualizado.")

        except sqlite3.Error as er:
            conn.rollback()  # Reverte a transação em caso de erro
            print(f"Erro ao atualizar transcrição: {er}")

    # Função para selecionar um usuário pelo ID
    def select_user_by_id(self, user_id):
        try:
            cursor = self.cursor
            cursor.execute('SELECT user_id, username, email, fone FROM Users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()
            if user:
                user_data = {
                    'user_id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'fone': user[3]
                }
                return user_data
            return None
        except sqlite3.Error as er:
            print(f"Erro ao selecionar usuário: {er}")
            return None

    # Função para selecionar um usuário pelo nome de usuário
    def select_user_by_username(self, username):
        try:
            cursor = self.cursor
            cursor.execute('SELECT user_id, username, email, fone FROM Users WHERE username = ?', (username,))
            user = cursor.fetchone()
            if user:
                user_data = {
                    'user_id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'fone': user[3]
                }
                return user_data
            return None
        except sqlite3.Error as er:
            print(f"Erro ao selecionar usuário: {er}")
            return None

    # Função para selecionar um arquivo de áudio pelo ID
    def select_audio_file_by_id(self, audio_id):
        try:
            cursor = self.cursor
            cursor.execute('SELECT audio_id, filename, user_id, file_path, upload_date FROM Audio_files WHERE audio_id = ?', (audio_id,))
            audio_file = cursor.fetchone()
            if audio_file:
                audio_data = {
                    'audio_id': audio_file[0],
                    'filename': audio_file[1],
                    'user_id': audio_file[2],
                    'file_path': audio_file[3],
                    'upload_date': audio_file[4]
                }
                return audio_data
            return None
        except sqlite3.Error as er:
            print(f"Erro ao selecionar arquivo de áudio: {er}")
            return None

    # Função para selecionar todas as transcrições para um arquivo de áudio
    def select_transcriptions_by_audio_id(self, audio_id):
        try:
            cursor = self.cursor
            cursor.execute('SELECT transcription_id, transcription_text, upload_date FROM Transcriptions WHERE audio_id = ?', (audio_id,))
            transcriptions = cursor.fetchall()
            transcription_data = []
            for transcription in transcriptions:
                transcription_data.append({
                    'id': transcription[0],
                    'transcription_text': transcription[1],
                    'upload_date': transcription[2]
                })
            return transcription_data
        except sqlite3.Error as er:
            print(f"Erro ao selecionar transcrições: {er}")
            return []

