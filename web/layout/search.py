from dash import html, dcc, dash_table

def get_search_layout(df, theme):
    return html.Div([
    html.H2("ค้นหาหลักสูตรที่เหมาะสม", style={'textAlign': 'center'}),
    html.Div([], style={'height': '10px'}),  # placeholder spacing only   

    # ครอบ 3 แถว dropdown ด้วย div นี้ กำหนดกึ่งกลางและจัดเรียงแนวตั้ง
    html.Div([
        html.Div([
            # แถว 1
            html.Div([
                html.Label("คำค้น (หลักสูตร):"),
                dcc.Dropdown(
                    id='search-keyword',
                    options=[{'label': 'ทั้งหมด', 'value': 'all'}] +
                            [{'label': k, 'value': k} for k in sorted(df['คำค้น'].dropna().unique())],
                    value='all',
                    clearable=False,
                    style={'width': '100%'}
                )
            ], style={'width': '30%'}),

            html.Div([
                html.Label("มหาวิทยาลัย:"),
                dcc.Dropdown(
                    id='search-university',
                    options=[{'label': 'ทั้งหมด', 'value': 'all'}] +
                            [{'label': u, 'value': u} for u in sorted(df['มหาวิทยาลัย'].dropna().unique())],
                    value='all',
                    clearable=False,
                    style={'width': '100%'}
                )
            ], style={'width': '30%'}),

            html.Div([
                html.Label("คณะ:"),
                dcc.Dropdown(
                    id='search-faculty',
                    options=[{'label': 'ทั้งหมด', 'value': 'all'}] +
                            [{'label': f, 'value': f} for f in sorted(df['คณะ'].dropna().unique())],
                    value='all',
                    clearable=False,
                    style={'width': '100%'}
                )
            ], style={'width': '30%'}),
        ], style={'display': 'flex', 'gap': '20px', 'justifyContent': 'center', 'marginBottom': '15px'}),

        # แถว 2
        html.Div([
            html.Div([
                html.Label("สาขา:"),
                dcc.Dropdown(
                    id='search-department',
                    options=[{'label': 'ทั้งหมด', 'value': 'all'}] +
                            [{'label': d, 'value': d} for d in sorted(df['สาขา'].dropna().unique())],
                    value='all',
                    clearable=False,
                    style={'width': '100%'}
                )
            ], style={'width': '30%'}),

            html.Div([
                html.Label("ประเภทหลักสูตร:"),
                dcc.Dropdown(
                    id='search-type',
                    options=[{'label': 'ทั้งหมด', 'value': 'all'}] +
                            [{'label': t, 'value': t} for t in sorted(df['ประเภทหลักสูตร'].dropna().unique())],
                    value='all',
                    clearable=False,
                    style={'width': '100%'}
                )
            ], style={'width': '30%'}),

            html.Div([
                html.Label("ภาค:"),
                dcc.Dropdown(
                    id='search-region',
                    options=[{'label': 'ทั้งหมด', 'value': 'all'}] +
                            [{'label': r, 'value': r} for r in sorted(df['ภาค'].dropna().unique())],
                    value='all',
                    clearable=False,
                    style={'width': '100%'}
                )
            ], style={'width': '30%'}),
        ], style={'display': 'flex', 'gap': '20px', 'justifyContent': 'center', 'marginBottom': '20px'}),

        # แถว 3
        html.Div([
            html.Div([
                html.Label("ค่าเทอมขั้นต่ำ:"),
                dcc.Input(id='min-fee-input', type='number', value=df['ค่าเทอม'].min(), style={'width': '100%'})
            ], style={'width': '30%'}),
            html.Div([
                html.Label("ค่าเทอมสูงสุด:"),
                dcc.Input(id='max-fee-input', type='number', value=df['ค่าเทอม'].max(), style={'width': '100%'})
            ], style={'width': '30%'}),
            html.Div([
                html.Label("เรียงตามค่าเทอม:"),
                dcc.Dropdown(
                    id='sort-order',
                    options=[
                        {'label': 'สูง → ต่ำ', 'value': 'desc'},
                        {'label': 'ต่ำ → สูง', 'value': 'asc'}
                    ],
                    value='asc',
                    clearable=False,
                    style={'width': '100%'}
                )
            ], style={'width': '30%'}),
        ], style={'display': 'flex', 'gap': '20px', 'justifyContent': 'center', 'marginBottom': '30px'}),
    ], style={'maxWidth': '1280px', 'margin': '0 auto', 'display': 'flex', 'flexDirection': 'column', 'gap': '15px'}),


    # ตารางแสดงผลหลักสูตรตามเงื่อนไข
    html.Div([
        dash_table.DataTable(
            id='search-table',
            columns=[
                {"name": "มหาวิทยาลัย", "id": "มหาวิทยาลัย"},
                {"name": "หลักสูตร", "id": "หลักสูตร"},
                {"name": "ประเภทหลักสูตร", "id": "ประเภทหลักสูตร"},
                {"name": "ค่าเทอม", "id": "ค่าเทอม"}
            ],
            page_size=10,
            style_table={
                'overflowX': 'auto',
                'width': '100%',
            },
            style_cell={
                'textAlign': 'left',
                'padding': '12px',
                'fontFamily': 'Arial',
                'fontSize': '15px',
                'whiteSpace': 'normal',
            },
            style_header={
                'backgroundColor': '#003C71',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'left',
                'fontSize': '16px',
                'padding': '14px'
            },
            style_data={
                'backgroundColor': 'white',
                'color': '#333',
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': "#edf5f8"
                }
            ],
            style_as_list_view=True,
            row_selectable="multi",
            selected_rows=[],
        )
    ], style={
        'backgroundColor': theme['card'],
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.05)',
        'width': '100%',
        'maxWidth': '1280px',
        'margin': '0 auto',
        'marginBottom': '30px'
    }),

    # ตารางสำหรับแสดงหลักสูตรที่ผู้ใช้เลือกและลากจัดอันดับได้
    html.Div([
        html.H4("10 อันดับหลักสูตรที่สนใจ"),
        dash_table.DataTable(
            id='selected-rank-table',
            columns=[
                {"name": "อันดับ", "id": "อันดับ"},                
                {"name": "มหาวิทยาลัย", "id": "มหาวิทยาลัย"},
                {"name": "หลักสูตร", "id": "หลักสูตร"},
                {"name": "ประเภทหลักสูตร", "id": "ประเภทหลักสูตร"},
                {"name": "ค่าเทอม", "id": "ค่าเทอม"}
            ],
            data=[],
            row_deletable=True,
            style_table={'overflowX': 'auto', 'width': '100%'},
            style_cell={
                'textAlign': 'left',
                'padding': '12px',
                'fontFamily': 'Arial',
                'fontSize': '15px',
                'whiteSpace': 'normal',
            },
            style_header={
                'backgroundColor': '#005f9e',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'left',
                'fontSize': '16px',
                'padding': '14px'
            },
            style_data={
                'backgroundColor': 'white',
                'color': '#333',
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': "#edf5f8"
                }
            ],
            style_as_list_view=True,
            selected_rows=[],
            editable=False,
            page_action='native',
            page_current=0,
            page_size=10,
            sort_action='none',
            filter_action='none',
            ),
    html.Br(),
    html.Button("Export 10 อันดับหลักสูตรเป็น Excel", id="export-button"),
    dcc.Download(id="download-dataframe-xlsx"),
    ], style={
        'backgroundColor': theme['card'],
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.05)',
        'width': '100%',
        'maxWidth': '1280px',
        'margin': '0 auto',
    }),

])