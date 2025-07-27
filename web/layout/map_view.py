from dash import html, dcc

def get_map_layout(theme):
    return html.Div([
        html.H2("แผนที่มหาวิทยาลัยและค่าเทอม", style={'textAlign': 'center'}),
        html.Div([], style={'height': '15px'}), 

        html.Div([
            html.Label("เลือกมหาวิทยาลัย:", style={'marginRight': '10px'}),
            dcc.Dropdown(
                id='university-dropdown',
                placeholder="เลือกมหาวิทยาลัย (หรือปล่อยว่างเพื่อดูทั้งหมด)",
                multi=True,
                style={'width': '100%'}
            )
        ], style={'marginBottom': '20px'}),

        dcc.Loading(dcc.Graph(id='map-graph', style={'height': '600px'})),
    ])
