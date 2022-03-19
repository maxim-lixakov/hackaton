import dash
from dash import dash_table
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

from preprocessing import df_initial

df_initial.sort_values(by=['rating'], inplace=True, ascending=False)
df = df_initial.fillna('').drop_duplicates('domain')

def floater(x):
    if len(x) > 0:
        return float(x)
    else:
        return 0


try:
    df['Reviews'] = ["".join(i) for i in df['reviews']]
    df['yandex_rating'] = [ floater(x.replace(',', '.')) for x in df['yandex_rating']]
    df = df.drop(columns = ['reviews'])
except KeyError:
    pass

list_of_details = [' Манжета М50х70 ГОСТ 22704',
                   ' Манжета М65х90 ГОСТ 22704',
                   ' Манжета М220х250 ГОСТ 22704',
                   ' Манжета М60х80 ГОСТ 22704',
                   ' Манжета резиновая армированная для валов 1.2-120х150х12-1 ГОСТ 8752',
                   ' Пластина техническая 2Н-I-ТМКЩ-С-4 ГОСТ 7338',
                   ' Рукав всасывающий В-1-75-У рабочий вакуум 0,08МПа ГОСТ 5398',
                   ' Рукав с текстильным каркасом В(II)-16-25-38-ХЛ ГОСТ 18698',
                   ' Пластина техническая 1Н-I-ТМКЩ-С-5 ГОСТ 7338',
                   ' Манжета резиновая армированная для валов 1.2-90х120х12-1 ГОСТ 8752',
                   ' Манжета М140х170 ГОСТ 22704',
                   ' Манжета резиновая армированная для валов 1.2-180х220х15-1 ГОСТ 8752',
                   ' Манжета резиновая армированная для валов 1.2-190х230х15-1 ГОСТ 8752',
                   ' Рукав газосварочный I-6,3-0,63-У ГОСТ 9356',
                   ' Рукав с текстильным каркасом ВГ(III)-10-25-38-У ГОСТ 18698',
                   ' БОЛТ; СТАНДАРТ ГОСТ7796, ГОЛОВКА ШЕСТИГРАННАЯ, ОБОЗНАЧЕНИЕ M20Х80, КЛАСС ПРОЧНОСТИ 6.6, МАТЕРИАЛ СТАЛЬ ОЦИНКОВАННАЯ',
                   ' Болт головка шестигранная M16х120.88 ГОСТ Р ИСО 4014',
                   ' Гайка шестигранная M30.6 покрытие цинковое ГОСТ 5915',
                   ' Гвоздь строительный круглый головка плоская 3х80 ГОСТ 4028',
                   ' БОЛТ; СТАНДАРТ ГОСТ7817 DIN609, ОБОЗНАЧЕНИЕ M36-6GХ200, КЛАСС ПРОЧНОСТИ 10.9, МАТЕРИАЛ СТАЛЬ 40Х',
                   ' БОЛТ; СТАНДАРТ ГОСТ7796, ГОЛОВКА ШЕСТИГРАННАЯ, ОБОЗНАЧЕНИЕ 2М10-6GХ28, КЛАСС ПРОЧНОСТИ 5.6, МАТЕРИАЛ СТАЛЬ ОЦИНКОВАННАЯ',
                   ' Болт головка шестигранная M10х35.66 покрытие цинковое ГОСТ 7796',
                   ' БОЛТ; СТАНДАРТ ГОСТ7817 DIN609, ГОЛОВКА ШЕСТИГРАННАЯ, ОБОЗНАЧЕНИЕ 2.M30Х100, КЛАСС ПРОЧНОСТИ 5.8, МАТЕРИАЛ СТАЛЬ',
                   ' БОЛТ; СТАНДАРТ ГОСТ7798 ГОСТ7805, ГОЛОВКА ШЕСТИГРАННАЯ, ОБОЗНАЧЕНИЕ 3.M12Х25, КЛАСС ПРОЧНОСТИ 5.8, МАТЕРИАЛ СТАЛЬ',
                   ' БОЛТ; СТАНДАРТ ГОСТ7808, ГОЛОВКА ШЕСТИГРАННАЯ, ОБОЗНАЧЕНИЕ М24Х55, КЛАСС ПРОЧНОСТИ 5.6, МАТЕРИАЛ СТАЛЬ',
                   ' БОЛТ; СТАНДАРТ ГОСТ7817 DIN609, ГОЛОВКА ШЕСТИГРАННАЯ, ОБОЗНАЧЕНИЕ M24Х80, КЛАСС ПРОЧНОСТИ 6.6, МАТЕРИАЛ СТАЛЬ ОЦИНКОВАННАЯ',
                   ' Гайка шестигранная M24.8 ГОСТ 5916',
                   ' БОЛТ; СТАНДАРТ ГОСТ7796, ГОЛОВКА ШЕСТИГРАННАЯ, ОБОЗНАЧЕНИЕ 3M16Х30, КЛАСС ПРОЧНОСТИ 5.8',
                   ' Гайка шестигранная M30.8.35 покрытие цинковое ГОСТ 15521',
                   ' ГАЙКА; ТИП ШЕСТИГРАННАЯ, ОБОЗНАЧЕНИЕ M20, СТАНДАРТ ГОСТ15521, КЛАСС ПРОЧНОСТИ 5, МАТЕРИАЛ СТАЛЬ ОЦИНКОВАННАЯ',
                   ' ГАЙКА; ОБОЗНАЧЕНИЕ M10, СТАНДАРТ ГОСТ15521, КЛАСС ПРОЧНОСТИ 5, МАТЕРИАЛ СТАЛЬ ОЦИНКОВАННАЯ',
                   ' ГАЙКА; ОБОЗНАЧЕНИЕ M16, СТАНДАРТ ГОСТ15521, КЛАСС ПРОЧНОСТИ 5, МАТЕРИАЛ СТАЛЬ ОЦИНКОВАННАЯ',
                   ' ШАЙБА; ТИП ПЛОСКАЯ УМЕНЬШЕННАЯ, СТАНДАРТ ГОСТ10450 DIN433, ОБОЗНАЧЕНИЕ А24, МАТЕРИАЛ СТАЛЬ 20 ОЦИНКОВАННАЯ',
                   ' Гайка шестигранная M20х1,5.5 покрытие цинковое, хроматированное ГОСТ\xa0 15521',
                   ' Гайка шестигранная M12.5 покрытие цинковое ГОСТ 15521',
                   ' Гайка шестигранная M12.8.35 покрытие цинковое ГОСТ 15521',
                   ' Шайба плоская 16.32 ГОСТ 6958',
                   ' ГАЙКА; ОБОЗНАЧЕНИЕ М24-6Н.8.35.0112, СТАНДАРТ ГОСТ15521, КЛАСС ПРОЧНОСТИ 8, МАТЕРИАЛ СТАЛЬ 35 ОЦИНКОВАННАЯ',
                   ' Гайка шестигранная M42х3.8 покрытие цинковое ГОСТ 5915',
                   ' БОЛТ; СТАНДАРТ ГОСТ Р ИСО4014 DIN931 (ГОСТ7798/7805), ГОЛОВКА ШЕСТИГРАННАЯ, ОБОЗНАЧЕНИЕ M16Х65, КЛАСС ПРОЧНОСТИ 8.8, МАТЕРИАЛ СТАЛЬ/ ОЦИНКОВАННАЯ']


