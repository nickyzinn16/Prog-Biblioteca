import mysql.connector

db_host = "localhost"
db_user = "root"
db_password = ""
db_name = "biblioteca_db"

def connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

conexao = connection()
cursor = conexao.cursor()