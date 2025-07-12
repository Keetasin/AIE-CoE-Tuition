from dash import Input, Output, State, callback_context, dcc
import pandas as pd
import io

def register_search_callbacks(app, df):
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
        selected_rank_table_data = selected_rank_data if selected_rank_data else []

        if triggered_id == 'search-table' and search_selected_rows is not None and search_data is not None:
            newly_selected_items = [search_data[i] for i in search_selected_rows if i < len(search_data)]

            existing_keys = set((item['หลักสูตร'], item['มหาวิทยาลัย']) for item in selected_rank_table_data)
            for item in newly_selected_items:
                key = (item['หลักสูตร'], item['มหาวิทยาลัย'])
                if key not in existing_keys:
                    selected_rank_table_data.append(item)
                    existing_keys.add(key)

            selected_rank_table_data = selected_rank_table_data[:10]

        elif triggered_id == 'selected-rank-table':
            if selected_rank_data:
                selected_rank_table_data = selected_rank_data[:10]
                for idx, item in enumerate(selected_rank_table_data):
                    item['อันดับ'] = idx + 1
                search_selected_rows = []
            else:
                selected_rank_table_data = []

        for idx, item in enumerate(selected_rank_table_data):
            item['อันดับ'] = idx + 1

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

        df_export = pd.DataFrame(table_data)

        expected_cols = ['อันดับ', 'มหาวิทยาลัย', 'หลักสูตร', 'ประเภทหลักสูตร', 'ค่าเทอม']
        df_export = df_export.reindex(columns=expected_cols)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_export.to_excel(writer, index=False, sheet_name='Top 10 Courses')

        output.seek(0)
        return dcc.send_bytes(output.read(), filename="10อันดับหลักสูตรที่สนใจ.xlsx")
