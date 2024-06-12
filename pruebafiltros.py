##Para probar usar:
## uvicorn pruebafiltros:app --reload --port 8001

import pandas as pd
from fastapi.responses import JSONResponse, FileResponse
from config.database import cursor
import psycopg2
from pathlib import Path
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
from datetime import date, datetime
import os

app = FastAPI()

DirectoryEmpleados = "reportsfile/administracion/empleados/"

## Timesheet proyectos

@app.get('/timesheetProyectosFiltros', tags=["ReportsXls"])
def get_timesheet_proyectos(
    id: Optional[str] = Query(None, description="Área de los proyectos"),     
    proyecto: Optional[int] = Query(None, description="ID del proyecto"),     
    fechainicio: Optional[datetime] = Query(None, description="Fecha de inicio en formato YYYY-MM-DD"), 
    fechafin: Optional[datetime] = Query(None, description="Fecha de fin en formato YYYY-MM-DD")
):     
    query = """         
        SELECT         
            tp.proyecto AS "ID-Proyecto",         
            STRING_AGG(DISTINCT a.area, ', ') AS "Áreas participantes",         
            STRING_AGG(DISTINCT e.name, ', ') AS "Empleados participantes",        
            tc.nombre AS "Cliente" 
        FROM timesheet_proyectos tp         
        LEFT JOIN timesheet_proyectos_empleados tpe ON tp.id = tpe.proyecto_id         
        LEFT JOIN timesheet_proyectos_areas tpa ON tp.id = tpe.proyecto_id         
        LEFT JOIN areas a ON tpe.area_id = a.id           
        LEFT JOIN empleados e ON tpe.empleado_id = e.id         
        RIGHT JOIN timesheet_clientes tc ON tp.cliente_id = tc.id
    """        
    
    conditions = []        
    if id:         
        conditions.append(f"a.id = '{id}'")     
    if proyecto:         
        conditions.append(f"tp.proyecto = {proyecto}")     
    if fechainicio:         
        conditions.append(f"tp.fecha_inicio >= '{fechainicio}'")     
    if fechafin:         
        conditions.append(f"tp.fecha_fin <= '{fechafin}'")         
    if conditions:         
        query += " WHERE " + " AND ".join(conditions)         
    query += " GROUP BY tp.proyecto, tc.nombre;"
    
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    fileRoute = DirectoryEmpleados + "timesheetProyectos" + str(now) + ".xlsx" 
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    exportar_a_excel(resultados, fileRoute)
    
    excel_path = Path(fileRoute) 
    if not excel_path.is_file(): 
        raise HTTPException(status_code=404, detail="File not found on the server") 

    return FileResponse(excel_path)

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

