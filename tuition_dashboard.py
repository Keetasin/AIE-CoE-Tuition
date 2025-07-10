
import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px

# Load data
df = pd.read_excel("web/data/cleaned_file.xlsx")
df['ประเภทหลักสูตร'] = df['ประเภทหลักสูตร'].astype(str)

# App initialization
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server


# Layouts for each tab
theme = {
    'background': '#f0f8ff',
    'card': '#ffffff',
    'primary': '#007acc',
    'text': '#003f5c',
    'accent': '#00bcd4'
}



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
        ], style={'width': '50%'}),

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
        ], style={'width': '50%'})
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


university_layout = html.Div([
    html.H2("🏫 เปรียบเทียบค่าเทอมรายมหาวิทยาลัย", style={'textAlign': 'center'}),
    
    html.Label("เลือกประเภทหลักสูตร:"),
    dcc.Dropdown(
        id='type-filter',
        options=[{'label': t, 'value': t} for t in df['ประเภทหลักสูตร'].unique()],
        value=df['ประเภทหลักสูตร'].unique()[0],
        clearable=False,
        style={'width': '40%', 'marginBottom': '10px'}
    ),

    html.Label("เลือกคำค้น (หลักสูตร):"),
    dcc.Dropdown(
        id='keyword-filter-university',
        options=[{'label': k, 'value': k} for k in sorted(df['คำค้น'].dropna().unique())],
        value=None,
        clearable=True,
        style={'width': '40%', 'marginBottom': '20px'}
    ),

    dcc.Graph(id='bar-university'),
    dash_table.DataTable(
        id='table-university',
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'fontFamily': 'Arial'}
    )
])


faculty_layout = html.Div([
    html.H2("🏛 วิเคราะห์ค่าเทอมตามคณะ/สาขา", style={'textAlign': 'center'}),

    html.Label("เลือกคำค้น (หลักสูตร):"),
    dcc.Dropdown(
        id='keyword-filter',
        options=[{'label': 'ทั้งหมด', 'value': 'all'}] +
                [{'label': k, 'value': k} for k in sorted(df['คำค้น'].dropna().unique())],
        value='all',
        clearable=False,
        style={'width': '60%', 'marginBottom': '20px'}
    ),
    dcc.Graph(id='treemap-faculty')
])



search_layout = html.Div([
    html.H2("🔎 ค้นหาหลักสูตรที่เหมาะสม", style={'textAlign': 'center'}),
    html.Label("ช่วงค่าเทอม (บาท):"),
    dcc.RangeSlider(
        id='fee-slider',
        min=df['ค่าเทอม'].min(), max=df['ค่าเทอม'].max(),
        step=1000,
        value=[df['ค่าเทอม'].min(), df['ค่าเทอม'].max()],
        marks={int(k): str(int(k)) for k in df['ค่าเทอม'].quantile([0, 0.25, 0.5, 0.75, 1])}
    ),
    html.Br(),
    html.Label("ประเภทหลักสูตร:"),
    dcc.Dropdown(
        id='search-type',
        options=[{'label': t, 'value': t} for t in df['ประเภทหลักสูตร'].unique()],
        multi=True,
        value=list(df['ประเภทหลักสูตร'].unique())
    ),
    dash_table.DataTable(
        id='search-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'}
    )
])

# Main app layout
# Theme color palette
theme = {
    'background': '#f0f8ff',  # Alice Blue
    'card': '#ffffff',        # White
    'primary': '#007acc',     # Blue
    'text': '#003f5c',        # Dark Blue
    'accent': '#00bcd4'       # Cyan
}

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

        dcc.Tab(label='🏫 มหาวิทยาลัย', value='university',
                style={'backgroundColor': theme['background'], 'color': theme['text']},
                selected_style={'backgroundColor': theme['card'], 'color': theme['primary']}),

        dcc.Tab(label='🏛 คณะ/สาขา', value='faculty',
                style={'backgroundColor': theme['background'], 'color': theme['text']},
                selected_style={'backgroundColor': theme['card'], 'color': theme['primary']}),

        dcc.Tab(label='🔎 ค้นหาหลักสูตร', value='search',
                style={'backgroundColor': theme['background'], 'color': theme['text']},
                selected_style={'backgroundColor': theme['card'], 'color': theme['primary']}),
    ]),
    html.Div(id='tabs-content', style={'padding': '20px'})
])


