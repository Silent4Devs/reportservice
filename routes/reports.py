from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse
from config.database import cursor
import pandas as pd
import psycopg2
from pathlib import Path
from fastapi import HTTPException
from datetime import date
from datetime import datetime
import os

reports = APIRouter()

DirectoryEmpleados = "reportsfile/administracion/empleados/"

# Validar si la carpeta ya existe
if not os.path.exists(DirectoryEmpleados):
    # Si no existe, crear la carpeta
    os.makedirs(DirectoryEmpleados)

now = date.today()

@reports.get('/empleados', tags=["ReportsXls"])
def getEmpleados():
    return {"message": "empleados"}

# Corrected route name to match the SQL query route


@reports.get('/getUsers', tags=["ReportsXls"])
def retrieve_all_item():
    query = "SELECT name, email, created_at, n_empleado FROM users"
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "users" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)


# Corrected route name to match the SQL query route
@reports.get('/empleadosPuestos', tags=["ReportsXls"])
def getEmpleadosPuestos():
    query = """
            SELECT
                e.name AS empleado,
                s.name AS supervisor,
                a.area AS area,
                p.puesto AS puesto
            FROM
                empleados e
                LEFT JOIN empleados s ON e.supervisor_id=s.id
                INNER JOIN areas a ON e.area_id=a.id
                INNER JOIN puestos p ON e.puesto_id =p.id
            WHERE
                e.deleted_at IS NULL AND e.estatus='alta'
            ORDER BY
                empleado ASC;
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "empleadosPuestos" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)


def ejecutar_consulta_sql(cursor, consulta):
    try:
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        return resultados
    except psycopg2.Error as e:
        print("Error al ejecutar la consulta SQL:" + str(e))
        # return JSONResponse(content={"message": "Error al ejecutar la consulta SQL."})
        raise HTTPException(
            status_code=500, detail="Error executing SQL query: " + str(e))


def exportar_a_excel(resultados, nombre_archivo):
    try:
        if resultados is not None:
            df = pd.DataFrame(resultados, columns=[
                desc[0] for desc in cursor.description])
            df.to_excel(nombre_archivo, index=False)
            print("Resultados exportados a", nombre_archivo)
    except Exception as e:
        print("No se pudieron exportar los resultados a Excel debido a un error." + str(e))
        raise HTTPException(
            status_code=500, detail="Report error: " + str(e))
