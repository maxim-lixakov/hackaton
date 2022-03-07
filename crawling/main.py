import dash
from dash import dash_table
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


def floater(x):
    if len(x) > 0:
        return float(x)
    else:
        return 0

df = pd.read_json('data.jl', lines =True).fillna('')
try:
    df['Reviews'] = ["\n".join(i) for i in df['reviews']]
except KeyError:
    pass

df['yandex_rating'] = [ floater(x.replace(',', '.')) for x in df['yandex_rating']]
df = df.drop(columns = ['reviews'])


df.set_index('domain', inplace=True, drop=False)

app = dash.Dash(__name__, prevent_initial_callbacks=True)

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
            for i in df.columns
        ],
        style_data_conditional=[{'if': {'column_id': 'Reviews'},  'whiteSpace': 'no-wrap',  'overflow': 'hidden',
                                 'textOverflow': 'ellipsis', 'maxWidth': 0,

                                 'if': {'row_index': 'even'},
                                 'backgroundColor': 'rgb(220, 220, 220)',
                                 # 'color': 'white'
                                 } ],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'backgroundColor': 'rgb(150, 150, 150)',
            'border': '1px solid blue'
        },
        data=df.to_dict('records'),
        editable=False, # editing the values
        filter_action="native", # filter on top
        sort_action="native", # sort on top
        sort_mode="multi", # sort by multiple columns
        column_selectable=False, # single or none
        row_selectable='multi', # single or multi
        row_deletable=True, #
        hidden_columns=['working_hours', 'phone', 'place_in_search', 'details', 'title',
                        'ogrn', 'domain_company_inn_match', 'authorized_capital', 'activity', 'full_name', 'director',
                        'grade', 'planned_checks', 'unplanned_checks', 'infringement', 'not_infringement',
                        'unknown_infringement', 'probable_name', 'fines', 'Reviews'],

        page_action="none", # none if full table
        page_current=0, # opening page
        #page_size=10, # how many rows
        # style_cell_conditional=[
        #{
        #   'if': {'column_id': column_name},
        #   'textAlign': 'middle'
        #} for column_name in ['domain', 'title']
        #],
        style_table={'height': '500px', 'overflowY': 'auto'},
        style_header={
            # 'backgroundColor': 'white',
            # 'fontWeight': 'bold'
            'border': '1px solid pink'
        }
    ),
    html.Br(),
    html.Br(),
    html.Div(id='bar-container'),
    html.Div(id='choromap-container'),
])

@app.callback(
    Output(component_id='bar-container', component_property='children'),
    [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
     ]
)
def update_bar(all_data, slctd_rows):
    dff = pd.DataFrame(all_data)
    colors = ['#7FDBFF' if i in slctd_rows else '#0074D9'
              for i in range(len(dff))]
    if "domain" in dff:
        return [
            dcc.Graph(id='bar-chart',
                      figure=px.bar(
                          data_frame=dff,
                          x="domain",
                          y=column
                      ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
                      .update_traces(marker_color=colors)
                      )
            for column in ['yandex_rating', 'inn', 'ogrn'] if column in dff
        ]

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=False)
