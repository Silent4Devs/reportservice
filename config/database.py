# from sqlalchemy import create_engine, MetaData, text
# from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv,find_dotenv
import psycopg2
import os

load_dotenv(find_dotenv())  # Load environment variables from .env file

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_conexion():
    try:
        conexion = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conexion
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None


conexion = get_conexion()
if conexion is not None:
    cursor = conexion.cursor()
    # Ahora puedes usar el cursor para ejecutar consultas
else:
    print("No se pudo establecer la conexión a la base de datos.")

# URL_DATABASE = f"postgresql://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}/{DBNAME}"

# engine = create_engine(URL_DATABASE)

# meta = MetaData()

# conn = engine.connect()
