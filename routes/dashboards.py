import plotly.graph_objects as go
import pandas as pd
import psycopg2
from fastapi import HTTPException, FastAPI
from fastapi import APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from config.database import conexion, cursor
from typing import Optional

app=FastAPI()
dash= APIRouter()
# Verificar si la conexión es exitosa antes de continuar

############ Registros Timesheet ############### (Barras horizontal)

if cursor is None:
    raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

@dash.post('/registrosTimesheetEstatus/', tags=["Dashboards"])
def registros_timesheet_estatus(
    area: Optional[str] = None
): 
    # Definir el query
    query = """
    select
        count(case when t.estatus = 'aprobado' then 1 end) as "Aprobado",
        count(case when t.estatus = 'pendiente' then 1 end) as "Pendiente",
        count(case when t.estatus = 'rechazado' then 1 end) as "Rechazado",
        count(case when t.estatus = 'borrador' then 1 end) as "Borrador",
        a.area as "Área"
    from timesheet t
    inner join empleados e on t.empleado_id = e.id
    inner join areas a on e.area_id = a.id
    """
    if area:
        query += f" and a.area = '{area}'"

    query += """
        group by
            a.area
    """ 

    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)
    
    # Ejecutar la consulta SQL y obtener los datos
    def ejecutar_consulta_sql(cursor, consulta):
        try:
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(resultados, columns=colnames)
            return df
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail="Error al ejecutar la consulta SQL: " + str(e))
    
    df = ejecutar_consulta_sql(cursor, query)
    
    # Crear la gráfica
    fig = go.Figure(data=[
        go.Bar(name='Aprobado', y=df['Área'], x=df['Aprobado'], orientation='h'),
        go.Bar(name='Pendiente', y=df['Área'], x=df['Pendiente'], orientation='h'),
        go.Bar(name='Rechazado', y=df['Área'], x=df['Rechazado'], orientation='h'),
        go.Bar(name='Borrador', y=df['Área'], x=df['Borrador'], orientation='h')
    ])
    
    # Actualizar el diseño de la gráfica
    fig.update_layout(
        title='Estatus por Área',
        xaxis_title='Registros de timesheet',
        yaxis_title='Área',
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    graph_html = fig.to_html(full_html=False)

    return HTMLResponse(content=graph_html)

app.include_router(dash)


################################################ (Estatus Todas las Areas Dona)

if cursor is None:
    raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

@dash.post('/registrosEstatusDona/', tags=["Dashboards"]) 
def registros_timesheet_status_dona(
    area: Optional[str] = None
):
    query = """
        select
            sum(case when t.estatus = 'aprobado' then 1 else 0 end) as "Aprobado",
            sum(case when t.estatus = 'pendiente' then 1 else 0 end) as "Pendiente",
            sum(case when t.estatus = 'rechazado' then 1 else 0 end) as "Rechazado",
            sum(case when t.estatus = 'borrador' then 1 else 0 end) as "Borrador"
        from timesheet t
        left join empleados e on t.empleado_id =e.id 
        left join areas a on e.area_id =a.id 
    """
    if area:
        query += f" and a.area = '{area}'"

    query += """
        group by
            a.area
    """ 

    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)

    df = pd.read_sql(query, conexion)
    
    labels = df.columns.tolist()  #Estatus
    values = df.iloc[0].tolist()  # Valores correspondientes a cada estatus

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    fig.update_layout(
        title='Registros de Timesheet por Estatus',
        annotations=[dict(text=' ', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    graph_html = fig.to_html(full_html=False)

    return HTMLResponse(content=graph_html)

app.include_router(dash)

################################################ (Barras Vertical)

if cursor is None:
    raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

@dash.post('/registrosTimesheetEstatus/', tags=["Dashboards"])
def registros_timesheet_area(
    area: Optional[str] = None
):
    query = """
                select
                a.area as "Área",
                sum(
                    coalesce(cast(nullif(th.horas_lunes, '') as numeric), 0) +
                    coalesce(cast(nullif(th.horas_martes, '') as numeric), 0) +
                    coalesce(cast(nullif(th.horas_miercoles, '') as numeric), 0) +
                    coalesce(cast(nullif(th.horas_jueves, '') as numeric), 0) +
                    coalesce(cast(nullif(th.horas_viernes, '') as numeric), 0) +
                    coalesce(cast(nullif(th.horas_sabado, '') as numeric), 0) +
                    coalesce(cast(nullif(th.horas_domingo, '') as numeric), 0)
                ) as "Horas del área"
                from timesheet t
                inner join empleados e on t.empleado_id = e.id
                inner join areas a on e.area_id = a.id
                left join timesheet_horas th on t.id=th.timesheet_id 
    """
    if area:
        query += f" and a.area = '{area}'"

    query += """
        group by
            a.area
    """ 

    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)
    
    def ejecutar_consulta_sql(cursor, consulta):
        try:
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(resultados, columns=colnames)
            return df
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail="Error al ejecutar la consulta SQL: " + str(e))
    
    df = ejecutar_consulta_sql(cursor, query)
    
    # Crear la gráfica de barras
    fig = go.Figure(data=[
        go.Bar(name='Registros de horas trabajadas por Área', x=df['Área'], y=df['Horas del área'])
    ])
    
    # Actualizar el layout de la gráfica
    fig.update_layout(
        title='Horas por Área',
        xaxis_title='Área',
        yaxis_title='Horas del área',
        bargap=0.15
    )
    
    graph_html = fig.to_html(full_html=False)

    return HTMLResponse(content=graph_html)

app.include_router(dash)


############## Registros Timesheet Empleados ############## (Barras Horizontales)

if cursor is None:
    raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

@dash.post('/registrosTimEmpEstatus/', tags=["Dashboards"])
def registros_tsempleados_estatus(
    area: Optional[str] = None
): 
    # Definir el query
    query = """
            select e.name as "Empleado",
            a.area as "Área",
            sum(case when t.estatus = 'aprobado' then 1 else 0 end) as "Aprobado",
            sum(case when t.estatus = 'pendiente' then 1 else 0 end) as "Pendiente",
            sum(case when t.estatus = 'rechazado' then 1 else 0 end) as "Rechazado",
            sum(case when t.estatus = 'borrador' then 1 else 0 end) as "Borrador"
            from timesheet t
            left join empleados e on t.empleado_id = e.id
            inner join areas a on e.area_id = a.id
            left join timesheet_horas th on t.id=th.timesheet_id 
    """
    if area:
        query += f" and a.area = '{area}'"

    query += """
        group by
            a.area, 
            e.name
    """ 

    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)
    
    # Ejecutar la consulta SQL y obtener los datos
    def ejecutar_consulta_sql(cursor, consulta):
        try:
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(resultados, columns=colnames)
            return df
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail="Error al ejecutar la consulta SQL: " + str(e))
    
    df = ejecutar_consulta_sql(cursor, query)
    
    # Crear la gráfica
    fig = go.Figure(data=[
        go.Bar(name='Aprobado', y=df['Empleado'], x=df['Aprobado'], orientation='h'),
        go.Bar(name='Pendiente', y=df['Empleado'], x=df['Pendiente'], orientation='h'),
        go.Bar(name='Rechazado', y=df['Empleado'], x=df['Rechazado'], orientation='h'),
        go.Bar(name='Borrador', y=df['Empleado'], x=df['Borrador'], orientation='h')
    ])
    
    # Actualizar el diseño de la gráfica
    fig.update_layout(
        title='Estatus Empleado por Área',
        xaxis_title='Registros de timesheet',
        yaxis_title='Empleado',
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    
    graph_html = fig.to_html(full_html=False)

    return HTMLResponse(content=graph_html)

app.include_router(dash)

###################################################### (Sin filtro , no lleva/Registros Timesheet por Área Dona)

if cursor is None:
    raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

@dash.post('/registrosTimesheetAreaDona', tags=["Dashboards"]) 
def registros_timesheetArea_dona():
    query = """
                select
                a.area as "Área",
                sum(
                    coalesce(cast(nullif(th.horas_lunes, '') as numeric), 0) +
                    coalesce(cast(nullif(th.horas_martes, '') as numeric), 0) +
                    coalesce(cast(nullif(th.horas_miercoles, '') as numeric), 0) +
                    coalesce(cast(nullif(th.horas_jueves, '') as numeric), 0) +
                    coalesce(cast(nullif(th.horas_viernes, '') as numeric), 0) +
                    coalesce(cast(nullif(th.horas_sabado, '') as numeric), 0) +
                    coalesce(cast(nullif(th.horas_domingo, '') as numeric), 0)
                ) as "Horas del área"
                from timesheet t
                inner join empleados e on t.empleado_id = e.id
                inner join areas a on e.area_id = a.id
                left join timesheet_horas th on t.id=th.timesheet_id 
                group by a.area
    """

    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)

    df = pd.read_sql(query, conexion)
    
    labels = df['Área'].tolist()  
    values = df['Horas del área'].tolist()  

    # Crear la gráfica de dona
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    # Actualizar el layout de la gráfica
    fig.update_layout(
        title='Registros de Timesheet por Área',
        annotations=[dict(text=' ', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    graph_html = fig.to_html(full_html=False)

    return HTMLResponse(content=graph_html)

app.include_router(dash)

################################################# (Dona ultimo mes)

if cursor is None:
    raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

@dash.post('/registrosTimesheetDona/', tags=["Dashboards"]) 
def registros_timesheetMes_dona(
    area: Optional[str] = None
):
    query = """
        select
            sum(case when t.estatus = 'aprobado' then 1 else 0 end) as "Registros Aprobados",
            sum(case when t.estatus = 'rechazado' then 1 else 0 end) as "Registros Rechazados",
            sum(case when t.estatus = 'pendiente' then 1 else 0 end) as "Pendiente",
            sum(case when t.estatus = 'borrador' then 1 else 0 end) as "Borrador",
            count(*) as "Registros Totales"
        from (
        select *
        from timesheet t
        where t.fecha_dia BETWEEN CURRENT_DATE - INTERVAL '1 MONTH' AND CURRENT_DATE
        )t
        left join empleados e on t.empleado_id=e.id 
        left join areas a on e.area_id =a.id 
        where t.estatus in ('aprobado', 'rechazado')        
    """
    if area:
        query += f" and a.area = '{area}'"

    query += """
        group by
            a.area
    """ 

    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)

    df = pd.read_sql(query, conexion)

    if df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron registros para el área y período especificados")
    
    labels = df.columns.tolist()
    values = df.iloc[0].tolist()  

    # Crear la gráfica de dona
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    # Actualizar el layout de la gráfica
    fig.update_layout(
        title='Registros de Timesheet del mes',
        annotations=[dict(text=' ', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    graph_html = fig.to_html(full_html=False)

    return HTMLResponse(content=graph_html)

app.include_router(dash)

####################  Timesheet Proyectos ####################### (Proyecto Areas Horizontal)
if cursor is None:
    raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

@dash.post('/timesheetProyectosArea', tags=["Dashboards"])
def timesheet_proyectos_area(
    estatus: Optional[str] = None,
    proyecto: Optional[str] = None,
    area: Optional[str] = None    
    ): 
    # Definir el query
    query = """
        select 
        a.area as "Áreas",
        count(tt.tarea) as "Tareas Asignadas del Proyecto" ,
        sum(
            coalesce(cast(nullif(th.horas_lunes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_martes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_miercoles, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_jueves, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_viernes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_sabado, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_domingo, '') as numeric), 0)
        ) as "Horas invertidas"
        from timesheet_proyectos tp 
        inner join timesheet_tareas tt on tp.id=tt.proyecto_id 
        inner join areas a on tt.area_id=a.id 
        inner join timesheet_horas th on tt.id =th.tarea_id 
    """
    if area:
        query += f" and a.area = '{area}'"
    if proyecto:
        query += f" and tp.proyecto = '{proyecto}'"
    if estatus:
        query += f" and tp.estatus = '{estatus}'"


    query += """
        group by 
            a.area,
            tp.proyecto,
            tp.fecha_inicio, 
            tp.estatus
        order by a.area
    """   

    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)

    # Ejecutar la consulta SQL y obtener los datos
    def ejecutar_consulta_sql(cursor, consulta):
        try:
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(resultados, columns=colnames)
            return df
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail="Error al ejecutar la consulta SQL: " + str(e))
    
    df = ejecutar_consulta_sql(cursor, query)
 
    # Crear la gráfica
    fig = go.Figure(data=[
        go.Bar(name='Horas invertidas', y=df['Áreas'], x=df['Horas invertidas'], orientation='h'),
        go.Bar(name='Tareas Asignadas del Proyecto', y=df['Áreas'], x=df['Tareas Asignadas del Proyecto'], orientation='h')
    ])
    
    # Actualizar el diseño de la gráfica
    fig.update_layout(
        title='Proyectos',
        xaxis_title='Horas Trabajadas en el Proyecto',
        yaxis_title='Área',
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )

    graph_html = fig.to_html(full_html=False)

    return HTMLResponse(content=graph_html)

app.include_router(dash)


############################ (Horas Invertidas en el Proyecto por Área Dona)
if cursor is None:
    raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

@dash.post('/timesheetHorasAreaDona/', tags=["Dashboards"]) 
def timesheet_horas_area_dona(
    estatus: Optional[str] = None,
    proyecto: Optional[str] = None,
    area: Optional[str] = None
):
    query = """
        select 
        a.area as "Áreas",
        tp.proyecto as "Proyecto",
        count(tt.tarea) as "Tareas Asignadas" ,
        sum(
            coalesce(cast(nullif(th.horas_lunes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_martes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_miercoles, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_jueves, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_viernes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_sabado, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_domingo, '') as numeric), 0)
        ) as "Horas invertidas"
        from timesheet_proyectos tp 
        inner join timesheet_tareas tt on tp.id=tt.proyecto_id 
        inner join areas a on tt.area_id=a.id 
        inner join timesheet_horas th on tt.id =th.tarea_id 
    """

    if area:
        query += f" and a.area = '{area}'"
    if proyecto:
        query += f" and tp.proyecto = '{proyecto}'"
    if estatus:
        query += f" and tp.estatus = '{estatus}'"


    query += """
        group by 
            a.area,
            tp.proyecto,
            tp.estatus
        order by a.area
    """   

    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)

    df = pd.read_sql(query, conexion)
    
    labels = df['Áreas'].tolist()  
    values = df['Horas invertidas'].tolist() 

    # Crear la gráfica de dona
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    # Actualizar el layout de la gráfica
    fig.update_layout(
        title='Horas Invertidas en el Proyecto por Área',
        annotations=[dict(text=' ', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    graph_html = fig.to_html(full_html=False)

    return HTMLResponse(content=graph_html)

app.include_router(dash)

################ (Tareas en el Proyecto por Área Dona)
if cursor is None:
    raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

@dash.post('/timesheetHorasAreaDona/', tags=["Dashboards"]) 
def timesheet_horas_area_dona(
    estatus: Optional[str] = None,
    proyecto: Optional[str] = None,
    area: Optional[str] = None
):
    query = """
        select 
        a.area as "Áreas",
        tp.proyecto as "Proyecto",
        count(tt.tarea) as "Tareas Asignadas" ,
        sum(
            coalesce(cast(nullif(th.horas_lunes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_martes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_miercoles, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_jueves, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_viernes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_sabado, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_domingo, '') as numeric), 0)
        ) as "Horas invertidas"
        from timesheet_proyectos tp 
        inner join timesheet_tareas tt on tp.id=tt.proyecto_id 
        inner join areas a on tt.area_id=a.id 
        inner join timesheet_horas th on tt.id =th.tarea_id 
    """

    if area:
        query += f" and a.area = '{area}'"
    if proyecto:
        query += f" and tp.proyecto = '{proyecto}'"
    if estatus:
        query += f" and tp.estatus = '{estatus}'"


    query += """
        group by 
            a.area,
            tp.proyecto, 
            tp.estatus
        order by a.area
    """   
    df = pd.read_sql(query, conexion)
    
    labels = df['Áreas'].tolist()  
    values = df['Tareas Asignadas'].tolist() 

    # Crear la gráfica de dona
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    # Actualizar el layout de la gráfica
    fig.update_layout(
        title='Tareas en el Proyecto por Área',
        annotations=[dict(text=' ', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    graph_html = fig.to_html(full_html=False)

    return HTMLResponse(content=graph_html)

app.include_router(dash)

###################### Horas trabajadas en proyecto por empleado (Barras verticales) 
if cursor is None:
    raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

@dash.post('/timesheetHorasAreaEmp/', tags=["Dashboards"])
def timesheet_horasarea_emp(
    estatus: Optional[str] = None,
    proyecto: Optional[str] = None,
    area: Optional[str] = None
):
    query = """
        select 
        concat(e.name, ' - ', a.area) as "Empleado",
                sum(
            coalesce(cast(nullif(th.horas_lunes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_martes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_miercoles, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_jueves, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_viernes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_sabado, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_domingo, '') as numeric), 0)
        ) as "Horas trabajadas en proyecto"
        from timesheet_proyectos tp 
        left join timesheet_tareas tt on tp.id=tt.proyecto_id  
        inner join timesheet_horas th on tt.id =th.tarea_id 
        inner join empleados e on th.empleado_id =e.id
        left join areas a on e.area_id =a.id
    """
    if area:
        query += f" and a.area = '{area}'"
    if proyecto:
        query += f" and tp.proyecto = '{proyecto}'"
    if estatus:
        query += f" and tp.estatus = '{estatus}'"


    query += """
        group by 
            a.area,
            tp.proyecto, 
            e.name,
            tp.estatus
        order by a.area
    """   
    def ejecutar_consulta_sql(cursor, consulta):
        try:
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(resultados, columns=colnames)
            return df
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail="Error al ejecutar la consulta SQL: " + str(e))
    
    df = ejecutar_consulta_sql(cursor, query)
    
    # Crear la gráfica de barras
    fig = go.Figure(data=[
        go.Bar(name='Registros de horas trabajadas por Área', x=df['Empleado'], y=df['Horas trabajadas en proyecto'])
    ])
    
    # Actualizar el layout de la gráfica
    fig.update_layout(
        title='Horas Trabajadas en Proyecto',
        xaxis_title='Empleados en Proyecto',
        yaxis_title='Horas invertidas',
        bargap=0.15
    )
    
    graph_html = fig.to_html(full_html=False)

    return HTMLResponse(content=graph_html)

app.include_router(dash)

##################### Dashboard Timesheet Financiero #############################3
if cursor is None:
    raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

@dash.post('/timesheetHoraAreaEmp/', tags=["Dashboards"])
def timesheet_horasarea_emp(
    proyecto: Optional[str] = None,
    mes: Optional[int] = None,
    anio: Optional[int] = None
):
    query = """
        select 
        e.name as "Empleado",
                sum(
            coalesce(cast(nullif(th.horas_lunes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_martes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_miercoles, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_jueves, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_viernes, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_sabado, '') as numeric), 0) +
            coalesce(cast(nullif(th.horas_domingo, '') as numeric), 0)
        ) as "Horas trabajadas en proyecto"
        from timesheet_proyectos tp 
        left join timesheet_tareas tt on tp.id=tt.proyecto_id  
        inner join timesheet_horas th on tt.id =th.tarea_id 
        inner join empleados e on th.empleado_id =e.id
        left join areas a on e.area_id =a.id
        where 1=1
    """
    if proyecto:
        query += f" and tp.proyecto = '{proyecto}'"
    if mes and anio:
        query += f" and extract(month from th.fecha_dia) = {mes} and extract(year from th.fecha_dia) = {anio}"

    query += """
        group by 
            a.area,
            e.name,
            tp.proyecto
        order by a.area
    """   

    file_path = "query.txt"
    with open(file_path, "w") as file:
        file.write(query)


    
    def ejecutar_consulta_sql(cursor, consulta):
        try:
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(resultados, columns=colnames)
            return df
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail="Error al ejecutar la consulta SQL: " + str(e))
    
    df = ejecutar_consulta_sql(cursor, query)
    
    # Crear la gráfica de barras
    fig = go.Figure(data=[
        go.Bar(name='Registros de horas trabajadas por Área', x=df['Empleado'], y=df['Horas trabajadas en proyecto'])
    ])
    
    # Actualizar el layout de la gráfica
    fig.update_layout(
        title='Horas Trabajadas en Proyecto',
        xaxis_title='Empleados en Proyecto',
        yaxis_title='Horas invertidas',
        bargap=0.15
    )
    
    graph_html = fig.to_html(full_html=False)

    return HTMLResponse(content=graph_html)

app.include_router(dash)