# Script for fetching the imdb api data for budget and revenue for each movie in our dataset

# 1. Import raw dataset
# 2. Iterate through df
# 3. Save the imdb id
# 4. API call with that id
# 5. Parse the json for revenue and budget
# 6. Maybe process them if needed
# 7. If there are values, write them in the budget and revenue column of the df
# 8. If not, do nothing


import pandas as pd
import numpy as np
import requests
import math

df = pd.read_csv('../../data/raw/movies_metadata.csv')
#remove NaN's from imdb_id column
df = df[pd.notnull(df['imdb_id'])]
#remove rows where imdb_id is 0
df = df[df.imdb_id != '0']

df.sort_values(by='imdb_id', ascending=False)


#base url for request. Later: append the imdb_id
base_url = "https://theimdbapi.org/api/movie?movie_id="


for index, row in df.iterrows():
    imdb_id = row['imdb_id']
    # build url
    url = base_url + imdb_id

    # api call
    r = requests.get(url)
    # fetch json
    j = r.json()

    # Budget processing
    revenue_raw = j['metadata']['gross']

    revenue = process_json(gross_raw)

    #prints for debugging
    print(revenue)

    # check if the revenue is not null, then write it to the df
    #if revenue != 0:
        #row['revenue'] = revenue


def process_json(json):
    # split  into array because of additional information
    json_processed = json.split(' ')[0]
    # only extract digits from processed json
    result = ''.join([i for i in json_processed if i.isdigit()])

    return float(result)
