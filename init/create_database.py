import sqlite3
import os

'''if __name__ == '__main__':
    from .'''
class Connect(object):

    def __init__(self, db_file_path: str):
        try:
            # Especifique o caminho para o arquivo do banco de dados SQLite
            db_file_path="../database/database2.db"
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

            if db_exist:
                print('#### Banco de dados ja existente. As tabelas não serão recriadas.')
            else:
                print("#### Criando a estrutura de tabelas do banco de dados")
                self.create_users_table()
                self.create_audio_table()
                self.create_transcription_table()

        except sqlite3.Error as er:
            print("Erro ao abrir banco de dados. ", er)

    # Função para criar a tabela de usuários
    def create_users_table(self):
        try:
            cursor = self.cursor
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    fone TEXT
                )
            ''')
            self.commit_db()

        except sqlite3.Error as e:
            print(f"Erro ao criar a tabela de usuários: {e}")

    # Função para criar a tabela de arquivos de áudio
    def create_audio_table(self):
        try:
            cursor = self.cursor
            cursor.execute('''
                 CREATE TABLE IF NOT EXISTS Audio_files (
                    audio_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT,
                    filename TEXT NOT NULL,
                    user_id INTEGER NOT NULL,                    
                    upload_date DATE,
                    status TEXT,
                    FOREIGN KEY (user_id) REFERENCES Users(user_id)

                )
             ''')
            self.commit_db()
        except sqlite3.Error as e:
            print(f"Erro ao criar a tabela de audio: {e}")

    # Função para criar a tabela de transcrições
    def create_transcription_table(self):
        try:
            cursor = self.cursor
            cursor.execute('''
                 CREATE TABLE IF NOT EXISTS Transcriptions (
                     transcriptions_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     audio_id INTEGER NOT NULL,
                     transcription_text TEXT NOT NULL,
                     transcribed_at DATE,
                     model TEXT NOT NULL,
                     FOREIGN KEY (audio_id) REFERENCES Audio_files(audio_id)
                 )
             ''')
            self.commit_db()

        except sqlite3.Error as e:
            print(f"Erro ao criar a tabela de transcrições: {e}")

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")

