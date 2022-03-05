import dash
from dash import dash_table
from dash import html
import pandas as pd

from preprocessing import df_initial


df = df_initial.fillna('')

#TODO: except keyerror

# df['Reviews'] = ['\n'.join(i) for i in df['reviews']]
# df = df.drop(columns = ['reviews'])
df.set_index('domain', inplace=True, drop=False)

app = dash.Dash(__name__, prevent_initial_callbacks=True)

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
            for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=False, # editing the values
        filter_action="native", # filter on top
        sort_action="native", # sort on top
        sort_mode="multi", # sort by multiple columns
        column_selectable="multi", # single or none
        row_selectable=False, # single or multi
        row_deletable=True, #
        selected_columns=[], # ?
        selected_rows=[], # ?
        page_action="native", # none if full table
        page_current=0, # opening page
        page_size=3, # how mane rows
        style_cell={
            'minWidth': 150, 'maxWidth': 150, 'width': 150
        },
        # style_cell_conditional=[
            #{
             #   'if': {'column_id': column_name},
             #   'textAlign': 'middle'
            #} for column_name in ['domain', 'title']
        #],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        }
    ),
    html.Br(),
    html.Br(),
    html.Div(id='bar-container'),
    html.Div(id='choromap-container')
])
# -------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=False)