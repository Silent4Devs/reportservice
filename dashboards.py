import plotly.graph_objects as go
import pandas as pd
import psycopg2
from fastapi import HTTPException
from config.database import conexion, cursor
 
# Verificar si la conexión es exitosa antes de continuar
if cursor is None:
    raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")
 
# Definir el query
query = """
SELECT
    count(case when t.estatus = 'aprobado' then 1 end) as "Aprobado",
    count(case when t.estatus = 'pendiente' then 1 end) as "Pendiente",
    count(case when t.estatus = 'rechazado' then 1 end) as "Rechazado",
    count(case when t.estatus = 'borrador' then 1 end) as "Borrador",
    a.area as "Área"
FROM timesheet t
INNER JOIN empleados e on t.empleado_id = e.id
INNER JOIN areas a on e.area_id = a.id
GROUP BY a.area
"""
 
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
    xaxis_title='Cantidad',
    yaxis_title='Área',
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1
)
 
# Mostrar la gráfica
fig.show()    

 ################################################

 
def registros_timesheetarea_dona():
    # Definir el query para la segunda gráfica
    query = """
        SELECT
            count(case when t.estatus = 'aprobado' then 1 end) as "Aprobado",
            count(case when t.estatus = 'pendiente' then 1 end) as "Pendiente",
            count(case when t.estatus = 'rechazado' then 1 end) as "Rechazado",
            count(case when t.estatus = 'borrador' then 1 end) as "Borrador",
            a.area as "Área"
        FROM timesheet t
        INNER JOIN empleados e on t.empleado_id = e.id
        INNER JOIN areas a on e.area_id = a.id
        GROUP BY a.area
    """
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
    
    labels = df['Área']
    values_aprobado = df['Aprobado']
    values_pendiente = df['Pendiente']
    values_rechazado = df['Rechazado']
    values_borrador = df['Borrador']

    values = values_aprobado + values_pendiente + values_rechazado + values_borrador
    status_labels = ['Aprobado'] * len(values_aprobado) + ['Pendiente'] * len(values_pendiente) + ['Rechazado'] * len(values_rechazado) + ['Borrador'] * len(values_borrador)
    
    # Crear la gráfica de dona
    fig2 = go.Figure(data=[go.Pie(labels=status_labels, values=values, hole=.3)])
    
    # Actualizar el diseño de la gráfica
    fig2.update_layout(
        title='Estatus por Área',
        annotations=[dict(text='Timesheet', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
   
    fig2.show()



# Cerrar la conexión a la base de datos
cursor.close()
conexion.close()

