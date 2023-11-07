import sqlite3


def createDatabase():
    pass


def connection(database: str):
    try:
        con = sqlite3.connect(database)
        return con
    except sqlite3.Error as ex:
        print(ex)


def consult(con, sql):
    cursor = con.cursor()
    cursor.execute(sql)
    dados = cursor().fetchall()
    return dados


# caminho = "./database/database1.db"
# conexao = connection(caminho)

'''from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import DeclarativeBase
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql://user:password@localhost/mydatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

#Base = DeclarativeBase()
'''
