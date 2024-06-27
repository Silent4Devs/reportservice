import plotly.graph_objects as go
import pandas as pd
import psycopg2
from fastapi import HTTPException, FastAPI
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.database import conexion, cursor

app=FastAPI()
dash= APIRouter()
# Verificar si la conexión es exitosa antes de continuar

# if cursor is None:
#     raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")


# def registros_timesheet_estatus(): 
#     # Definir el query
#     query = """
#     SELECT
#         count(case when t.estatus = 'aprobado' then 1 end) as "Aprobado",
#         count(case when t.estatus = 'pendiente' then 1 end) as "Pendiente",
#         count(case when t.estatus = 'rechazado' then 1 end) as "Rechazado",
#         count(case when t.estatus = 'borrador' then 1 end) as "Borrador",
#         a.area as "Área"
#     FROM timesheet t
#     INNER JOIN empleados e on t.empleado_id = e.id
#     INNER JOIN areas a on e.area_id = a.id
#     GROUP BY a.area
#     """
    
#     # Ejecutar la consulta SQL y obtener los datos
#     def ejecutar_consulta_sql(cursor, consulta):
#         try:
#             cursor.execute(consulta)
#             resultados = cursor.fetchall()
#             colnames = [desc[0] for desc in cursor.description]
#             df = pd.DataFrame(resultados, columns=colnames)
#             return df
#         except psycopg2.Error as e:
#             raise HTTPException(status_code=500, detail="Error al ejecutar la consulta SQL: " + str(e))
    
#     df = ejecutar_consulta_sql(cursor, query)
    
#     # Crear la gráfica
#     fig = go.Figure(data=[
#         go.Bar(name='Aprobado', y=df['Área'], x=df['Aprobado'], orientation='h'),
#         go.Bar(name='Pendiente', y=df['Área'], x=df['Pendiente'], orientation='h'),
#         go.Bar(name='Rechazado', y=df['Área'], x=df['Rechazado'], orientation='h'),
#         go.Bar(name='Borrador', y=df['Área'], x=df['Borrador'], orientation='h')
#     ])
    
#     # Actualizar el diseño de la gráfica
#     fig.update_layout(
#         title='Estatus por Área',
#         xaxis_title='Registros de timesheet',
#         yaxis_title='Área',
#         barmode='group',
#         bargap=0.15,
#         bargroupgap=0.1
#     )
#     fig.show()
# registros_timesheet_estatus()
    
#     # graph_json = fig.to_json()
#     # return graph_json

# # @dash.get("/timesheet_estatus")
# # def get_timesheet_estatus():
# #     try:
# #         graph_json = registros_timesheet_estatus()
# #         return JSONResponse(content=graph_json)
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# ################################################

 
# if cursor is None:
#     raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

# def registros_timesheet_area():
#     query = """
#                 select
#                 a.area as "Área",
#                 sum(
#                     coalesce(cast(nullif(th.horas_lunes, '') as numeric), 0) +
#                     coalesce(cast(nullif(th.horas_martes, '') as numeric), 0) +
#                     coalesce(cast(nullif(th.horas_miercoles, '') as numeric), 0) +
#                     coalesce(cast(nullif(th.horas_jueves, '') as numeric), 0) +
#                     coalesce(cast(nullif(th.horas_viernes, '') as numeric), 0) +
#                     coalesce(cast(nullif(th.horas_sabado, '') as numeric), 0) +
#                     coalesce(cast(nullif(th.horas_domingo, '') as numeric), 0)
#                 ) as "Horas del área"
#                 from timesheet t
#                 inner join empleados e on t.empleado_id = e.id
#                 inner join areas a on e.area_id = a.id
#                 left join timesheet_horas th on t.id=th.timesheet_id 
#                 group by a.area
#     """
    
#     def ejecutar_consulta_sql(cursor, consulta):
#         try:
#             cursor.execute(consulta)
#             resultados = cursor.fetchall()
#             colnames = [desc[0] for desc in cursor.description]
#             df = pd.DataFrame(resultados, columns=colnames)
#             return df
#         except psycopg2.Error as e:
#             raise HTTPException(status_code=500, detail="Error al ejecutar la consulta SQL: " + str(e))
    
