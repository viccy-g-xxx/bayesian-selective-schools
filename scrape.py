import pandas as pd 
import numpy as np
import requests
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


#init
acara_path = 'C:/Users/Victor/Downloads/acara_schools.xlsx'

acara_df = pd.read_excel(acara_path)
acara_df.columns = acara_df.columns.map(str.lower)
acara_df = acara_df[(acara_df['school type'].isin(['Secondary', 'Combined']))&
                    (acara_df['state'] == 'NSW')].copy()

for school_id in acara_df['acara sml id']:
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")
    # options.add_argument("--log-level=3")
    # ua = UserAgent()
    # userAgent = ua.random
    # print(userAgent)
    # options.add_argument(f'user-agent={userAgent}')
    dr = webdriver.Chrome(options=options)

    url = 'https://www.myschool.edu.au/school/{}/naplan/results/2019#results'.format(school_id)
    print(url)
    dr.get(url)
    #get past accept page
    dr.find_element_by_xpath("//input[@class='accept' and @value='Accept']").click()

    try: 
        naplan = dr.find_element_by_id('similarSchoolsTable').text
    except Exception as e:
        print(e)
        naplan = 'no naplan results found for ' + url
    dr.quit()
    acara_df.loc[acara_df['acara sml id'] == school_id, 'naplan hist'] = naplan

acara_df.to_csv('c:/users/victor/documents/selectives/naplan.csv', index = False)
    


