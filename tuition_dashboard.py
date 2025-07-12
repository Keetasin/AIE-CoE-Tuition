import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table, State
from dash.exceptions import PreventUpdate
from dash import callback_context
from dash import callback_context
import plotly.express as px
import io

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
    'text': '#003C71',
    'accent': '#00bcd4'
}

# =======================
# 📊 Overview Layout
# =======================
overview_layout = html.Div([
    html.H2("ภาพรวมค่าเทอมของหลักสูตร", style={'textAlign': 'center'}),
    html.Div([], style={'height': '10px'}),  # placeholder spacing only   
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




# =======================
# 🗺️ Map Layout
# =======================
map_layout = html.Div([
    html.H2("แผนที่มหาวิทยาลัยและค่าเทอม", style={'textAlign': 'center'}),
    html.Div([], style={'height': '15px'}),  # placeholder spacing only    
    dcc.Loading(dcc.Graph(id='map-graph', style={'height': '600px'})),
])


# =======================
# 🧭 App Layout (Tabs)
# =======================
app.layout = html.Div(style={
    'backgroundColor': theme['background'], 
    'fontFamily': 'Arial, sans-serif'
}, children=[
    html.H1("AIE & CoE Tuition Dashboard", 
            style={
                'textAlign': 'center', 
                'color': theme['text'],
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
        dcc.Tab(label='🗺️ แผนที่มหาวิทยาลัย', value='map',
                style={'backgroundColor': theme['background'], 'color': theme['text']},
                selected_style={'backgroundColor': theme['card'], 'color': theme['primary']}),
        dcc.Tab(label='🔎 ค้นหาหลักสูตร', value='search',
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
    Input('overview-region-filter', 'value')
)
def update_overview(type_selected, keyword_selected, region_selected):
    dff = df.copy()

    if type_selected != 'all':
        dff = dff[dff['ประเภทหลักสูตร'] == type_selected]

    if keyword_selected != 'all':
        dff = dff[dff['คำค้น'].str.contains(keyword_selected, case=False, na=False)]

    if region_selected != 'all':
        dff = dff[dff['ภาค'] == region_selected]

    if dff.empty:
        # กรณีไม่มีข้อมูล
        empty_fig = px.bar(title='ไม่มีข้อมูล')
        empty_box = px.box(title='ไม่มีข้อมูล')
        return (empty_fig, empty_box,
                "ไม่มีข้อมูล", "ไม่มีข้อมูล", "ไม่มีข้อมูล", "ไม่มีข้อมูล", "0 หลักสูตร")

    # กำหนดขนาด bin ค่าเทอม เช่น 3000 บาท
    bin_size = 3000
    dff['fee_bin_start'] = (dff['ค่าเทอม'] // bin_size) * bin_size
    dff['fee_bin_end'] = dff['fee_bin_start'] + bin_size

    # สรุปข้อมูลในแต่ละ bin
    grouped = dff.groupby(['fee_bin_start', 'fee_bin_end']).agg(
        count=('หลักสูตร', 'count'),
        programs_list=('หลักสูตร', lambda x: list(x.unique())),
        universities_list=('มหาวิทยาลัย', lambda x: list(x.unique()))
    ).reset_index()

    def wrap_text(text, width=60):
        words = text.split(' ')
        lines = []
        current_line = ''

        for word in words:
            # ถ้าเติมคำนี้แล้วเกิน width
            if len(current_line) + len(word) + (1 if current_line else 0) > width:
                # เก็บบรรทัดปัจจุบันก่อน แล้วเริ่มบรรทัดใหม่
                lines.append(current_line)
                current_line = word
            else:
                # เติมคำลงบรรทัด
                if current_line:
                    current_line += ' ' + word
                else:
                    current_line = word

        # บรรทัดสุดท้าย
        if current_line:
            lines.append(current_line)

        return '<br>'.join(lines)


    def make_hover_text(row):
        fee_range = f"ค่าเทอม {int(row['fee_bin_start']):,} - {int(row['fee_bin_end']):,} บาท<br>"
        count = f"จำนวนหลักสูตร: {row['count']} หลักสูตร<br>"
        uni_programs = []
        

        # จำกัดแสดงมหาวิทยาลัยไม่เกิน 3 แห่ง
        for uni in row['universities_list'][:3]:
            progs = dff[
                (dff['fee_bin_start'] == row['fee_bin_start']) &
                (dff['fee_bin_end'] == row['fee_bin_end']) &
                (dff['มหาวิทยาลัย'] == uni)
            ]['หลักสูตร'].unique()

            # จำกัดหลักสูตรไม่เกิน 3 รายการ
            wrapped_progs = [wrap_text(p) for p in progs[:3]]
            progs_text = "<br>- " + "<br>- ".join(wrapped_progs)
            if len(progs) > 3:
                progs_text += "<br>..."

            uni_programs.append(f"{uni}<br>หลักสูตร:{progs_text}<br>")

        # ถ้ามีมากกว่า 3 มหาวิทยาลัย
        if len(row['universities_list']) > 3:
            uni_programs.append("...")

        uni_programs_text = "<br><br>".join(uni_programs)
        return f"{fee_range}{count}<br>{uni_programs_text}"


    grouped['hover_text'] = grouped.apply(make_hover_text, axis=1)

    hist_fig = px.bar(
        grouped,
        x='fee_bin_start',
        y='count',
        color='fee_bin_start',
        color_continuous_scale=px.colors.sequential.Viridis,
        labels={'fee_bin_start': 'ช่วงค่าเทอม (บาท)', 'count': 'จำนวนหลักสูตร'},
        title='การกระจายของค่าเทอมตามช่วง',
        text='count'
    )

    hist_fig.update_traces(
        hovertemplate="%{customdata}<extra></extra>",
        customdata=grouped['hover_text']
    )

    hist_fig.update_layout(
        coloraxis_showscale=False,
        coloraxis_colorbar=dict(title="ช่วงค่าเทอม"),
        title_x=0.5
    )


    # สร้าง boxplot แบบเดิม (ค่าเทอมตามประเภทหลักสูตร)
    box_fig = px.box(
        dff,
        x='ประเภทหลักสูตร',
        y='ค่าเทอม',
        color='ประเภทหลักสูตร',
        title='ค่าเทอมตามประเภทหลักสูตร'
    )
    box_fig.update_layout(showlegend=False,title_x=0.5) 

    count_programs = f"{len(dff):,} หลักสูตร"
    mean_fee = f"{dff['ค่าเทอม'].mean():,.0f} บาท"
    max_fee = f"{dff['ค่าเทอม'].max():,} บาท"
    min_fee = f"{dff['ค่าเทอม'].min():,} บาท"
    median_fee = f"{dff['ค่าเทอม'].median():,} บาท"

    return hist_fig, box_fig, mean_fee, max_fee, min_fee, median_fee, count_programs



@app.callback(
    Output('map-graph', 'figure'),
    Input('tabs', 'value')  # dummy input ให้ callback รันเมื่อเปิด tab map
)
def update_map(tab):
    dff = df.copy()

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
        color_continuous_scale=px.colors.sequential.Plasma,
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


@app.callback(
    Output('search-table', 'data'),
    Output('search-table', 'selected_rows'),
    Output('selected-rank-table', 'data'),
    Input('search-keyword', 'value'),
    Input('search-university', 'value'),
    Input('search-faculty', 'value'),
    Input('search-department', 'value'),
    Input('search-type', 'value'),
    Input('search-region', 'value'),
    Input('min-fee-input', 'value'),
    Input('max-fee-input', 'value'),
    Input('sort-order', 'value'),
    Input('search-table', 'selected_rows'),
    Input('selected-rank-table', 'data'),
    State('search-table', 'data'),
)
def update_all(keyword, university, faculty, department, type_course, region, min_fee, max_fee, sort_order,
               search_selected_rows, selected_rank_data, search_data):

    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # 1. กรองข้อมูลสำหรับ search table ตาม filter dropdown
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

    min_fee = min_fee if min_fee is not None else dff['ค่าเทอม'].min()
    max_fee = max_fee if max_fee is not None else dff['ค่าเทอม'].max()
    dff = dff[(dff['ค่าเทอม'] >= min_fee) & (dff['ค่าเทอม'] <= max_fee)]
    dff = dff.sort_values(by='ค่าเทอม', ascending=(sort_order == 'asc'))

    search_table_data = dff.to_dict('records')

    # 2. กำหนดค่าพื้นฐาน selected_rank_table_data
    selected_rank_table_data = selected_rank_data if selected_rank_data else []

    # 3. ถ้า triggered เป็น search-table (เลือกแถวใหม่) ให้เพิ่ม item ใหม่ลงใน selected_rank_table_data (เก็บไว้)
    if triggered_id == 'search-table' and search_selected_rows is not None and search_data is not None:
        # หาข้อมูลที่ถูกเลือกใน search table
        newly_selected_items = [search_data[i] for i in search_selected_rows if i < len(search_data)]
        
        # รวมข้อมูลเดิมกับข้อมูลใหม่ (โดยไม่ซ้ำหลักสูตร+มหาวิทยาลัย)
        existing_keys = set((item['หลักสูตร'], item['มหาวิทยาลัย']) for item in selected_rank_table_data)
        for item in newly_selected_items:
            key = (item['หลักสูตร'], item['มหาวิทยาลัย'])
            if key not in existing_keys:
                selected_rank_table_data.append(item)
                existing_keys.add(key)
        
        # จำกัดจำนวน 10 อันดับล่าสุดที่เก็บไว้ (ถ้าเกิน)
        selected_rank_table_data = selected_rank_table_data[:10]

    # 4. ถ้า triggered เป็น selected-rank-table (แก้ไขอันดับ หรือ ลบ) ให้ปรับอันดับใหม่
    elif triggered_id == 'selected-rank-table':
        if selected_rank_data:
            selected_rank_table_data = selected_rank_data[:10]
            # ปรับอันดับใหม่
            for idx, item in enumerate(selected_rank_table_data):
                item['อันดับ'] = idx + 1
            # ไม่ติ๊ก checkbox ใน search-table ตอนแก้ไข selected-rank-table
            search_selected_rows = []
        else:
            selected_rank_table_data = []

    # 5. ปรับอันดับของข้อมูลใน selected_rank_table_data เสมอ
    for idx, item in enumerate(selected_rank_table_data):
        item['อันดับ'] = idx + 1

    # 6. กำหนด selected_rows ให้ search-table ให้ตรงกับข้อมูลที่มีใน selected_rank_table_data
    selected_rows = []
    if selected_rank_table_data:
        selected_keys = set((item['หลักสูตร'], item['มหาวิทยาลัย']) for item in selected_rank_table_data)
        for i, row in enumerate(search_table_data):
            key = (row['หลักสูตร'], row['มหาวิทยาลัย'])
            if key in selected_keys:
                selected_rows.append(i)
    else:
        selected_rows = []

    return search_table_data, selected_rows, selected_rank_table_data

@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("export-button", "n_clicks"),
    State("selected-rank-table", "data"),
    prevent_initial_call=True
)
def export_to_excel(n_clicks, table_data):
    if not table_data:
        return dash.no_update
    
    # แปลง list dict เป็น DataFrame
    df_export = pd.DataFrame(table_data)
    
    # ตรวจสอบ columns ที่มี (เพื่อให้แน่ใจว่าครบ)
    expected_cols = ['อันดับ', 'มหาวิทยาลัย', 'หลักสูตร', 'ประเภทหลักสูตร', 'ค่าเทอม']
    # ถ้าคอลัมน์ไม่ครบ อาจจัดเรียงหรือตัดส่วนเกินออก
    df_export = df_export.reindex(columns=expected_cols)
    
    # สร้างไฟล์ Excel ใน memory buffer
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_export.to_excel(writer, index=False, sheet_name='Top 10 Courses')
        # ไม่ต้องเรียก save() เอง
    
    output.seek(0)
    return dcc.send_bytes(output.read(), filename="10อันดับหลักสูตรที่สนใจ.xlsx")




# =======================
# 🚀 Run Server
# =======================
if __name__ == '__main__':
    app.run(debug=True)
