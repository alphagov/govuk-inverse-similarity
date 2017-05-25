# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import data

def load_content_dictionary():
  json_data = data.load_json_data('education_content_dictionary.json')
  columns = ['content_id', 'taxons', 'basepath', 'title', 'body']
  return pd.DataFrame(json_data, columns=columns)

# Load this up on import
print "Loading content dictionary"
content_dictionary = load_content_dictionary()

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

def random_results():
  filename = 'random_sampling.pickle'
  if data.isfile(filename):
    print "Loading Randomly sampled dataset"
    results = data.load_pickle_data(filename)
  else:
    print "Building Randomly sampled dataset"
    results = n_randomly_picked_pages(500)
    data.save_pickle_data(results, filename)
  return results

def n_randomly_picked_pages(n):
  samples = []
  for i in range(1, n):
    s = content_dictionary.sample(frac=0.4)
    samples.append(calc_cumulative_concepts(s))

  return pd.DataFrame(samples).T

def percentage_as_string(nom, denom, dps):
  p = (nom / float(denom)) * 100
  if(dps == 0):
    string = str(int(round(p, dps))) + '%'
  else:
    string = str(round(p, dps)) + '%'
  return string

def threshold_analysis(cumulative_series, percentage_of_terms):
  pages = cumulative_series.apply(number_of_pages_reviewed_before_term_limit_reached, args=[percentage_of_terms])
  return pd.Series(pages)

# expects results to be a pandas Series, and term_limit to be float as percentage eg 0.2
def number_of_pages_reviewed_before_term_limit_reached(results, percentage_of_terms):
  max_concepts = total_number_of_concepts()
  term_limit = max_concepts * percentage_of_terms
  page_count = sum(results.apply(lambda s: s < term_limit))

  return page_count

def print_percentiles(results, percentiles):
  for percentage_of_terms in percentiles:

    pages = threshold_analysis(results, percentage_of_terms)

    max_concepts = total_number_of_concepts()
    term_limit = max_concepts * percentage_of_terms

    std = int(round(pages.std()))
    mean = int(round(pages.mean()))
    min = pages.min()
    max = pages.max()

    percent_of_corpus = percentage_as_string(mean, total_number_of_pages(), 1)
    terms = percentage_as_string(term_limit, total_number_of_concepts(), 0)

    str = "{terms} of terms were found by reviewing an average of {mean!s} pages. {percent_of_corpus} of corpus, σ {std!s}, range {min!s} - {max!s}".format(**locals())
    print str
