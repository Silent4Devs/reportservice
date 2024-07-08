# Para probar usar:
# uvicorn pruebafiltros:app --reload --port 8001

import pandas as pd
from fastapi.responses import JSONResponse, FileResponse
from config.database import cursor
import psycopg2
from fastapi import APIRouter
from pathlib import Path
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
from datetime import date, datetime
from openpyxl import load_workbook
import os
import pprint
import sys

app = FastAPI()
DirectoryEmpleados = "reportsfile/administracion/empleados/"

# Validar si la carpeta ya existe
if not os.path.exists(DirectoryEmpleados):
    # Si no existe, crear la carpeta
    os.makedirs(DirectoryEmpleados)

now = date.today()


@app.post("/")
def read_root():
    return {"message": "Hi"}


# Registro Timesheet *
@app.post('/registrosTimesheet/', tags=["ReportsXls"])
def get_registro_timesheet(
    area: Optional[str] = None,
    empleado: Optional[str] = None,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None
):
    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Formato de fecha incorrecto. Use 'YYYY-MM-DD'.")

    query = """
        select
        to_char(date_trunc('week', t.fecha_dia), 'DD/MM/YYYY') as "Fecha inicio",
        to_char(t.fecha_dia, 'DD/MM/YYYY') as "Fecha fin",
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
        inner join empleados e ON t.empleado_id = e.id
        inner join empleados p ON t.aprobador_id = p.id
        inner join areas a on e.id = a.empleados_id
        inner join timesheet_horas th on t.id = th.timesheet_id
        where e.deleted_at is null
    """

    if area:
        query += f" and a.area = '{area}'"
    if empleado:
        query += f" and e.name = '{empleado}'"
    if fecha_inicio and fecha_fin:
        query += f" and t.fecha_dia between '{fecha_inicio}' and '{fecha_fin}'"

    query += """
        group by
            t.fecha_dia,
            e.name,
            p.name,
            a.area,
            t.estatus
        order by t.fecha_dia desc;
    """

    print(query)

    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)

    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "registroTimesheet" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
    excel_path = Path(fileRoute)

    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)


# Timesheet Áreas *
@app.post("/timesheetAreas/", tags=["ReportsXls"])
def gettimesheetAreas(
    area: Optional[str] = None,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None
):
    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Formato de fecha incorrecto. Use 'YYYY-MM-DD'.")

    query = """
            select 
            e.name as "Nombre",
            p.puesto as "Puesto",
            a.area as "Área",
            e.estatus as "Estatus",
            e.antiguedad as "Fecha"
            from empleados e 
            inner join puestos p on e.puesto_id =p.id 
            inner join areas a on e.area_id=a.id
        """
    if area:
        query += f" and a.area = '{area}'"
    if fecha_inicio and fecha_fin:
        query += f" and t.fecha_dia between '{fecha_inicio}' and '{fecha_fin}'"

    query += """
        group by
            a.area,
            t.fecha_dia
    """   

    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)

    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "timesheetAreas" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
    excel_path = Path(fileRoute)

    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

# Timesheet proyectos 


@app.post('/timesheetProyectos/', tags=["ReportsXls"])
def gettimesheetProyectos(
    area: Optional[str] = None,
    proyecto: Optional[str] = None,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None
    ):

    if fecha_inicio and fecha_fin:   
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Formato de fecha incorrecto. Use 'YYYY-MM-DD'.")

    query = """
            select 
            tp.proyecto as "ID-Proyecto",
            string_agg(distinct a.area, ', ') as "Áreas participantes",
            string_agg(distinct e.name, ', ') as "Empleados participantes",
            tc.nombre as "Cliente"
            from timesheet_proyectos tp 
            left join timesheet_proyectos_empleados tpe on tp.id=tpe.proyecto_id 
            left join timesheet_proyectos_areas tpa on tp.id =tpe.proyecto_id 
            left join areas a on tpe.area_id =a.id  
            left join empleados e on tpe.empleado_id =e.id 
            right  join timesheet_clientes tc on tp.cliente_id =tc.id           
        """
    
    if area:
        query += f" and a.area = '{area}'"
    if proyecto:
        query += f" and tp.proyecto = '{proyecto}'"
    if fecha_inicio and fecha_fin:
        query += f" and tp.fecha_inicio between '{fecha_inicio}' and '{fecha_fin}'"


    query += """
        group by 
            a.area,
            tp.proyecto, 
            tc.nombre,
            tp.fecha_inicio 
    """   

    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)

    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "timesheetProyectos" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

