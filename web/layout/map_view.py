from dash import html, dcc

def get_map_layout(theme):
    return html.Div([
    html.H2("แผนที่มหาวิทยาลัยและค่าเทอม", style={'textAlign': 'center'}),
    html.Div([], style={'height': '15px'}),  # placeholder spacing only    
    dcc.Loading(dcc.Graph(id='map-graph', style={'height': '600px'})),
])
