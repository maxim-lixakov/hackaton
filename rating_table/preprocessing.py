import json
import re
import math

import pandas as pd
import numpy as np

def convert_string_to_float(df, column):
    column_name = []
    df[column] = df[column].fillna('none')
    for meaning in df[column]:
        meaning = re.findall('[+-]?(\d+[.]?[0-9]*)', meaning)
        meaning = float(meaning[0]) if len(meaning) > 0 else 0
        column_name.append(meaning)
    df[column] = column_name
    column_name = []
    mean = round(df[column].mean(), 3)
    for meaning in df[column]:
        meaning = mean if meaning == 0 else meaning
        column_name.append(meaning)
    df[column] = column_name


def convert_string_to_binary(df, column):
    column_name = []
    for meaning in df[column]:
        meaning = 1 if len(str(meaning)) > 0 else 0
        column_name.append(meaning)
    df[column] = column_name


def main():
    weights = [-3.237012567147341e-09,
               -2.767900767267789,
               -16.256427241983257,
               -5.809628333963701e-10,
                14.529598236229196,
                0.4137193704321781,
                0.4137193705548797,
                0.41371937056185143,
                0.41371937051986024,
                47.402257913957655,
               -43.711202198990804,
               -16.68023948808181,
               -0.39412568009946686,
               -16.680239488122474,
               -16.68023948810354,
               -2.8484074000820785,
               -1891.7957652924097,
               -1717.4335324384654,
               1814.0936787334895,
               1746.1481044472011,
               1965.6042583810392,
               -0.07125753650983446,
               -17.013592504677465,
               1.6798383038279145,
               79.63412816136287,
               0.0,
               -119.70577952627274]

    float_fields = ['reviews_count', 'yandex_rating', 'authorized_capital', 'fines', 'planned_checks',
                    'unplanned_checks', 'infringement', 'not_infringement', 'unknown_infringement']
    binar_fields = ['inn', 'details', 'title', 'full_name', 'ogrn', 'director', 'domain_company_inn_match',
                    'grade', 'date_reg', 'activity', 'name', 'reviews', 'working_hours', 'phone', 'email', 'domain']


    with open('data.jl', 'r') as file:
        dicts = []
        for line in file.readlines():
            dicts.append(json.loads(re.findall(r'({.*?})', line)[0]))
        df = pd.DataFrame.from_records(dicts)
        df = df.drop_duplicates(subset='domain', keep='last')

    df = df.drop(columns=['probable_name'])

    for field in float_fields:
        convert_string_to_float(df, field)

    for field in binar_fields:
        convert_string_to_binary(df, field)

    df['rating'] = df[df.columns].dot(np.array(list(weights)).T)
    return df['rating']


with open('data.jl', 'r') as file:
    dicts = []
    for line in file.readlines():
        dicts.append(json.loads(re.findall(r'({.*?})', line)[0]))
    df_initial = pd.DataFrame.from_records(dicts)

df_initial = df_initial.drop_duplicates(subset='domain', keep='last')
df_initial['rating'] = main()
#normalization
x = (max(df_initial['rating']) - (df_initial['rating'] + 1000))/max(df_initial['rating'])
df_initial['rating'] = [round(rating, 3) for rating in  x / x.max(axis=0)]