list_of_domains = df['domain'].unique()
good_part = df[['domain', 'details']].drop_duplicates('domain')


def binar(domain, data_details, data):
    a = []
    for i in range(len(data_details)):
        if data_details[i] in data[data['domain'] == domain].reset_index()['details'][0]:
            a.append(1)
        else:
            a.append(0)
    return a

domains_details = [binar(dom, list_of_details, good_part) for dom in good_part['domain'].to_list()]
final_df = pd.DataFrame(domains_details, index = list_of_domains, columns = list_of_details)
Table = pd.concat([final_df,pd.DataFrame(final_df.sum(axis=1),columns=['Количество деталей'])],
                  axis=1).reset_index().rename(columns={"index": "domain"})
hidden_columns = Table.columns.to_list()
hidden_columns.remove('domain')
hidden_columns.remove('Количество деталей')


df.set_index('domain', inplace=True, drop=False)

app = dash.Dash(__name__, prevent_initial_callbacks=True)

table_1 = dash_table.DataTable(
    id='datatable-interactivity',
    columns=[
        {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
        for i in df.columns
    ],
    style_data_conditional=[{'if': {'column_id': 'Reviews'},  'whiteSpace': 'no-wrap',  'overflow': 'hidden',
                             'textOverflow': 'ellipsis', 'maxWidth': 0,

                             'if': {'row_index': 'even'},
                             'backgroundColor': 'rgb(176, 196, 222)',
                             # 'color': 'white'
                             } ],
    style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        #'border': '1px solid black'
    },
    data=df.to_dict('records'),
    editable=False, # editing the values
    filter_action="native", # filter on top
    sort_action="native", # sort on top
    sort_mode="multi", # sort by multiple columns
    column_selectable=False, # single or none
    row_selectable='multi', # single or multi
    row_deletable=True, #
    hidden_columns=['working_hours', 'place_in_search', 'details', 'title',
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
        'border': '1px solid black'
    }
)




table_2 = dash_table.DataTable(
    id='datatable-interactivity_2',
    columns=[
        {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
        for i in Table.columns
    ],
    style_data_conditional=[{ 'if': {'row_index': 'even'},
                              'backgroundColor': 'rgb(176, 196, 222)',
                              # 'color': 'white'
                              } ],
    style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        #'border': '1px solid black'
    },
    data=Table.to_dict('records'),
    editable=False, # editing the values
    filter_action="native", # filter on top
    sort_action="native", # sort on top
    sort_mode="multi", # sort by multiple columns
    column_selectable=False, # single or none
    row_selectable='multi', # single or multi
    row_deletable=True, #
    hidden_columns=hidden_columns,
    page_action="none", # none if full table
    page_current=0, # opening page
    #page_size=10, # how many rows
    # style_cell_conditional=[
    #{
    #   'if': {'column_id': column_name},
    #   'textAlign': 'middle'
    #} for column_name in ['domain', 'title']
    #],
    style_table={'height': '300px', 'overflowY': 'auto'},
    style_header={
        # 'backgroundColor': 'white',
        # 'fontWeight': 'bold'
        'border': '1px solid black'
    }
)




app.layout = html.Div([ html.Div([table_1], style={'display': 'inline-block'}),
                        html.Br(),
                        html.Br(),
                        html.Div(id='bar-container'),
                        html.Div(id='choromap-container'),
                        html.Div([table_2], style={'display': 'inline-block'}),
                        ])

@app.callback(
    Output(component_id='bar-container', component_property='children'),
    [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
     ]
)

def update_bar(all_data, slctd_rows):
    dff = pd.DataFrame(all_data)
    colors = ['#00008B' if i in slctd_rows else '#B0C4DE'
              for i in range(len(dff))]
    if "domain" in dff:
        return [
            dcc.Graph(id='bar-chart',
                      figure=px.bar(
                          data_frame=dff,
                          x="domain",
                          y=column
                      ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
                      .update_traces(marker_color=colors).update_yaxes(title=column,
                                                                       visible=True, showticklabels=False)
                      )
            for column in ['rating'] if column in dff
        ]


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=False)
