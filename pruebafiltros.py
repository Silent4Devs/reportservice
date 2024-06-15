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
from openpyxl import load_workbook
import os

app = FastAPI()

DirectoryEmpleados = "reportsfile/administracion/empleados/"

## Timesheet proyectos
@app.get('/timesheetProyectosF', tags=["ReportsXls"])
def get_timesheet_proyectosF(
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
    fileRoute = DirectoryEmpleados + "timesheetProyectosF" + str(now) + ".xlsx" 
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    exportar_a_excel(resultados, fileRoute)
    ajustar_columnas(fileRoute)

    excel_path = Path(fileRoute) 
    if not excel_path.is_file(): 
        raise HTTPException(status_code=404, detail="File not found on the server") 

    return FileResponse(excel_path)
get_timesheet_proyectosF()
    
## Registro Timesheet Areas
@app.get('/registroTimesheet', tags=["ReportsXls"])
def get_registroTimesheet(
    empleado: Optional[str] = Query(None, description="Nombre del Empleado"),     
    fechainicio: Optional[datetime] = Query(None, description="Fecha de inicio en formato YYYY-MM-DD"), 
    fechafin: Optional[datetime] = Query(None, description="Fecha de fin en formato YYYY-MM-DD"),
    horas_semana: Optional[float] = Query(None, description="Horas registradas en la semana")
    ):    
      
    query = """         
        select 
            th.created_at as "Fecha inicio",
            th.updated_at as "Fecha fin",
            e.name as "Empleado",
            p.name as "Aprovador",
            a.area as "Área",
            t.estatus as "Estatus",
            sum(
            coalesce(cast(nullif(th.horas_lunes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_martes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_miercoles, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_jueves, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_viernes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_sabado, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_domingo, '') as numeric), 0)
            ) as "Horas de la semana"
            from timesheet t 
            inner join empleados e ON t.empleado_id =e.id
            inner join empleados p ON t.aprobador_id =p.id
            inner join areas a on e.id =a.empleados_id 
            inner join timesheet_horas th on t.id=th.timesheet_id  
            where e.deleted_at is null
            GROUP BY 
                th.created_at, 
                th.updated_at, 
                e.name, 
                p.name, 
                a.area, 
                t.estatus;
        """        
    

    conditions = []        
    if empleado:         
        conditions.append(f"e.name = '{empleado}'")     
    if fechainicio:         
        conditions.append(f"th.created_at >= '{fechainicio}'")     
    if fechafin:         
        conditions.append(f"th.updated_at <= '{fechafin}'")  
    if horas_semana is not None:
        conditions.append(f"""
            SUM(
                COALESCE(CAST(NULLIF(th.horas_lunes, '') AS numeric), 0) +
                COALESCE(CAST(NULLIF(th.horas_martes, '') AS numeric), 0) +
                COALESCE(CAST(NULLIF(th.horas_miercoles, '') AS numeric), 0) +
                COALESCE(CAST(NULLIF(th.horas_jueves, '') AS numeric), 0) +
                COALESCE(CAST(NULLIF(th.horas_viernes, '') AS numeric), 0) +
                COALESCE(CAST(NULLIF(th.horas_sabado, '') AS numeric), 0) +
                COALESCE(CAST(NULLIF(th.horas_domingo, '') AS numeric), 0)
            ) = {horas_semana}
        """)       

    if conditions:         
        query += " AND " + " AND ".join(conditions)         

    query += """
        GROUP BY 
            th.created_at, 
            th.updated_at, 
            e.name, 
            p.name, 
            a.area, 
            t.estatus;
    """
    

    now = datetime.now().strftime("%Y%m%d%H%M%S")
    fileRoute = DirectoryEmpleados + "registroTimesheet" + str(now) + ".xlsx" 
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    exportar_a_excel(resultados, fileRoute)
    ajustar_columnas(fileRoute)

    excel_path = Path(fileRoute) 
    if not excel_path.is_file(): 
        raise HTTPException(status_code=404, detail="File not found on the server") 

    return FileResponse(excel_path)


##Registro Timesheet Áreas
@app.get('/timesheetAreas', tags=["ReportsXls"])
def gettimesheetAreas(
    area: Optional[str] = Query(None, description="Área de los empleados"),
    ############Ajustar
    fecha_ultima_semana: Optional[datetime] = Query(None, description="Fecha de última semana en formato YYYY-MM-DD"), 
    fecha_penultima_semana: Optional[datetime] = Query(None, description="Fecha de penúltima semana en formato YYYY-MM-DD")
):    
    query = """         
        SELECT
            e.name AS "Nombre",
            p.puesto AS "Puesto",
            a.area AS "Área",
            e.estatus AS "Estatus",
            e.antiguedad AS "Fecha"
        FROM empleados e
        INNER JOIN puestos p ON e.puesto_id = p.id 
        INNER JOIN areas a ON e.area_id = a.id
        WHERE 1=1
    """        

    conditions = []        
    if area:         
        conditions.append(f"a.area = '{area}'")     
    if fecha_ultima_semana:  #######ajustar       
        conditions.append(f"e.antiguedad <= '{fecha_ultima_semana}'")     
    if fecha_penultima_semana:         
        conditions.append(f"e.antiguedad >= '{fecha_penultima_semana}'")       

    if conditions:         
        query += " AND " + " AND ".join(conditions)         

    query += ";"
    
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    fileRoute = DirectoryEmpleados +"timesheetAreas" + str(now) + ".xlsx" 
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    exportar_a_excel(resultados, fileRoute)
    ajustar_columnas(fileRoute)

    excel_path = Path(fileRoute) 
    if not excel_path.is_file(): 
        raise HTTPException(status_code=404, detail="File not found on the server") 

    return FileResponse(excel_path)

## Registros Colaboradores Tareas
@app.get('/colaboradoresTareas', tags=["ReportsXls"])
def get_timesheet_proyectos(
    empleado: Optional[str] = Query(None, description="Nombre del empleado"),
    proyecto: Optional[int] = Query(None, description="ID del proyecto"),
    fechainicio: Optional[datetime] = Query(None, description="Fecha de inicio en formato YYYY-MM-DD"), 
    fechafin: Optional[datetime] = Query(None, description="Fecha de fin en formato YYYY-MM-DD")
):    
    query = """         
        SELECT
            tp.fecha_inicio AS "Fecha inicio", 
            tp.fecha_fin AS "Fecha fin",
            STRING_AGG(DISTINCT e.name, ', ') AS "Empleado",
            STRING_AGG(DISTINCT s.name, ', ') AS "Supervisor",
            STRING_AGG(DISTINCT tp.proyecto::text, ', ') AS "Proyecto",
            STRING_AGG(DISTINCT tt.tarea, ', ') AS "Tarea",
            th.descripcion AS "Descripción",
            SUM(
                COALESCE(CAST(NULLIF(th.horas_lunes, '') AS numeric), 0) +
                COALESCE(CAST(NULLIF(th.horas_martes, '') AS numeric), 0) +
                COALESCE(CAST(NULLIF(th.horas_miercoles, '') AS numeric), 0) +
                COALESCE(CAST(NULLIF(th.horas_jueves, '') AS numeric), 0) +
                COALESCE(CAST(NULLIF(th.horas_viernes, '') AS numeric), 0) +
                COALESCE(CAST(NULLIF(th.horas_sabado, '') AS numeric), 0) +
                COALESCE(CAST(NULLIF(th.horas_domingo, '') AS numeric), 0)
            ) AS "Horas de la semana"
        FROM timesheet_proyectos tp 
        LEFT JOIN timesheet_proyectos_empleados tpe ON tp.id = tpe.proyecto_id 
        LEFT JOIN empleados e ON tpe.empleado_id = e.id 
        LEFT JOIN empleados s ON e.supervisor_id = s.id
        LEFT JOIN timesheet_tareas tt ON tp.id = tt.proyecto_id
        RIGHT JOIN timesheet_horas th ON e.id = th.empleado_id 
        WHERE tp.fecha_inicio > '2022-01-01'
    """        

    conditions = []        
    if empleado:         
        conditions.append(f"e.name = '{empleado}'")     
    if proyecto:         
        conditions.append(f"tp.proyecto = {proyecto}")     
    if fechainicio:         
        conditions.append(f"tp.fecha_inicio >= '{fechainicio}'")     
    if fechafin:         
        conditions.append(f"tp.fecha_fin <= '{fechafin}'")       

    if conditions:         
        query += " AND " + " AND ".join(conditions)         

    query += """
        GROUP BY 
            tp.fecha_inicio, 
            tp.fecha_fin, 
            th.descripcion;
    """
    
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    fileRoute = DirectoryEmpleados + "colaboradoresTareas" + str(now) + ".xlsx" 
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    exportar_a_excel(resultados, fileRoute)
    ajustar_columnas(fileRoute)

    excel_path = Path(fileRoute) 
    if not excel_path.is_file(): 
        raise HTTPException(status_code=404, detail="File not found on the server") 

    return FileResponse(excel_path)

##Timesheet Financiero 
@app.get('/timesheetFinanciero', tags=["ReportsXls"])
def get_timesheet_proyectos(
    proyecto: Optional[int] = Query(None, description="ID del proyecto")
):    
    query = """         
        SELECT
            tc.nombre AS "Cliente",
            a.area AS "Área(s)",
            e.name AS "Empleados participantes",
            tpe.horas_asignadas AS "Horas del empleado",
            tpe.horas_asignadas * tpe.costo_hora AS "Costo total del empleado",
            tp.estatus AS "Estatus",
            SUM(tpe.horas_asignadas) OVER(PARTITION BY tpe.proyecto_id) AS "Horas totales del proyecto",
            SUM(tpe.horas_asignadas * tpe.costo_hora) OVER(PARTITION BY tpe.proyecto_id) AS "Costo total del Proyecto"
        FROM timesheet_proyectos tp 
        LEFT JOIN timesheet_clientes tc ON tp.cliente_id = tc.id
        LEFT JOIN timesheet_proyectos_empleados tpe ON tp.id = tpe.proyecto_id 
        LEFT JOIN areas a ON tpe.area_id = a.id 
        LEFT JOIN empleados e ON tpe.empleado_id = e.id
        WHERE 1=1
    """        

    if proyecto:         
        query += f" AND tp.id = {proyecto}"         

    query += ";"
    
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    fileRoute = DirectoryEmpleados + "timesheetFinanciero" + str(now) + ".xlsx" 
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    exportar_a_excel(resultados, fileRoute)
    ajustar_columnas(fileRoute)

    excel_path = Path(fileRoute) 
    if not excel_path.is_file(): 
        raise HTTPException(status_code=404, detail="File not found on the server") 

    return FileResponse(excel_path) 

#########################
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

def ajustar_columnas(nombre_archivo):
    try:
        workbook = load_workbook(nombre_archivo)
        worksheet = workbook.active

        for col in worksheet.columns:
            max_length = 0
            column = col[0].column_letter  # Get the column name
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column].width = adjusted_width

        workbook.save(nombre_archivo)
        print("Columnas ajustadas en", nombre_archivo)
    except Exception as e:
        print("No se pudieron ajustar las columnas debido a un error." + str(e))
        raise HTTPException(
            status_code=500, detail="Column adjust error: " + str(e))
    
