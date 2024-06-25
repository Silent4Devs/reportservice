import pandas as pd
from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse
from config.database import cursor
import pandas as pd
import psycopg2
from pathlib import Path
from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
import os

from fastapi.responses import JSONResponse, FileResponse
from fastapi import FastAPI, Query, HTTPException
from datetime import date, datetime

app = FastAPI()
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
            e.name as "Nombre", 
            e.email as "Correo Electrónico", 
            r.title as "Roles",
            e.name as "Empleado Vinculado",
            a.area as "Área", 
            p.puesto as "Puesto"
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
    ajustar_columnas(fileRoute)
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
            e.name as "Empleado",
            s.name as "Supervisor",
            a.area as "Área",
            p.puesto as "Puesto"
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
    ajustar_columnas(fileRoute)
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
            p.puesto as "Puesto", 
            a.area as "Área", 
            a.descripcion as "Descripción" 
            from puestos p 
            inner join 
            areas a on p.id_area=a.id            
            where p.deleted_at is null 
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "puestos-" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)
    
    
## Roles
@reports.get('/moduloRoles', tags=["ReportsXls"])
def getRoles():
    query = """
            select r.id as "ID", r.title as "Nombre del rol"
            from roles r 
            where r.deleted_at is null;
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "roles-" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
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
            cs.id as "ID",
            cs.rol as "Rol",
            e.name as "Nombre",
            p.puesto as "Puesto", 
            cs.telefono as "Teléfono", 
            cs.extension as "Extensión",
            cs.tel_celular as "Tel. Celular",
            cs.correo as "Correo"
            from configuracion_soporte cs 
            inner join empleados e on cs.id_elaboro=e.id 
            inner join puestos p on e.puesto_id =p.id 
            where cs.deleted_at is null
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "soporte-" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
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
            e.n_empleado as "No.Empleado",
            e.name as "Nombre",
            e.email as "Email",
            e.telefono as "Teléfono",
            a.area as "Área",
            p.puesto as "Puesto",
            s.name as "Supervisor",
            e.antiguedad as "Antigüedad",
            e.estatus as "Estatus"
            from empleados e
            left join empleados s on e.supervisor_id=s.id
            inner join areas a on e.area_id=a.id
            inner join  puestos p on e.puesto_id =p.id
            where e.deleted_at is null and e.estatus='alta'
            order by Nombre asc 
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "empleados-" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
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
            s.id as "ID",
            s.sede as "Sede", 
            s.direccion as "Dirección",
            s.descripcion as "Descripción",
            o.empresa as "Empresa"
            from sedes s 
            inner join organizacions o on s.organizacion_id=o.id 
            where s.deleted_at is null 
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "sedes-" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

## Niveles Jerarquicos
@reports.get('/nivelesJerarquicos', tags=["ReportsXls"])
def getnivelesJerarquicos():
    query = """
            select pe.nombre as "Nivel", descripcion as "Descripción" 
            from perfil_empleados pe  
            where pe.deleted_at is null
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "niveles-jerarquicos-" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
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
            a.id as "ID",
            a.area as "Nombre de área",
            g.nombre as "Grupo",
            r.area as "Reporta a",
            a.descripcion as "Descripción"
            from areas a 
            inner join grupos g on a.id_grupo=g.id
            left join areas r on a.id_reporta =r.id
            order by a.created_at asc
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "registroAreas-" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
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
            m.codigo as "Código",
            m.nombre as "Nombre",
            g.nombre as "Grupo" ,
            m.descripcion as "Descripción" 
            from macroprocesos m 
            inner join grupos g on m.id_grupo=g.id 
            order by m.created_at asc
            where m.deleted_at is null
            order by m.created_at asc
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "macroprocesos-" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
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
            p.codigo as "Código",
            p.nombre as "Nombre del proceso", 
            m.nombre as "Macroproceso",
            p.descripcion as "Descripción"
            from procesos p 
            inner join macroprocesos m on p.id_macroproceso=m.id 
            order by p.created_at asc
            where p.deleted_at is null
            order by p.created_at asc
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "moduloProcesos" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
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
            t.id as "ID",
            t.tipo as "Categoria"
            from tipoactivos t 
            order by t.created_at asc
            where t.deleted_at is null
            order by t.created_at asc
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "moduloTipoActivos" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
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
            t.id as "ID",
            t.tipo as "Categoria",
            sa.subcategoria as "Subcategoría"
            from tipoactivos t 
            inner join subcategoria_activos sa on t.id =sa.categoria_id  
            order by t.created_at asc 
            where t.deleted_at is null
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "moduloActivos" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
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
            a.id as "ID" ,
            a.nombreactivo as "Nombre del activo",
            t.tipo as "Categoria", 
            sa.subcategoria as "Subcategoría",
            a.descripcion as "Descripción",
            e.name as "Dueño",
            s.name as "Responsable"
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
    ajustar_columnas(fileRoute)
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
            g.numero as "Inciso",
            concepto as "Concepto", 
            norma as "Modulo",
            definicion as "Definición", 
            explicacion as "Explicación" 
            from glosarios g 
            where g.deleted_at is null 
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "glosario" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

