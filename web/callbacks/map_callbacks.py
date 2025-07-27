from dash import Input, Output
import plotly.express as px
import pandas as pd

def register_map_callbacks(app, df):
    @app.callback(
        Output('university-dropdown', 'options'),
        Input('tabs', 'value')
    )
    def update_dropdown(tab):
        if tab == 'map':
            options = [{'label': uni, 'value': uni} for uni in sorted(df['มหาวิทยาลัย'].dropna().unique())]
            return options
        return []

    @app.callback(
        Output('map-graph', 'figure'),
        Input('tabs', 'value'),
        Input('university-dropdown', 'value')
    )
    def update_map(tab, selected_unis):
        dff = df.copy()
        dff = dff.dropna(subset=['Latitude', 'Longitude'])

        # Filter by university dropdown
        if selected_unis:
            dff = dff[dff['มหาวิทยาลัย'].isin(selected_unis)]

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

        grouped['customdata'] = grouped.apply(lambda row: [
            row['ภาค'],
            row['ข้อมูลหลักสูตร'],
            f"{row['ค่าเทอมเฉลี่ย']:,.0f} บาท",
            f"{row['ค่าเทอมต่ำสุด']:,.0f} บาท",
            f"{row['ค่าเทอมสูงสุด']:,.0f} บาท",
            row['จำนวนหลักสูตร']
        ], axis=1)

        color_range = (df.groupby('มหาวิทยาลัย')['ค่าเทอม'].mean().min(), df.groupby('มหาวิทยาลัย')['ค่าเทอม'].mean().max())

        fig = px.scatter_mapbox(
            grouped,
            lat="Latitude",
            lon="Longitude",
            color="ค่าเทอมเฉลี่ย",
            size="จำนวนหลักสูตร",
            size_max=20,
            zoom=5,
            color_continuous_scale=px.colors.sequential.Plasma,
            range_color=color_range
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
