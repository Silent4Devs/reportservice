import plotly.graph_objects as go
from config.database import *
import pandas as pd
import os

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


# Ejecutar la consulta y leer los datos en un DataFrame
df = pd.read_sql(query, cursor)
cursor.close()

fig = go.Figure(data=[
    go.Bar(name='Aprobado', y=df['Área'], x=df['Aprobado'], orientation='h'),
    go.Bar(name='Pendiente', y=df['Área'], x=df['Pendiente'], orientation='h'),
    go.Bar(name='Rechazado', y=df['Área'], x=df['Rechazado'], orientation='h'),
    go.Bar(name='Borrador', y=df['Área'], x=df['Borrador'], orientation='h')
])

# Crear la figura con Plotly
# fig = go.Figure(data=[
#     go.Bar(name='Aprobado', y=areas, x=aprobado, orientation='h'),
#     go.Bar(name='Pendiente', y=areas, x=pendiente, orientation='h'),
#     go.Bar(name='Rechazado', y=areas, x=rechazado, orientation='h'),
#     go.Bar(name='Borrador', y=areas, x=borrador, orientation='h')
# ])

# Cambiar el modo de las barras
fig.update_layout(barmode='group')

# Mostrar la figura
fig.show()

####################

query2="""
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
        ) as "Horas de la semana"
        from timesheet_horas th  
        inner join empleados e on th.empleado_id =e.id
        inner join areas a on e.area_id =a.id 
        group by a.area 
"""

labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
values = [4500, 2500, 1053, 500]

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig.show()