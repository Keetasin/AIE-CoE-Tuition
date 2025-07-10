import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px

# =======================
# 📥 Load Data
# =======================
df = pd.read_excel("web/data/university_fee_with_latlon.xlsx")
df['ประเภทหลักสูตร'] = df['ประเภทหลักสูตร'].astype(str)

# =======================
# ⚙️ App Initialization
# =======================
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# =======================
# 🎨 Theme Configuration
# =======================
theme = {
    'background': '#f0f8ff',
    'card': '#ffffff',
    'primary': '#007acc',
    'text': '#003f5c',
    'accent': '#00bcd4'
}

# =======================
# 📊 Overview Layout
# =======================
overview_layout = html.Div([
    html.H2("📊 ภาพรวมค่าเทอมของหลักสูตร", style={'textAlign': 'center'}),
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
        dcc.Graph(id='histogram-overview'),
        dcc.Graph(id='boxplot-overview')
    ], style={'display': 'flex', 'gap': '40px'}),

    html.Div([
        html.Div([
            html.H4("📦 จำนวนหลักสูตร", style={'color': theme['primary']}),
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
            html.H4("🎯 ค่าเฉลี่ย", style={'color': theme['primary']}),
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

# =======================
# 🔍 Search Layout
# =======================
search_layout = html.Div([
    html.H2("🔎 ค้นหาหลักสูตรที่เหมาะสม", style={'textAlign': 'center'}),

    html.Div([
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
    ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '15px'}),

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
    ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}),

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
    ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '30px'}),

    dash_table.DataTable(
        id='search-table',
        columns=[
            {"name": "มหาวิทยาลัย", "id": "มหาวิทยาลัย"},
            {"name": "หลักสูตร", "id": "หลักสูตร"},
            {"name": "ประเภทหลักสูตร", "id": "ประเภทหลักสูตร"},
            {"name": "ค่าเทอม", "id": "ค่าเทอม"}
        ],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'}
    )
])


# =======================
# 🗺️ Map Layout
# =======================
map_layout = html.Div([
    html.H2("🗺️ แผนที่มหาวิทยาลัยและค่าเทอม", style={'textAlign': 'center'}),
    html.Div([
        html.Label("เลือกภาค:"),
        dcc.Dropdown(
            id='map-region-filter',
            options=[{'label': 'ทั้งหมด', 'value': 'all'}] +
                    [{'label': r, 'value': r} for r in sorted(df['ภาค'].dropna().unique())],
            value='all',
            clearable=False,
            style={'width': '300px', 'marginBottom': '20px'}
        ),
    ], style={'textAlign': 'center'}),
    
    dcc.Graph(id='map-graph', style={'height': '600px'}),
])


# =======================
# 🧭 App Layout (Tabs)
# =======================
app.layout = html.Div(style={
    'backgroundColor': theme['background'], 
    'fontFamily': 'Arial, sans-serif'
}, children=[
    html.H1("Dashboard วิเคราะห์ค่าเทอม", 
            style={
                'textAlign': 'center', 
                'color': theme['primary'],
                'padding': '20px'
            }),

    dcc.Tabs(id='tabs', value='overview', colors={
        "border": theme['accent'],
        "primary": theme['primary'],
        "background": theme['background']
    }, children=[
        dcc.Tab(label='📊 ภาพรวม', value='overview',
                style={'backgroundColor': theme['background'], 'color': theme['text']},
                selected_style={'backgroundColor': theme['card'], 'color': theme['primary']}),
        dcc.Tab(label='🔎 ค้นหาหลักสูตร', value='search',
                style={'backgroundColor': theme['background'], 'color': theme['text']},
                selected_style={'backgroundColor': theme['card'], 'color': theme['primary']}),
                dcc.Tab(label='🗺️ แผนที่มหาวิทยาลัย', value='map',
                style={'backgroundColor': theme['background'], 'color': theme['text']},
                selected_style={'backgroundColor': theme['card'], 'color': theme['primary']}),
    ]),
    html.Div(id='tabs-content', style={'padding': '20px'})
])

# =======================
# 🔄 Callbacks
# =======================
@app.callback(Output('tabs-content', 'children'), Input('tabs', 'value'))
def switch_tab(tab):
    if tab == 'overview':
        return overview_layout
    elif tab == 'search':
        return search_layout
    elif tab == 'map':
        return map_layout