#     df = ejecutar_consulta_sql(cursor, query)
    
#     # Crear la gráfica de barras
#     fig = go.Figure(data=[
#         go.Bar(name='Registros de horas trabajadas por Área', x=df['Área'], y=df['Horas del área'])
#     ])
    
#     # Actualizar el layout de la gráfica
#     fig.update_layout(
#         title='Horas por Área',
#         xaxis_title='Área',
#         yaxis_title='Horas del área',
#         bargap=0.15
#     )
    
#     # Mostrar la gráfica
#     fig.show()
# registros_timesheet_area()


# ################################################

# if cursor is None:
#     raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")
 
# def registros_timesheet_status_dona():
#     query = """
#         SELECT
#             sum(case when t.estatus = 'aprobado' then 1 else 0 end) as "Aprobado",
#             sum(case when t.estatus = 'pendiente' then 1 else 0 end) as "Pendiente",
#             sum(case when t.estatus = 'rechazado' then 1 else 0 end) as "Rechazado",
#             sum(case when t.estatus = 'borrador' then 1 else 0 end) as "Borrador"
#         FROM timesheet t;
#     """
#     df = pd.read_sql(query, conexion)
    
#     labels = df.columns.tolist()  #Estatus
#     values = df.iloc[0].tolist()  # Valores correspondientes a cada estatus

#     # Crear la gráfica de dona
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

#     # Actualizar el layout de la gráfica
#     fig.update_layout(
#         title='Registros de Timesheet por Estatus',
#         annotations=[dict(text=' ', x=0.5, y=0.5, font_size=20, showarrow=False)]
#     )

#     # Mostrar la gráfica
#     fig.show()
 
# # Llamar a la función para generar y mostrar la gráfica
# registros_timesheet_status_dona()

# ######################################### Crear filtros
# if cursor is None:
#     raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

# def registros_tsempleados_estatus(): 
#     # Definir el query
#     query = """
#             select e.name as "Empleado",
#             a.area as "Área",
#             sum(case when t.estatus = 'aprobado' then 1 else 0 end) as "Aprobado",
#             sum(case when t.estatus = 'pendiente' then 1 else 0 end) as "Pendiente",
#             sum(case when t.estatus = 'rechazado' then 1 else 0 end) as "Rechazado",
#             sum(case when t.estatus = 'borrador' then 1 else 0 end) as "Borrador"
#             from timesheet t
#             left join empleados e on t.empleado_id = e.id
#             inner join areas a on e.area_id = a.id
#             left join timesheet_horas th on t.id=th.timesheet_id 
#             group by e.name, a.area 
#     """
    
#     # Ejecutar la consulta SQL y obtener los datos
#     def ejecutar_consulta_sql(cursor, consulta):
#         try:
#             cursor.execute(consulta)
#             resultados = cursor.fetchall()
#             colnames = [desc[0] for desc in cursor.description]
#             df = pd.DataFrame(resultados, columns=colnames)
#             return df
#         except psycopg2.Error as e:
#             raise HTTPException(status_code=500, detail="Error al ejecutar la consulta SQL: " + str(e))
    
#     df = ejecutar_consulta_sql(cursor, query)
    
#     # Crear la gráfica
#     fig = go.Figure(data=[
#         go.Bar(name='Aprobado', y=df['Empleado'], x=df['Aprobado'], orientation='h'),
#         go.Bar(name='Pendiente', y=df['Empleado'], x=df['Pendiente'], orientation='h'),
#         go.Bar(name='Rechazado', y=df['Empleado'], x=df['Rechazado'], orientation='h'),
#         go.Bar(name='Borrador', y=df['Empleado'], x=df['Borrador'], orientation='h')
#     ])
    
#     # Actualizar el diseño de la gráfica
#     fig.update_layout(
#         title='Estatus Empleado por Área',
#         xaxis_title='Registros de timesheet',
#         yaxis_title='Empleado',
#         barmode='group',
#         bargap=0.15,
#         bargroupgap=0.1
#     )
    
#     # Mostrar la gráfica
#     fig.show()    
# registros_tsempleados_estatus()

# #################################################

# if cursor is None:
#     raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")
 