## Categorias capacitaciones 
@reports.get('/categoriasCapacitaciones', tags=["ReportsXls"])
def getcategoriasCapacitaciones():
    query = """
            select distinct cc.nombre as "Nombre"
            from recursos r 
            inner join categoria_capacitacions cc on r.categoria_capacitacion_id =cc.id  ;
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "categoriasCapacitaciones" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

## Logs
@reports.get('/visualizarLogs', tags=["ReportsXls"])
def getvisualizarLogs():
    query = """
            select 
            u.name as "Nombre",
            a.event as "Evento",
            a.old_values as "Antiguos valores",
            a.new_values as "Nuevos valores",
            a.url as "Url",
            a.created_at as "Fecha de creación",
            a.updated_at as "Fecha de actualización"
            from audits a 
            inner join users u on a.user_id =u.id 
            where u.deleted_at is null;
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "visualizarLogs" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)


## Registro Timesheet
@reports.get('/registroTimesheet', tags=["ReportsXls"])
def getregistroTimesheet():
    query = """
            select 
            th.created_at as "Fecha inicio",
            th.updated_at as "Fecha fin",
            e.name as "Empleado",
            p.name as "Aprobador",
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

## Timesheet Áreas
@reports.get('/timesheetAreas', tags=["ReportsXls"])
def gettimesheetAreas():
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

## Timesheet proyectos
@reports.get('/timesheetProyectos', tags=["ReportsXls"])
def gettimesheetProyectos():
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
            group by tp.proyecto , tc.nombre;            
        """
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

## Registros Colaboradores Tareas ######################
@reports.get('/colaboradoresTareas', tags=["ReportsXls"])
def getcolaboradoresTareas():
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
            group by tp.fecha_inicio , tp.fecha_fin,th.descripcion ;
        """
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

## Timesheet Financiero
@reports.get('/timesheetFinanciero', tags=["ReportsXls"])
def gettimesheetFinanciero():
    query = """
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

## Vista global de Solicitudes de Day Off  ####### Integrar IF para 
@reports.get('/solicitudesDayOff', tags=["ReportsXls"])
def getsolicitudesDayOff():
    query = """
            select e.name as "Solicitante",
            sd.descripcion as "Descripcion",
            to_char(sd.año, 'FM9999') as "Año",
            sd.dias_solicitados as "Días solicitados",
            sd.fecha_inicio as "Inicio",
            sd.fecha_fin as "Fin",
            case  
                when sd.aprobacion = 3 then 'Aprobado'
                when sd.aprobacion = 2 then 'Rechazado'
                when sd.aprobacion = 1 then 'Pendiente'
                else 'desconocido'
            end as "Aprobacion" 
            from solicitud_dayoff sd 
            inner join empleados e on sd.empleado_id =e.id
            order by sd.año desc 
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "solicitudesDayOff" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

## Vista GLobal Solicitudes de Vacaciones
@reports.get('/solicitudesVacaciones', tags=["ReportsXls"])
def getsolicitudesVacaciones():
    query = """
            select e.name as "Solicitante",
            sv.descripcion as "Descripción",
            sv.año as "Periodo",
            sv.dias_solicitados  as "Días solicitados",
            sv.fecha_inicio as "Inicio",
            sv.fecha_fin as "Fin",
            case  
                when sv.aprobacion = 3 then 'Aprobado'
                when sv.aprobacion = 2 then 'Rechazado'
                when sv.aprobacion = 1 then 'Pendiente'
                else 'desconocido'
            end as "Aprobacion"
            from solicitud_vacaciones sv 
            inner join empleados e on sv.empleado_id =e.id 
            order by sv.fecha_inicio desc 
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "solicitudesVacaciones" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
    excel_path = Path(fileRoute)
    if not excel_path.is_file():
        raise HTTPException(
            status_code=404, detail="file not found on the server")
    return FileResponse(excel_path)

## Evaluaciones 360
@reports.get('/evaluaciones360', tags=["ReportsXls"])
def getevaluaciones360():
    query = """
            select id as "ID",
            nombre as "Nombre",
            case  
                when estatus:: integer = 3 then 'Cerrado'
                when estatus:: integer = 2 then 'Abierto'
                when estatus:: integer = 1 then 'Pendiente'
                else 'desconocido'
            end as "Estatus",
            fecha_inicio as "Fecha inicio",
            fecha_fin as "Fecha fin",
            case 
                when include_competencias then 'si'
                else 'no'
            end  as "¿Incluye competencias?",
            case 
                when include_objetivos then 'si'
                else 'no'
            end  as "¿Incluye objetivos?"
            from ev360_evaluaciones ee 
            where estatus ::integer = 3
                and include_competencias = true 
                and include_objetivos = true 
        """
    resultados = ejecutar_consulta_sql(cursor, query)
    fileRoute = DirectoryEmpleados + "evaluaciones360" + str(now) + ".xlsx"
    exportar_a_excel(
        resultados, fileRoute)
    ajustar_columnas(fileRoute)
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