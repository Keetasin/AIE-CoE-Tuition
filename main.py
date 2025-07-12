from dash import Dash, dcc, html, Input, Output
from web.layout.overview import get_overview_layout
from web.layout.map_view import get_map_layout
from web.layout.search import get_search_layout
from web.callbacks.overview_callbacks import register_overview_callbacks
from web.callbacks.map_callbacks import register_map_callbacks
from web.callbacks.search_callbacks import register_search_callbacks

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

# สมมติคุณโหลด DataFrame ไว้ที่นี่ (แก้เป็น DataFrame จริงของคุณ)
import pandas as pd
df = pd.read_excel("web/data/university_fee_with_latlon.xlsx")

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

@app.callback(Output('tabs-content', 'children'), Input('tabs', 'value'))
def switch_tab(tab):
    if tab == 'overview':
        return get_overview_layout(df, theme)
    elif tab == 'search':
        # เรียกใช้ฟังก์ชัน get_search_layout พร้อมส่ง df กับ theme
        return get_search_layout(df, theme)
    elif tab == 'map':
        # เรียกใช้ฟังก์ชัน get_map_layout พร้อมส่ง theme
        return get_map_layout(theme)

# Register all callbacks from separate files
register_overview_callbacks(app, df)
register_map_callbacks(app, df)
register_search_callbacks(app, df)  

if __name__ == '__main__':
    app.run(debug=True)