# def registros_timesheetArea_dona():
#     query = """
#                 select
#                 a.area as "Área",
#                 sum(
#                     coalesce(cast(nullif(th.horas_lunes, '') as numeric), 0) +
#                     coalesce(cast(nullif(th.horas_martes, '') as numeric), 0) +
#                     coalesce(cast(nullif(th.horas_miercoles, '') as numeric), 0) +
#                     coalesce(cast(nullif(th.horas_jueves, '') as numeric), 0) +
#                     coalesce(cast(nullif(th.horas_viernes, '') as numeric), 0) +
#                     coalesce(cast(nullif(th.horas_sabado, '') as numeric), 0) +
#                     coalesce(cast(nullif(th.horas_domingo, '') as numeric), 0)
#                 ) as "Horas del área"
#                 from timesheet t
#                 inner join empleados e on t.empleado_id = e.id
#                 inner join areas a on e.area_id = a.id
#                 left join timesheet_horas th on t.id=th.timesheet_id 
#                 group by a.area
#     """

#     df = pd.read_sql(query, conexion)
    
#     labels = df['Área'].tolist()  
#     values = df['Horas del área'].tolist()  

#     # Crear la gráfica de dona
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

#     # Actualizar el layout de la gráfica
#     fig.update_layout(
#         title='Registros de Timesheet por Área',
#         annotations=[dict(text=' ', x=0.5, y=0.5, font_size=20, showarrow=False)]
#     )

#     # Mostrar la gráfica
#     fig.show()
 
# # Llamar a la función para generar y mostrar la gráfica
# registros_timesheetArea_dona()

# #################################################

# if cursor is None:
#     raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")
 
# def registros_timesheetMes_dona():
#     query = """
#         select
#             sum(case when t.estatus = 'aprobado' then 1 else 0 end) as "Registros Aprobados",
#             sum(case when t.estatus = 'rechazado' then 1 else 0 end) as "Registros Rechazados",
#             sum(case when t.estatus = 'pendiente' then 1 else 0 end) as "Pendiente",
#             sum(case when t.estatus = 'borrador' then 1 else 0 end) as "Borrador",
#             count(*) as "Registros Totales"
#         from (
#         select *
#         from timesheet t
#         where t.fecha_dia BETWEEN CURRENT_DATE - INTERVAL '1 MONTH' AND CURRENT_DATE
#         )t
#         where t.estatus IN ('aprobado', 'rechazado')        
#     """

#     df = pd.read_sql(query, conexion)
    
#     labels = df.columns.tolist()
#     values = df.iloc[0].tolist()  

#     # Crear la gráfica de dona
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

#     # Actualizar el layout de la gráfica
#     fig.update_layout(
#         title='Registros de Timesheet del mes',
#         annotations=[dict(text=' ', x=0.5, y=0.5, font_size=20, showarrow=False)]
#     )

#     # Mostrar la gráfica
#     fig.show()
 
# # Llamar a la función para generar y mostrar la gráfica
# registros_timesheetMes_dona()

###############  Timesheet Proyectos #######################
# if cursor is None:
#     raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

# def timesheet_proyectos_area(cursor): 
#     # Definir el query
#     query = """
#         select 
#         a.area as "Áreas",
#         count(tt.tarea) as "Tareas Asignadas del Proyecto" ,
#         sum(
#             coalesce(cast(nullif(th.horas_lunes, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_martes, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_miercoles, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_jueves, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_viernes, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_sabado, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_domingo, '') as numeric), 0)
#         ) as "Horas invertidas"
#         from timesheet_proyectos tp 
#         inner join timesheet_tareas tt on tp.id=tt.proyecto_id 
#         inner join areas a on tt.area_id=a.id 
#         inner join timesheet_horas th on tt.id =th.tarea_id 
#         group by a.area
#         order by a.area
#     """
    
#     # Ejecutar la consulta SQL y obtener los datos
#     def ejecutar_consulta_sql(cursor, consulta):
#         try:
#             cursor.execute(consulta)
#             resultados = cursor.fetchall()
#             colnames = [desc[0] for desc in cursor.description]
#             df = pd.DataFrame(resultados, columns=colnames)
#             return df
#         except psycopg2.Error as e:
#             raise HTTPException(status_code=500, detail="Error al ejecutar la consulta SQL: " + str(e))
    
