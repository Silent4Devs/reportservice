from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from routes.reports import reports
from dashboards import dash

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()
app.title = os.getenv("APP_NAME")
app.version = os.getenv("APP_VERSION")

app.include_router(reports)
app.include_router(dash)

# tags=["Home"] es una etiqueta que se le asigna a la ruta para poder agruparla en la documentación


@app.get('/', tags=["Home"])
def message():
    return {"Hello World!"}


@app.get('/movies', tags=["Movies"])
def movies():
    return JSONResponse(content={"message": "movies"})
