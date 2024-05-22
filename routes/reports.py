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

# Users #############
@reports.get('/Users', tags=["ReportsXls"])
def retrieve_all_item():
    query = """
            select  
            e.name as Nombre, 
            e.email as Correo_Electonico, 
            r.title as Roles,
            e.name as Empleado_Vinculado,
            a.area as Area, 
            p.puesto as Puesto

            from empleados e  

            inner join role_user ru on e.id=ru.user_id 
            inner join roles r on ru.role_id =r.id
            inner join areas a ON e.area_id=a.id
            inner join puestos p ON e.puesto_id =p.id

            where r.deleted_at IS null

            order by 
            name asc;
        """

    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "users" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)


# Empleados Puestos
@reports.get('/empleadosPuestos', tags=["ReportsXls"])
def getempleadosPuestos():
    query = """
            select 
            e.name as empleado,
            s.name as supervisor,
            a.area as area,
            p.puesto as puesto

            from empleados e

            left join empleados s on e.supervisor_id=s.id
            inner join areas a on e.area_id=a.id
            inner join  puestos p on e.puesto_id =p.id

            where e.deleted_at is null and e.estatus='alta'

            order by empleado asc
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
     
## Puestos
@reports.get('/moduloPuestos', tags=["ReportsXls"])
def getPuestos():
    query = """
            select 
            p.puesto, a.area , a.descripcion 

            from puestos p 
            inner join 
            areas a on p.id_area=a.id
            
            where p.deleted_at is null 
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "moduloPuestos" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)
    
    
## Roles
@reports.get('/moduloRoles', tags=["ReportsXls"])
def getRoles():
    query = """
            select r.id as ID, r.title as Nombre_del_rol
            
            from roles r 
            
            where r.deleted_at is null;
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "moduloRoles" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)


## Soporte
@reports.get('/soporte', tags=["ReportsXls"])
def getsoporte():
    query = """
            select 
            cs.id,
            cs.rol ,
            e.name as Nombre,
            p.puesto, 
            cs.telefono , 
            cs."extension" ,
            cs.tel_celular ,
            cs.correo 

            from configuracion_soporte cs 

            inner join empleados e on cs.id_elaboro=e.id 
            inner join puestos p on e.puesto_id =p.id 

            where cs.deleted_at is null
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "soporte" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)
      
## Modulo Empleados
@reports.get('/moduloEmpleados', tags=["ReportsXls"])
def getmoduloEmpleados():
    query = """
            select 
            e.n_empleado as no_empleado,
            e.name as Nombre,
            e.email,
            e.telefono,
            a.area as area,
            p.puesto as puesto,
            s.name as supervisor,
            e.antiguedad,
            e.estatus

            from empleados e

            left join empleados s on e.supervisor_id=s.id
            inner join areas a on e.area_id=a.id
            inner join  puestos p on e.puesto_id =p.id

            where e.deleted_at is null and e.estatus='alta'

            order by Nombre asc 
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "moduloEmpleados" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)


##  Sedes
@reports.get('/moduloSedes', tags=["ReportsXls"])
def getmoduloSedes():
    query = """
            select 
            s.id,
            s.sede , 
            s.direccion ,
            s.descripcion ,
            o.empresa 

            from sedes s 

            inner join organizacions o on s.organizacion_id=o.id 
            
            where s.deleted_at is null 
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "moduloSedes" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

## Niveles Jerarquicos
@reports.get('/nivelesJerarquicos', tags=["ReportsXls"])
def getnivelesJerarquicos():
    query = """
            select pe.nombre as Nivel, descripcion 
            from perfil_empleados pe  

            where pe.deleted_at is null
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "nivelesJerarquicos" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

## Registro de Áreas
@reports.get('/registroAreas', tags=["ReportsXls"])
def getregistroAreas():
    query = """
            select 
            a.id as ID,
            a.area as Nombre_de_área,
            g.nombre as Grupo,
            r.area as Reporta_a,
            a.descripcion as Descripción

            from areas a 

            inner join grupos g on a.id_grupo=g.id
            left join areas r on a.id_reporta =r.id

            order by a.created_at asc

            where a.deleted_at is null
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "registroAreas" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

## Macroprocesos
@reports.get('/macroProcesos', tags=["ReportsXls"])
def getmacroProcesos():
    query = """
            select 
            m.codigo as Codigo,
            m.nombre as Nombre,
            g.nombre as Grupo ,
            m.descripcion as Descripcion 

            from macroprocesos m 

            inner join grupos g on m.id_grupo=g.id 

            order by m.created_at asc

            where m.deleted_at is null
 
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "macroProcesos" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)


## Procesos
@reports.get('/moduloProcesos', tags=["ReportsXls"])
def getmoduloProcesos():
    query = """
            select 
            p.codigo,
            p.nombre as Nombre_del_proceso, 
            m.nombre as Macroproceso,
            p.descripcion as Descripcion

            from procesos p 

            inner join macroprocesos m on p.id_macroproceso=m.id 

            order by p.created_at asc

            where p.deleted_at is null
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "moduloProcesos" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

## Modulo Tipo Activos
@reports.get('/moduloTipoActivos', tags=["ReportsXls"])
def getmoduloTipoActivos():
    query = """
            select 
            t.id as ID,
            t.tipo as Categoria

            from tipoactivos t 

            order by t.created_at asc

            where t.deleted_at is null
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "moduloTipoActivos" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)



## Modulo Activos
@reports.get('/moduloActivos', tags=["ReportsXls"])
def getmoduloActivos():
    query = """
            select 
            t.id as ID,
            t.tipo as Categoria,
            sa.subcategoria 

            from tipoactivos t 

            inner join subcategoria_activos sa on t.id =sa.categoria_id  

            order by t.created_at asc 

            where t.deleted_at is null
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "moduloActivos" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

## Inventario de Activos
@reports.get('/inventarioActivos', tags=["ReportsXls"])
def getinventarioActivos():
    query = """
            select 
            a.id ,
            a.nombreactivo as Nombre_del_activo,
            t.tipo as Categoria, 
            sa.subcategoria,
            a.descripcion,
            e.name as Dueno,
            s.name as Responsable

            from tipoactivos t 

            inner join	subcategoria_activos sa on t.id=sa.categoria_id 
            inner join activos a on t.id =a.tipoactivo_id 
            inner join empleados e on a.dueno_id=e.id
            left join empleados s on e.supervisor_id=s.id 

            where t.deleted_at is null ; 
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "inventarioActivos" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)
    
## Glosario
@reports.get('/glosario', tags=["ReportsXls"])
def getglosario():
    query = """
            select 
            g.numero as Inciso,
            concepto, 
            norma as Modulo,
            definicion, explicacion 

            from glosarios g 

            where g.deleted_at is null 
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "glosario" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

## Categorias capacitaciones ########### Falta revisar 
@reports.get('/categoriasCapacitaciones', tags=["ReportsXls"])
def getcategoriasCapacitaciones():
    query = """
            select 
            cc.id as No.,
            cc.nombre 

            from 
            categoria_capacitacions cc

            where g.deleted_at is null 
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "categoriasCapacitaciones" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

########


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
