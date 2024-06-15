import plotly.graph_objects as go
import pandas as pd
import psycopg2
from fastapi import HTTPException
from config.database import conexion, cursor
 
# Verificar si la conexión es exitosa antes de continuar
if cursor is None:
    raise HTTPException(status_code=500, detail="No se pudo establecer la conexión a la base de datos")
 
def registros_timesheetMes_dona():
    query = """
        select
            sum(case when t.estatus = 'aprobado' then 1 else 0 end) as "Aprobado",
            sum(case when t.estatus = 'rechazado' then 1 else 0 end) as "Rechazado",
            sum(case when t.estatus = 'pendiente' then 1 else 0 end) as "Pendiente",
            sum(case when t.estatus = 'borrador' then 1 else 0 end) as "Borrador",
            count(*) as "Registros Totales"
        from timesheet t
        where t.estatus IN ('aprobado', 'rechazado')
            and t.fecha_dia BETWEEN CURRENT_DATE - INTERVAL '1 MONTH' AND CURRENT_DATE;
    """

    df = pd.read_sql(query, conexion)
    
    labels = df[''].tolist()  #Áreas
    values = df['Registros Totales'].tolist()  # Valores correspondientes a cada estatus

    # Crear la gráfica de dona
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    # Actualizar el layout de la gráfica
    fig.update_layout(
        title='Registros de Timesheet del mes',
        annotations=[dict(text=' ', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    # Mostrar la gráfica
    fig.show()
 
# Llamar a la función para generar y mostrar la gráfica
registros_timesheetMes_dona()



# Cerrar la conexión a la base de datos
cursor.close()
conexion.close()


    

