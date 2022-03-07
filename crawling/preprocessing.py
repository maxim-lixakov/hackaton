import re
import json

import pandas as pd


def range_values(values, reverse=True):
    values = [0 if el is None else el for el in values]  # comment in future

    dict = {}
    place = 1
    for value in (sorted(values, reverse=reverse)):
        if value not in dict:
            dict[value] = place
            place += 1

    ranged_values = []
    for value in values:
        ranged_values.append(dict[value])

    return ranged_values


def get_ratings(rangingFields, grades, yandexRatings, binaryFields, alpha_rf=100, alpha_grade=10, alpha_yr=20,
                alpha_bf=20):
    # rangingFields - список списков, где каждый список содержит ранги поставщиков по данному полю
    # binaryFields - аналогично
    ratings = []
    for i in range(len(rangingFields[0])):  # количество поставщиков

        company_rangingFields = []
        for el in rangingFields:
            company_rangingFields.append(el[i])

        company_binaryFields = []
        for el in binaryFields:
            company_binaryFields.append(el[i])

        rf = iter(rangingFields)
        grades = iter(grades)
        yandexRatings = iter(yandexRatings)
        rating = alpha_rf * sum([max(next(rf)) - crf for crf in company_rangingFields]) + alpha_grade * next(
            grades) + alpha_yr * next(yandexRatings) + alpha_bf * sum(company_binaryFields)
        ratings.append(rating)
    return ratings


with open('data.jl', 'r') as file:
    dicts = []
    for line in file.readlines():
        dicts.append(json.loads(re.findall(r'({.*?})', line)[0]))
    df = pd.DataFrame.from_records(dicts)

formula_fields = ['grade', 'yandex_rating']
binary_fields = ['domain', 'title', 'inn', 'full_name', 'ogrn', 'phone', 'working_hours', 'director',
                 'domain_company_inn_match', 'activity', 'reviews']
ranging_fields = ['place_in_search', 'details_num', 'authorized_capital', 'planned_checks', 'unplanned_checks',
                  'reviews_count', 'not_infringement']
ranging_fields_reverse_false = ['date_reg', 'fines', 'infringement', 'unknown_infringement']
fields = formula_fields + binary_fields + ranging_fields + ranging_fields_reverse_false

for field in fields:
    if field not in df.columns:
        df[field] = int(df.shape[0]) * [None]

for field in binary_fields:
    df[field] = df[field].notnull().astype(int)

try:
    df['grade'] = df['grade'].notnull().astype(int)
    df['yandex_rating'] = df['yandex_rating'].fillna(0).replace(',', '.', regex=True).astype(float)
    df['place_in_search'].fillna(df['place_in_search'].max() + 1, inplace=True)
    df['place_in_search'].fillna(0, inplace=True)

    df['details_num'].fillna(0, inplace=True)  #
    df['fines'] = df['fines'].fillna(0).replace('(\D*)', '', regex=True).astype(int)  # Чем меньше тем лучше
    df['authorized_capital'] = df['authorized_capital'].fillna(0).replace('(\D*)', '', regex=True).astype(int)
    # Не забыть поправить парсинг капитала где огромные значение
    df['reviews_count'] = df['reviews_count'].fillna(0).replace('(\D*)', '', regex=True).astype(int)

    df['planned_checks'] = df['planned_checks'].fillna(0).astype(int)
    df['unplanned_checks'] = df['unplanned_checks'].fillna(0).astype(int)
    df['infringement'] = df['infringement'].fillna(0).astype(int)  # Чем меньше тем лучше
    df['not_infringement'] = df['not_infringement'].fillna(0).astype(int)
    df['unknown_infringement'] = df['unknown_infringement'].fillna(0).astype(int)  # Чем меньше тем лучше

    df['date_reg'] = pd.to_datetime(df['date_reg'].fillna(pd.to_datetime('today').date()))  # Чем меньше тем лучше
except KeyError:
    pass

try:
    df.drop(columns=['name', 'probable_name'], inplace=True)
except KeyError:
    pass

rangingFields_temp1 = [df[column_name] for column_name in ranging_fields]
rangingFields_temp2 = [df[column_name] for column_name in ranging_fields_reverse_false]
rangingFields1 = [range_values(field) for field in rangingFields_temp1]
rangingFields2 = [range_values(field, reverse=False) for field in rangingFields_temp2]
rangingFields = rangingFields1 + rangingFields2

grades = df['grade']
yandexRatings = df['yandex_rating']

binaryFields = [df[column_name] for column_name in binary_fields]

ratings = get_ratings(rangingFields, grades, yandexRatings, binaryFields)

with open('data.jl', 'r') as file:
    dicts = []
    for line in file.readlines():
        dicts.append(json.loads(re.findall(r'({.*?})', line)[0]))
    df_initial = pd.DataFrame.from_records(dicts)

df_initial['rating'] = ratings
df_initial.to_csv('data.csv', index=False)
