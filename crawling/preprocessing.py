import re
import json

import pandas as pd


def range_values(values, reverse=False):
    values = [0 if el is None else el for el in values]

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

        grades = iter(grades)
        yandexRatings = iter(yandexRatings)
        rating = alpha_rf * sum([crf for crf in company_rangingFields]) + alpha_grade * next(
            grades) + alpha_yr * next(yandexRatings) + alpha_bf * sum(company_binaryFields)
        ratings.append(rating)
    return ratings


def get_ratings_with_weights(rangingFields, grades, yandexRatings, binaryFields, weights, alpha_grade=15, alpha_yr=25,
                             alpha_bf=15):
    # rangingFields - список списков, где каждый список содержит ранги поставщиков по данному полю
    # binaryFields - аналогично
    ratings = []
    for i in range(len(rangingFields[0])):  # количество поставщиков

        company_rangingFields = []
        for el in rangingFields:
            company_rangingFields.append(el[i])
        for j in range(len(company_rangingFields)):
            company_rangingFields[j] *= weights[j]

        company_binaryFields = []
        for el in binaryFields:
            company_binaryFields.append(el[i])

        grades = iter(grades)
        yandexRatings = iter(yandexRatings)
        rating = sum([crf for crf in company_rangingFields]) + alpha_grade * next(
            grades) + alpha_yr * next(yandexRatings) + alpha_bf * sum(company_binaryFields)
        ratings.append(rating)
    return ratings


with open('data.jl', 'r') as file:
    dicts = []
    for line in file.readlines():
        dicts.append(json.loads(re.findall(r'({.*?})', line)[0]))
    df = pd.DataFrame.from_records(dicts)
    df.drop_duplicates(subset='domain', keep='last')
df.to_csv('data_temp.csv', index=False)
df = pd.read_csv('data_temp.csv')

formula_fields = ['grade', 'yandex_rating']
binary_fields = ['domain', 'title', 'inn', 'full_name', 'ogrn', 'phone', 'working_hours', 'director',
                 'domain_company_inn_match', 'activity', 'reviews']
ranging_fields = ['place_in_search', 'details_num', 'authorized_capital', 'planned_checks', 'unplanned_checks',
                  'reviews_count', 'not_infringement']
ranging_fields_reverse_true = ['date_reg', 'fines', 'infringement', 'unknown_infringement']
fields = formula_fields + binary_fields + ranging_fields + ranging_fields_reverse_true

for field in fields:
    if field not in df.columns:
        df[field] = int(df.shape[0]) * [None]

for field in binary_fields:
    df[field] = df[field].notnull().astype(int)

df['grade'] = df['grade'].notnull().astype(int)
df['yandex_rating'] = df['yandex_rating'].fillna(0).replace(',', '.', regex=True).astype(float)
df['place_in_search'].fillna(df['place_in_search'].max() + 1, inplace=True)
df['place_in_search'].fillna(0, inplace=True)

df['details_num'].fillna(0, inplace=True)
df['fines'] = df['fines'].fillna(0).replace('(\D*)', '', regex=True).astype(int)  # Чем меньше тем лучше
df['authorized_capital'] = df['authorized_capital'].fillna(10000).replace('(\D*)', '', regex=True).astype(int)
df['reviews_count'] = df['reviews_count'].fillna(0).replace('(\D*)', '', regex=True).astype(int)

df['planned_checks'] = df['planned_checks'].fillna(0).astype(int)
df['unplanned_checks'] = df['unplanned_checks'].fillna(0).astype(int)
df['infringement'] = df['infringement'].fillna(0).astype(int)  # Чем меньше тем лучше
df['not_infringement'] = df['not_infringement'].fillna(0).astype(int)
df['unknown_infringement'] = df['unknown_infringement'].fillna(0).astype(int)  # Чем меньше тем лучше

df['date_reg'] = pd.to_datetime(df['date_reg'].fillna(pd.to_datetime('today').date()))  # Чем меньше тем лучше

try:
    df.drop(columns=['name', 'probable_name'], inplace=True)
except KeyError:
    pass

rangingFields_temp1 = [df[column_name] for column_name in ranging_fields]
rangingFields_temp2 = [df[column_name] for column_name in ranging_fields_reverse_true]
rangingFields1 = [range_values(field) for field in rangingFields_temp1]
rangingFields2 = [range_values(field, reverse=True) for field in rangingFields_temp2]
rangingFields = rangingFields1 + rangingFields2

grades = df['grade']
yandexRatings = df['yandex_rating']

binaryFields = [df[column_name] for column_name in binary_fields]

ratings = get_ratings(rangingFields, grades, yandexRatings, binaryFields)
max_rating = max(ratings)
ratings_norm = [rating / max_rating for rating in ratings]

# веса для полей ranging_fields + ranging_fields_reverse_true
# ['place_in_search', 'details_num', 'authorized_capital', 'planned_checks', 'unplanned_checks',
#                   'reviews_count', 'not_infringement'] +
# ['date_reg', 'fines', 'infringement', 'unknown_infringement']
weights = [15, 45, 5, 2, 2, 20, 2, 10, 5, 2, 2]

ratings_ww = get_ratings_with_weights(rangingFields, grades, yandexRatings, binaryFields, weights)
max_rating_ww = max(ratings_ww)
ratings_ww_norm = [rating / max_rating_ww for rating in ratings_ww]

with open('data.jl', 'r') as file:
    dicts = []
    for line in file.readlines():
        dicts.append(json.loads(re.findall(r'({.*?})', line)[0]))
    df_initial = pd.DataFrame.from_records(dicts)
    df_initial.drop_duplicates(subset='domain', keep='last')
df_initial.to_csv('data_temp.csv', index=False)
df_initial = pd.read_csv('data_temp.csv')

ratings_norm = [round(rating, 3) for rating in ratings_norm]
ratings_ww_norm = [round(rating, 3) for rating in ratings_ww_norm]

df_initial['rating'] = ratings_norm
df_initial['rating_2'] = ratings_ww_norm
df_initial.to_csv('data.csv', index=False)
