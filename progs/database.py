import mysql.connector

db_host = "127.0.0.1"
db_user = "root"
db_password = "root"
db_name = "biblioteca_db"

def connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        port=3306
    )

conexao = connection()
cursor = conexao.cursor()