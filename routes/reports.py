from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.database import cursor
import pandas as pd
import psycopg2
reports = APIRouter()


@reports.get('/empleados', tags=["ReportsXls"])
def getEmpleados():
    return {"message": "empleados"}

# Corrected route name to match the SQL query route


@reports.get('/getUsers', tags=["ReportsXls"])
def retrieve_all_item():
    query = "SELECT * FROM ussers"

    resultados = ejecutar_consulta_sql(cursor, query)
    exportar_a_excel(resultados, "reportsfile/empleados/users.xlsx")


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
    exportar_a_excel(
        resultados, "reportsfile/empleados/empleadosPuestos.xlsx")


def ejecutar_consulta_sql(cursor, consulta):
    try:
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        return resultados
    except psycopg2.Error as e:
        print("Error al ejecutar la consulta SQL:", e)
        return JSONResponse(content={"message": "Error al ejecutar la consulta SQL."})


def exportar_a_excel(resultados, nombre_archivo):
    try:
        if resultados is not None:
            df = pd.DataFrame(resultados, columns=[
                desc[0] for desc in cursor.description])
            df.to_excel(nombre_archivo, index=False)
            print("Resultados exportados a", nombre_archivo)
    except Exception as e:
        print("No se pudieron exportar los resultados a Excel debido a un error.")
        return JSONResponse(content={"message": "Error al ejecutar la consulta SQL."})
