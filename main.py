from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from dotenv import load_dotenv
import os
from routes.reports import reports,app,repo_fil
from routes.dashboards import dash

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.title = os.getenv("APP_NAME")
app.version = os.getenv("APP_VERSION")

app.include_router(reports)
app.include_router(repo_fil, prefix="/repo_fil")
app.include_router(dash, prefix="/dash")

# tags=["Home"] es una etiqueta que se le asigna a la ruta para poder agruparla en la documentación


@app.get('/', tags=["Home"])
def message():
    return {"Hello World!"}


@dash.post('/dash', tags=["Dashboards"])
def dashboards():
    return JSONResponse(content={"message": "Dashboards"})

@app.post('/', tags=["ReportsXls"])
def read_root():
    return {"message": "Hi"}
