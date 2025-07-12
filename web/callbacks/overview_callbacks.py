from dash import Input, Output
import plotly.express as px
import pandas as pd

def register_overview_callbacks(app, df):
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
            empty_fig = px.bar(title='ไม่มีข้อมูล')
            empty_box = px.box(title='ไม่มีข้อมูล')
            return empty_fig, empty_box, "ไม่มีข้อมูล", "ไม่มีข้อมูล", "ไม่มีข้อมูล", "ไม่มีข้อมูล", "0 หลักสูตร"

        bin_size = 3000
        dff['fee_bin_start'] = (dff['ค่าเทอม'] // bin_size) * bin_size
        dff['fee_bin_end'] = dff['fee_bin_start'] + bin_size

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
                if len(current_line) + len(word) + (1 if current_line else 0) > width:
                    lines.append(current_line)
                    current_line = word
                else:
                    current_line = (current_line + ' ' + word) if current_line else word
            if current_line:
                lines.append(current_line)
            return '<br>'.join(lines)

        def make_hover_text(row):
            fee_range = f"ค่าเทอม {int(row['fee_bin_start']):,} - {int(row['fee_bin_end']):,} บาท<br>"
            count = f"จำนวนหลักสูตร: {row['count']} หลักสูตร<br>"
            uni_programs = []
            for uni in row['universities_list'][:3]:
                progs = dff[
                    (dff['fee_bin_start'] == row['fee_bin_start']) &
                    (dff['fee_bin_end'] == row['fee_bin_end']) &
                    (dff['มหาวิทยาลัย'] == uni)
                ]['หลักสูตร'].unique()
                wrapped_progs = [wrap_text(p) for p in progs[:3]]
                progs_text = "<br>- " + "<br>- ".join(wrapped_progs)
                if len(progs) > 3:
                    progs_text += "<br>..."
                uni_programs.append(f"{uni}<br>หลักสูตร:{progs_text}<br>")
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
            title_x=0.5
        )

        box_fig = px.box(
            dff,
            x='ประเภทหลักสูตร',
            y='ค่าเทอม',
            color='ประเภทหลักสูตร',
            title='ค่าเทอมตามประเภทหลักสูตร'
        )
        box_fig.update_layout(showlegend=False, title_x=0.5)

        count_programs = f"{len(dff):,} หลักสูตร"
        mean_fee = f"{dff['ค่าเทอม'].mean():,.0f} บาท"
        max_fee = f"{dff['ค่าเทอม'].max():,} บาท"
        min_fee = f"{dff['ค่าเทอม'].min():,} บาท"
        median_fee = f"{dff['ค่าเทอม'].median():,} บาท"

        return hist_fig, box_fig, mean_fee, max_fee, min_fee, median_fee, count_programs
