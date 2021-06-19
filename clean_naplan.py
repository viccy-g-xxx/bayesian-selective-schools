import pandas as pd 
import numpy as np

naplan_path = 'c:/users/victor/documents/selectives/naplan.csv'

naplan_df = pd.read_csv(naplan_path)

def clean_naplan(sample):
    output = None
    if 'no naplan results' in sample:
        return output
    deconstructed = sample.split('\nYear')
    header = deconstructed[0].split(' ')

    year9results = [x for x in deconstructed if x.startswith(' 9')]  
    if len(year9results) > 0:
        year9results = year9results[0]
        
        if '-' in year9results:
            return None

        cleaned = year9results[3:].split('\n')
        output = dict(zip(header, cleaned)) 
        avg_val = np.mean([int(x) for x in output.values()])
        return output, avg_val

# naplan_df['naplan_results_yr9'], naplan_df['mean_naplan_yr9']
naplan_df[['naplan_results_yr9', 'mean_naplan_yr9']] = pd.DataFrame(naplan_df['naplan hist'].apply(clean_naplan).tolist())

naplan_df.to_csv('c:/users/victor/documents/selectives/naplan_cleaned.csv', index = False)





