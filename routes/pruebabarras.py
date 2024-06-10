import plotly.graph_objects as go

animals=['giraffes', 'orangutans', 'monkeys']

fig = go.Figure(data=[
    go.Bar(name='SF Zoo', y=animals, x=[20, 14, 23], orientation='h'),
    go.Bar(name='LA Zoo', y=animals, x=[12, 18, 29], orientation='h'),
    go.Bar(name='DF Zoo', y=animals, x=[20, 18, 27], orientation='h'),
    go.Bar(name='MY Zoo', y=animals, x=[29, 4, 13], orientation='h')
])
# Change the bar mode
fig.update_layout(barmode='group')
fig.show()



# Dona
labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
values = [4500, 2500, 1053, 500]

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig.show()