@app.callback(
    Output('histogram-overview', 'figure'),
    Output('boxplot-overview', 'figure'),
    Output('mean-fee', 'children'),
    Output('max-fee', 'children'),
    Output('min-fee', 'children'),
    Output('median-fee', 'children'),
    Output('count-programs', 'children'),
    Input('overview-type-filter', 'value'),
    Input('overview-keyword-filter', 'value'),
    Input('overview-region-filter', 'value')  # เพิ่ม input ตัวนี้
)
def update_overview(type_selected, keyword_selected, region_selected):
    dff = df.copy()

    if type_selected != 'all':
        dff = dff[dff['ประเภทหลักสูตร'] == type_selected]

    if keyword_selected != 'all':
        dff = dff[dff['คำค้น'].str.contains(keyword_selected, case=False, na=False)]

    if region_selected != 'all':  # กรองภาค ถ้าเลือกไม่ใช่ "all"
        dff = dff[dff['ภาค'] == region_selected]

    hist_fig = px.histogram(dff, x='ค่าเทอม', nbins=20, color='ประเภทหลักสูตร',
                            title='การกระจายของค่าเทอมตามประเภทหลักสูตร')

    box_fig = px.box(dff, x='ประเภทหลักสูตร', y='ค่าเทอม',
                    title='Boxplot: ค่าเทอมตามประเภทหลักสูตร')

    count_programs = f"{len(dff):,} หลักสูตร"

    if not dff.empty:
        mean_fee = f"{dff['ค่าเทอม'].mean():,.0f} บาท"
        max_fee = f"{dff['ค่าเทอม'].max():,} บาท"
        min_fee = f"{dff['ค่าเทอม'].min():,} บาท"
        median_fee = f"{dff['ค่าเทอม'].median():,} บาท"
    else:
        mean_fee = max_fee = min_fee = median_fee = "ไม่มีข้อมูล"

    return hist_fig, box_fig, mean_fee, max_fee, min_fee, median_fee, count_programs

@app.callback(
    Output('search-table', 'data'),
    Input('search-keyword', 'value'),
    Input('search-university', 'value'),
    Input('search-faculty', 'value'),
    Input('search-department', 'value'),
    Input('search-type', 'value'),
    Input('search-region', 'value'),
    Input('min-fee-input', 'value'),
    Input('max-fee-input', 'value'),
    Input('sort-order', 'value')
)
def update_search_table(keyword, university, faculty, department, type_course, region, min_fee, max_fee, sort_order):
    dff = df.copy()

    if keyword != 'all':
        dff = dff[dff['คำค้น'].str.contains(keyword, case=False, na=False)]
    if university != 'all':
        dff = dff[dff['มหาวิทยาลัย'] == university]
    if faculty != 'all':
        dff = dff[dff['คณะ'] == faculty]
    if department != 'all':
        dff = dff[dff['สาขา'] == department]
    if type_course != 'all':
        dff = dff[dff['ประเภทหลักสูตร'] == type_course]
    if region != 'all':
        dff = dff[dff['ภาค'] == region]

    dff = dff[(dff['ค่าเทอม'] >= min_fee) & (dff['ค่าเทอม'] <= max_fee)]
    dff = dff.sort_values(by='ค่าเทอม', ascending=(sort_order == 'asc'))

    return dff.to_dict('records')


@app.callback(
    Output('map-graph', 'figure'),
    Input('map-region-filter', 'value')
)
def update_map(region):
    dff = df.copy()

    # กรองภาค
    if region != 'all':
        dff = dff[dff['ภาค'] == region]

    # ลบ NaN lat/lon
    dff = dff.dropna(subset=['Latitude', 'Longitude'])

    # รวมข้อมูลหลักสูตรและค่าเทอมในรูปแบบที่ต้องการ
    def format_programs(group):
        lines = []
        for _, row in group.iterrows():
            lines.append(f"- {row['หลักสูตร']}<br>&nbsp;&nbsp;ค่าเทอม: {row['ค่าเทอม']:,} บาท")
        return "<br>".join(lines)

    grouped = dff.groupby(['มหาวิทยาลัย', 'Latitude', 'Longitude', 'ภาค']).apply(lambda g: pd.Series({
        'ข้อมูลหลักสูตร': format_programs(g),
        'ค่าเทอมเฉลี่ย': g['ค่าเทอม'].mean(),
        'ค่าเทอมต่ำสุด': g['ค่าเทอม'].min(),
        'ค่าเทอมสูงสุด': g['ค่าเทอม'].max(),
        'จำนวนหลักสูตร': len(g)
    })).reset_index()

    # ใส่ customdata เพื่อใช้ใน hovertemplate
    grouped['customdata'] = grouped.apply(lambda row: [
        row['ภาค'],
        row['ข้อมูลหลักสูตร'],
        f"{row['ค่าเทอมเฉลี่ย']:,.0f} บาท",
        f"{row['ค่าเทอมต่ำสุด']:,.0f} บาท",
        f"{row['ค่าเทอมสูงสุด']:,.0f} บาท",
        row['จำนวนหลักสูตร']
    ], axis=1)

    fig = px.scatter_mapbox(
        grouped,
        lat="Latitude",
        lon="Longitude",
        color="ค่าเทอมเฉลี่ย",
        size="จำนวนหลักสูตร",
        size_max=20,
        zoom=5,
        title="แผนที่มหาวิทยาลัยและหลักสูตรทั้งหมด",
        color_continuous_scale=px.colors.sequential.Plasma
    )

    fig.update_traces(
        customdata=grouped['customdata'],
        hovertemplate=
            "<b>%{hovertext}</b><br><br>" +
            "จำนวนหลักสูตร: %{customdata[5]} หลักสูตร<br>" +
            "หลักสูตร:<br>%{customdata[1]}<br><br>" +
            "ค่าเทอมเฉลี่ย: %{customdata[2]}<br>" +
            "ต่ำสุด: %{customdata[3]}<br>" +
            "สูงสุด: %{customdata[4]}<br>" +
            "<extra></extra>",
        hovertext=grouped["มหาวิทยาลัย"]
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

    return fig




# =======================
# 🚀 Run Server
# =======================
if __name__ == '__main__':
    app.run(debug=True)
