import json
import pandas as pd
import os

_curr_path = os.path.dirname(os.path.realpath(__file__))
_filename = os.path.join(_curr_path, '..', 'content_dictionary', 'data', 'education_content_dictionary.json')

_file = open(_filename, 'r')
json_data = json.loads(_file.read())
_file.close()

columns = ['content_id', 'taxons', 'basepath', 'title', 'body']
content_dictionary = pd.DataFrame(json_data, columns=columns)

def total_number_of_concepts():
  s = calc_cumulative_concepts(content_dictionary)
  return s.iloc[-1]

def total_number_of_pages():
  return len(content_dictionary)

def calc_cumulative_concepts(df):
  set_of_taxons = set([])
  cumulative = []

  for i, row in df.iterrows():
    set_of_taxons |= set(row['taxons'])
    cumulative.append(len(set_of_taxons))

  return pd.Series(cumulative)
