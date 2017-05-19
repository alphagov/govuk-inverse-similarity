# -*- coding: utf-8 -*-

import pandas as pd
import content_dictionary as cd
import numpy as np

def get_averaged_result(num_rounds):
  samples = []
  for i in range(1, num_rounds):
    s = cd.content_dictionary.sample(frac=0.4)
    samples.append(cd.calc_cumulative_concepts(s))

  random_results = pd.DataFrame(samples).T
  random_results['Mean'] = random_results.mean(axis=1)
  return random_results

def percentage_as_string(nom, denom, dps):
  p = (nom / float(denom)) * 100
  if(dps == 0):
    string = str(int(round(p, dps))) + '%'
  else:
    string = str(round(p, dps)) + '%'
  return string

# expects results to be a pandas Series, and term_limit to be numeric
def number_of_pages_reviewed_before_term_limit_reached(results, term_limit):
  page_count = sum(results.apply(lambda s: s < term_limit))
  return page_count


def print_80_90_95th_percentiles(results):
  num_rounds = len(results.columns)

  print
  print 'Analysis of Education themed content.'
  print 'Baseline for optimal content-ordering experiment.'
  print 'For ', num_rounds, 'rounds of randomly ordered pages:'
  print

  for percentage_of_terms in [0.5, 0.8, 0.9, 0.95]:
    max_concepts = cd.total_number_of_concepts()
    term_limit = max_concepts * percentage_of_terms

    pages = results.apply(number_of_pages_reviewed_before_term_limit_reached, args=[term_limit])

    pd_pages = pd.Series(pages)
    std = int(round(pd_pages.std()))
    mean = int(round(pd_pages.mean()))
    min = pd_pages.min()
    max = pd_pages.max()
    percent_of_corpus = percentage_as_string(mean, cd.total_number_of_pages(), 1)
    terms = percentage_as_string(term_limit, cd.total_number_of_concepts(), 0)

    str = "{terms} of terms were found by reviewing an average of {mean!s} pages. {percent_of_corpus} of corpus, σ {std!s}, range {min!s} - {max!s}".format(**locals())
    print str