#     df = ejecutar_consulta_sql(cursor, query)
 
#     # Crear la gráfica
#     fig = go.Figure(data=[
#         go.Bar(name='Horas invertidas', y=df['Áreas'], x=df['Horas invertidas'], orientation='h'),
#         go.Bar(name='Tareas Asignadas del Proyecto', y=df['Áreas'], x=df['Tareas Asignadas del Proyecto'], orientation='h')
#     ])
    
#     # Actualizar el diseño de la gráfica
#     fig.update_layout(
#         title='Proyectos',
#         xaxis_title='Horas Trabajadas en el Proyecto',
#         yaxis_title='Área',
#         barmode='group',
#         bargap=0.15,
#         bargroupgap=0.1
#     )
#     fig.show()
# timesheet_proyectos_area(cursor)


#############################
# if cursor is None:
#     raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")
 
# def timesheet_horas_area_dona():
#     query = """
#         select 
#         a.area as "Áreas",
#         tp.proyecto as "Proyecto",
#         count(tt.tarea) as "Tareas Asignadas" ,
#         sum(
#             coalesce(cast(nullif(th.horas_lunes, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_martes, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_miercoles, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_jueves, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_viernes, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_sabado, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_domingo, '') as numeric), 0)
#         ) as "Horas invertidas"
#         from timesheet_proyectos tp 
#         inner join timesheet_tareas tt on tp.id=tt.proyecto_id 
#         inner join areas a on tt.area_id=a.id 
#         inner join timesheet_horas th on tt.id =th.tarea_id 
#         group by a.area, tp.proyecto 
#         order by a.area
#     """
#     df = pd.read_sql(query, conexion)
    
#     labels = df['Áreas'].tolist()  
#     values = df['Horas invertidas'].tolist() 

#     # Crear la gráfica de dona
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

#     # Actualizar el layout de la gráfica
#     fig.update_layout(
#         title='Horas Invertidas en el Proyecto por Área',
#         annotations=[dict(text=' ', x=0.5, y=0.5, font_size=20, showarrow=False)]
#     )

#     # Mostrar la gráfica
#     fig.show()
 
# # Llamar a la función para generar y mostrar la gráfica
# timesheet_horas_area_dona()

# ################ 
# if cursor is None:
#     raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")
 
# def timesheet_horas_area_dona():
#     query = """
#         select 
#         a.area as "Áreas",
#         tp.proyecto as "Proyecto",
#         count(tt.tarea) as "Tareas Asignadas" ,
#         sum(
#             coalesce(cast(nullif(th.horas_lunes, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_martes, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_miercoles, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_jueves, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_viernes, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_sabado, '') as numeric), 0) +
#             coalesce(cast(nullif(th.horas_domingo, '') as numeric), 0)
#         ) as "Horas invertidas"
#         from timesheet_proyectos tp 
#         inner join timesheet_tareas tt on tp.id=tt.proyecto_id 
#         inner join areas a on tt.area_id=a.id 
#         inner join timesheet_horas th on tt.id =th.tarea_id 
#         group by a.area, tp.proyecto 
#         order by a.area
#     """
#     df = pd.read_sql(query, conexion)
    
#     labels = df['Áreas'].tolist()  
#     values = df['Tareas Asignadas'].tolist() 

#     # Crear la gráfica de dona
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

#     # Actualizar el layout de la gráfica
#     fig.update_layout(
#         title='Tareas en el Proyecto por Área',
#         annotations=[dict(text=' ', x=0.5, y=0.5, font_size=20, showarrow=False)]
#     )

#     # Mostrar la gráfica
#     fig.show()
 
# # Llamar a la función para generar y mostrar la gráfica
# timesheet_horas_area_dona()

## Horas trabajadas en proyecto por empleado (Barras verticales) 
if cursor is None:
    raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")

def timesheet_horasarea_emp():
    query = """
        select 
        concat(e.name, ' - ', a.area) AS "Empleado",
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
        where a.area='Arquitectura'
        group by e.name, a.area
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
    
    # Mostrar la gráfica
    fig.show()
timesheet_horasarea_emp()

# Cerrar la conexión a la base de datos
cursor.close()
conexion.close()

