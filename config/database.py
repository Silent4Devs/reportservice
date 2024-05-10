# from sqlalchemy import create_engine, MetaData, text
# from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()  # Load environment variables from .env file

DBHOST = os.getenv("DB_HOST")
DBPORT = os.getenv("DB_PORT")
DBNAME = os.getenv("DB_NAME")
DBUSER = os.getenv("DB_USER")
DBPASS = os.getenv("DB_PASS")

conexion = psycopg2.connect(
    dbname=DBNAME,
    user=DBUSER,
    password=DBPASS,
    host=DBHOST,
    port=DBPORT
)
cursor = conexion.cursor()

# URL_DATABASE = f"postgresql://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}/{DBNAME}"

# engine = create_engine(URL_DATABASE)

# meta = MetaData()

# conn = engine.connect()
