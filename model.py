import json
import pandas as pd 
import numpy as np
import io
from sklearn.linear_model import RidgeCV, RidgeClassifierCV


prefix = 'C:/users/Victor/Documents/selectives/master_dataset_schools.csv' 
foei_path = 'C:/users/Victor/Documents/selectives/foei_funding_2019.csv'
ram_path = 'C:/users/Victor/Documents/selectives/data-hub-2020-approved.csv'
naplan_path = 'c:/users/victor/documents/selectives/naplan_cleaned.csv'

distinguished_cols = ['latest_year_enrolment_fte','indigenous_pct','lbote_pct','icsea_value',
'selective_school', 'school_gender', 'asgs_remoteness', 'healthy canteen']

foei_df = pd.read_csv(foei_path)
foei_df.columns = list(map(str.lower, foei_df.columns))
foei_df.dropna(subset = ['average_foei'], inplace = True)
foei_df['average_foei'].replace(' 3 or Less ', 3, inplace = True)

foei_df = foei_df[foei_df['average_foei'] != ' NA '][['average_foei', 'school_code']].copy()
foei_df['average_foei'] = foei_df['average_foei'].astype('int')

schools = pd.read_csv(prefix)
schools.columns = list(map(str.lower, schools.columns))

funding_df = pd.read_csv(ram_path)
funding_df.columns = list(map(str.lower, funding_df.columns))

naplan_df = pd.read_csv(naplan_path)
naplan_df = naplan_df[['age id', 'icsea', 'mean_naplan_yr9']]

filtered_schools = schools[(schools['level_of_schooling'] == 'Secondary School')&
                        (~pd.isnull(schools['icsea_value']))][distinguished_cols + ['school_code', 'ageid']].copy()

filtered_schools = filtered_schools.merge(foei_df, how = 'left', on = 'school_code')
# filtered_schools = filtered_schools.merge(funding_df)

filtered_schools['lbote_pct'].replace('np', 0, inplace = True)
filtered_schools['indigenous_pct'].replace('np', 0, inplace = True)
filtered_schools['latest_year_enrolment_fte'].fillna(0, inplace = True)

selective = pd.concat([filtered_schools, 
        pd.get_dummies(filtered_schools['selective_school'], prefix = 'schooltype')],
        axis = 1)

expanded = pd.concat([selective, 
        pd.get_dummies(selective['asgs_remoteness'], prefix = 'remoteness')],
        axis = 1)

expanded.dropna(axis = 0, subset = ['average_foei'], inplace = True)

naplan_master = pd.merge(naplan_df, expanded, how = 'left', left_on = 'age id', right_on = 'ageid')
naplan_master.dropna(inplace = True, axis = 0)
print(naplan_master.shape)
naplan_master['average_foei'] = (naplan_master['average_foei'] - np.mean(naplan_master['average_foei']))/(np.std(naplan_master['average_foei']))

naplan_master['indigenous_pct'] = (naplan_master['indigenous_pct'].astype('float') - np.mean(naplan_master['indigenous_pct'].astype('float')))/(np.std(naplan_master['indigenous_pct'].astype('float')))


features = [
#     'indigenous_pct', 
    # 'lbote_pct',
    'average_foei',
    # 'icsea_value',
#   'schooltype_Fully Selective',
#   'schooltype_Not Selective', 
# 'schooltype_Partially Selective',
#   'remoteness_Inner Regional Australia',
#   'remoteness_Major Cities of Australia',
#   'remoteness_Outer Regional Australia', 'remoteness_Remote Australia'
]

response = 'mean_naplan_yr9'


ridge = RidgeCV(alphas = [0.1, 1, 5, 10], normalize = False, store_cv_values = True)\
    .fit(naplan_master[features], naplan_master[response])

print(ridge.score(naplan_master[features], naplan_master[response]))

print(ridge.alpha_, ridge.cv_values_)

print(ridge.coef_)