# Callbacks
@app.callback(Output('tabs-content', 'children'), Input('tabs', 'value'))
def switch_tab(tab):
    if tab == 'overview':
        return overview_layout
    elif tab == 'university':
        return university_layout
    elif tab == 'faculty':
        return faculty_layout
    elif tab == 'search':
        return search_layout

@app.callback(
    Output('bar-university', 'figure'),
    Output('table-university', 'data'),
    Input('type-filter', 'value'),
    Input('keyword-filter-university', 'value')
)
def update_university(type_selected, keyword_selected):
    df_filtered = df[df['ประเภทหลักสูตร'] == type_selected]

    if keyword_selected:
        df_filtered = df_filtered[df_filtered['คำค้น'].str.contains(keyword_selected, case=False, na=False)]

    bar_fig = px.bar(
        df_filtered.groupby('มหาวิทยาลัย')['ค่าเทอม'].mean().reset_index(),
        x='มหาวิทยาลัย',
        y='ค่าเทอม',
        title='ค่าเทอมเฉลี่ยต่อมหาวิทยาลัย',
        color='ค่าเทอม',
        color_continuous_scale='viridis'
    )

    return bar_fig, df_filtered.to_dict('records')


@app.callback(
    Output('treemap-faculty', 'figure'),
    Input('keyword-filter', 'value')
)
def update_treemap_faculty(selected_keyword):
    if not selected_keyword or selected_keyword == 'all':
        filtered_df = df.dropna(subset=['สาขา', 'คำค้น', 'ค่าเทอม'])
        filtered_df['ค่าเทอม'] = pd.to_numeric(filtered_df['ค่าเทอม'], errors='coerce')
        filtered_df = filtered_df.dropna(subset=['ค่าเทอม'])
        title = 'Treemap: สาขา → คำค้น → ค่าเทอม (ทั้งหมด)'
    else:
        filtered_df = df[df['คำค้น'].str.contains(selected_keyword, case=False, na=False)]
        filtered_df = filtered_df.dropna(subset=['สาขา', 'คำค้น', 'ค่าเทอม'])
        filtered_df['ค่าเทอม'] = pd.to_numeric(filtered_df['ค่าเทอม'], errors='coerce')
        filtered_df = filtered_df.dropna(subset=['ค่าเทอม'])
        title = f'Treemap: สาขา → คำค้น → ค่าเทอม ({selected_keyword})'

    if filtered_df.empty:
        fig = px.treemap(
            names=['ไม่มีข้อมูล'],
            parents=[''],
            values=[1],
            title='ไม่มีข้อมูลสำหรับคำค้นที่เลือก'
        )
        return fig

    fig = px.treemap(
        filtered_df,
        path=['สาขา', 'คำค้น'],
        values='ค่าเทอม',
        color='ค่าเทอม',
        color_continuous_scale='Blues',
        title=title,
        hover_data={'ค่าเทอม': ':.0f'}
    )

    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        uniformtext=dict(minsize=12, mode='hide')
    )

    return fig



@app.callback(
    Output('histogram-overview', 'figure'),
    Output('boxplot-overview', 'figure'),
    Output('mean-fee', 'children'),
    Output('max-fee', 'children'),
    Output('min-fee', 'children'),
    Output('median-fee', 'children'),
    Output('count-programs', 'children'),
    Input('overview-type-filter', 'value'),
    Input('overview-keyword-filter', 'value')
)
def update_overview(type_selected, keyword_selected):
    dff = df.copy()

    if type_selected != 'all':
        dff = dff[dff['ประเภทหลักสูตร'] == type_selected]

    if keyword_selected != 'all':
        dff = dff[dff['คำค้น'].str.contains(keyword_selected, case=False, na=False)]

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





# Run server
if __name__ == '__main__':
    app.run(debug=True)