# Registros Colaboradores Tareas *
@app.post('/colaboradoresTareas/', tags=["ReportsXls"])
def getcolaboradoresTareas(
    empleado: Optional[str] = None,
    proyecto: Optional[str] = None,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None
    ):

    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Formato de fecha incorrecto. Use 'YYYY-MM-DD'.")

    query = """
            select 
            tp.fecha_inicio as "Fecha inicio", 
            tp.fecha_fin as "Fecha fin",
            string_agg(distinct e.name, ', ') as  "Empleado",
            string_agg(distinct s.name, ', ') as "Supervisor",
            string_agg(distinct tp.proyecto, ', ') as "Proyecto",
            string_agg(distinct tt.tarea, ', ') as "Tarea",
            th.descripcion as "Descripción",
            sum(
                coalesce(cast(nullif(th.horas_lunes, '') as numeric), 0) +
                coalesce(cast(nullif(th.horas_martes, '') as numeric), 0) +
                coalesce(cast(nullif(th.horas_miercoles, '') as numeric), 0) +
                coalesce(cast(nullif(th.horas_jueves, '') as numeric), 0) +
                coalesce(cast(nullif(th.horas_viernes, '') as numeric), 0) +
                coalesce(cast(nullif(th.horas_sabado, '') as numeric), 0) +
                coalesce(cast(nullif(th.horas_domingo, '') as numeric), 0)
            ) as "Horas de la semana"
            from timesheet_proyectos tp 
            left join timesheet_proyectos_empleados tpe on tp.id =tpe.proyecto_id 
            left join empleados e on tpe.empleado_id =e.id 
            left join empleados s on e.supervisor_id=s.id
            left join timesheet_tareas tt on tp.id =tt.proyecto_id
            right join timesheet_horas th on e.id=th.empleado_id 
            where tp.fecha_inicio > '2022-01-01'
        """
    if empleado:
        query += f" and e.name = '{empleado}'"
    if proyecto:
        query += f" and tp.proyecto = '{proyecto}'"
    if fecha_inicio and fecha_fin:
        query += f" and t.fecha_inicio between '{fecha_inicio}' and '{fecha_fin}'"

    query += """
        group by
            e.name,
            tp.proyecto,
            tp.fecha_inicio, 
            tp.fecha_fin,
            th.descripcion 
        order by tp.fecha_inicio desc;
    """

    print(query)

    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)

    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "colaboradoresTareas" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
    excel_path = Path(fileRoute)

    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

# Timesheet Financiero *
@app.post('/timesheetFinanciero/', tags=["ReportsXls"])
def gettimesheetFinanciero(
    proyecto: Optional[str] = None):

    query = """
            select
            tp.identificador as "ID",
            tp.proyecto as "Proyecto",
            tc.nombre as "Cliente",
            a.area as "Área(s)",
            e.name as "Empleados participantes",
            tpe.horas_asignadas as "Horas del empleado",
            tpe.horas_asignadas * tpe.costo_hora as "Costo total del empleado",
            tp.estatus as "Estatus",
                sum(tpe.horas_asignadas)over(partition by tpe.proyecto_id) as "Horas totales del proyecto",
                sum(tpe.horas_asignadas * tpe.costo_hora) over(partition by tpe.proyecto_id) as "Costo total del Proyecto"
            from timesheet_proyectos tp 
            left join timesheet_clientes tc on tp.cliente_id =tc.id
            left join timesheet_proyectos_empleados tpe on tp.id =tpe.proyecto_id 
            left join areas a on tpe.area_id =a.id 
            left join empleados e on tpe.empleado_id =e.id 
        """
    
    if proyecto:
        query += f" and tp.proyecto = '{proyecto}'"

    query += """
        group by
            tp.proyecto
    """    

    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)

    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "timesheetFinanciero" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
    excel_path = Path(fileRoute)

    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

## Empleados controller
@app.post('/empleadosController/', tags=["ReportsXls"])
def getempleadoController(
    empleado: Optional[str] = None
    ):
    
    query = """
            select 
            e.name as "Empleado",
            p.name as "Supervisor",
            s.sede as "Sede",
            pe.nombre as "Perfil",
            string_agg(distinct ce.nombre, ', ' ) as "Certificaciones",
            ee.institucion as "Educación"
            from empleados e 
            left join empleados p on e.supervisor_id=p.id 
            inner join sedes s on e.sede_id=s.id
            left join perfil_empleados pe on e.perfil_empleado_id=pe.id 
            left join certificaciones_empleados ce on e.id=ce.empleado_id 
            left join educacion_empleados ee on e.id=ee.empleado_id 
            where e.estatus= 'alta'
        """
        
    if empleado:
            query += f" and e.name = '{empleado}'"

    query += """
        group by
            e.name,
            p.name,
            s.sede,
            pe.nombre, 
            ee.institucion 
        order by e.name asc;
    """
    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)

    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "empleadoController" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
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
