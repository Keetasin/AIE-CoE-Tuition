from dash import html, dcc

def get_overview_layout(df, theme):
    return html.Div([
    html.H2("ภาพรวมค่าเทอมของหลักสูตร", style={'textAlign': 'center'}),
    html.Div([], style={'height': '10px'}),   
    html.Div([
        html.Div([
            html.Label("เลือกประเภทหลักสูตร:"),
            dcc.Dropdown(
                id='overview-type-filter',
                options=[{'label': 'ทั้งหมด', 'value': 'all'}] +
                        [{'label': t, 'value': t} for t in sorted(df['ประเภทหลักสูตร'].dropna().unique())],
                value='all',
                clearable=False,
                style={'width': '100%'}
            )
        ], style={'width': '33%'}),

        html.Div([
            html.Label("เลือกหลักสูตร:"),
            dcc.Dropdown(
                id='overview-keyword-filter',
                options=[{'label': 'ทั้งหมด', 'value': 'all'}] +
                        [{'label': k, 'value': k} for k in sorted(df['คำค้น'].dropna().unique())],
                value='all',
                clearable=False,
                style={'width': '100%'}
            )
        ], style={'width': '33%'}),

        html.Div([
            html.Label("เลือกภาค:"),
            dcc.Dropdown(
                id='overview-region-filter',
                options=[{'label': 'ทั้งประเทศ', 'value': 'all'}] +
                        [{'label': region, 'value': region} for region in sorted(df['ภาค'].dropna().unique())],
                value='all',
                clearable=False,
                style={'width': '100%'}
            )
        ], style={'width': '33%'}),

    ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '30px'}),

    html.Div([
        dcc.Loading(dcc.Graph(id='histogram-overview')),
        dcc.Loading(dcc.Graph(id='boxplot-overview'))
    ], style={'display': 'flex', 'gap': '40px'}),


    html.Div([
        html.Div([
            html.H4("📃 จำนวนหลักสูตร", style={'color': theme['primary']}),
            html.P(id='count-programs', style={'fontSize': '20px', 'fontWeight': 'bold'})
        ], style={
            'backgroundColor': theme['card'],
            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
            'borderRadius': '12px',
            'padding': '16px',
            'width': '19%',
            'textAlign': 'center'
        }),
        html.Div([
            html.H4("➗ ค่าเฉลี่ย", style={'color': theme['primary']}),
            html.P(id='mean-fee', style={'fontSize': '20px', 'fontWeight': 'bold'})
        ], style={
            'backgroundColor': theme['card'],
            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
            'borderRadius': '12px',
            'padding': '16px',
            'width': '19%',
            'textAlign': 'center'
        }),
        html.Div([
            html.H4("🔺 ค่าสูงสุด", style={'color': theme['primary']}),
            html.P(id='max-fee', style={'fontSize': '20px', 'fontWeight': 'bold'})
        ], style={
            'backgroundColor': theme['card'],
            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
            'borderRadius': '12px',
            'padding': '16px',
            'width': '19%',
            'textAlign': 'center'
        }),
        html.Div([
            html.H4("🔻 ค่าต่ำสุด", style={'color': theme['primary']}),
            html.P(id='min-fee', style={'fontSize': '20px', 'fontWeight': 'bold'})
        ], style={
            'backgroundColor': theme['card'],
            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
            'borderRadius': '12px',
            'padding': '16px',
            'width': '19%',
            'textAlign': 'center'
        }),
        html.Div([
            html.H4("⚖️ มัธยฐาน", style={'color': theme['primary']}),
            html.P(id='median-fee', style={'fontSize': '20px', 'fontWeight': 'bold'})
        ], style={
            'backgroundColor': theme['card'],
            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
            'borderRadius': '12px',
            'padding': '16px',
            'width': '19%',
            'textAlign': 'center'
        }),
    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'gap': '10px',
        'flexWrap': 'nowrap',
        'marginTop': '30px'
    })
])