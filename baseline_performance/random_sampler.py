import pandas as pd
import content_dictionary as cd
import numpy as np

def get_averaged_result(num_rounds):
  samples = []
  for i in range(1, num_rounds):
    s = cd.content_dictionary.sample(frac=0.4)
    samples.append(cd.calc_cumulative_concepts(s))

  random_results = pd.DataFrame(samples).T
  return pd.DataFrame(random_results.mean(axis=1), columns=['Mean'])

def perc_of_pages(pages_reviewed):
  total_pages = cd.total_number_of_pages()
  p = (pages_reviewed / float(total_pages)) * 100
  return str(round(p, 1)) + '%'

def print_80_90_95th_percentiles(results, num_rounds):
  max_concepts = cd.total_number_of_concepts()
  results['100%'] = pd.Series(max_concepts, index=np.arange(len(results)))
  results['95%'] = pd.Series(max_concepts * 0.95, index=np.arange(len(results)))
  results['90%'] = pd.Series(max_concepts * 0.9, index=np.arange(len(results)))
  results['80%'] = pd.Series(max_concepts * 0.8, index=np.arange(len(results)))

  pages_80 = sum(results.apply(lambda s: s['80%'] > s['Mean'], axis=1)) + 1
  pages_90 = sum(results.apply(lambda s: s['90%'] > s['Mean'], axis=1)) + 1
  pages_95 = sum(results.apply(lambda s: s['95%'] > s['Mean'], axis=1)) + 1

  print
  print 'Analysis of Education themed content.'
  print 'Baseline for optimal content-ordering experiment.'
  print 'For average of', num_rounds, 'rounds of randomly ordered pages:'
  print
  print '80% of terms were found by reviewing', pages_80, 'pages.', perc_of_pages(pages_80), 'of corpus.'
  print '90% of terms were found by reviewing', pages_90, 'pages.', perc_of_pages(pages_90), 'of corpus.'
  print '95% of terms were found by reviewing', pages_95, 'pages.', perc_of_pages(pages_95), 'of corpus.'
