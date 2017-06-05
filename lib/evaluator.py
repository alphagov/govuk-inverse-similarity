# coding: utf-8
import pandas as pd
from lda_model import LdaModel
from difference_sampler import DifferenceSampler

# expects content_dictionary to have a 'taxons' field, containing an array of strings
class Evaluator:
  def __init__(self, model_filename, content_dictionary):
    self.model_filename = model_filename
    self.content_dictionary = content_dictionary

    self.topic_numbers = [1000, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]
    self.affinities = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65]

    self.eighty_percent_of_terms = self.calc_80_percent_of_total_terms()

    self.results = self.run_evaluation()

  def save_results(self):
    pd.DataFrame(self.results).to_csv(self.model_filename + '_evaluation.csv', encoding='utf-8')

  def run_evaluation(self):
    results = []
    for num_topics in self.topic_numbers:
      model = LdaModel( self.model_filename, num_topics=num_topics )
      if model.no_pretrained_model_exists():
        print 'Training model with', num_topics, 'topics'
        model.train_model(self.content_dictionary)
      else:
        print 'Loading model with', num_topics, 'topics'

      print 'Testing against affinity matrix'
      for affinity in self.affinities:
        sampled_pages = DifferenceSampler(model).sample_pages(
          content_dictionary=self.content_dictionary,
          affinity_threshold=affinity
        )

        topic_affinity_result = self.get_results(sampled_pages)
        topic_affinity_result.update({'topics': num_topics, 'affinity': affinity, 'sample_size': len(sampled_pages)})
        results.append(topic_affinity_result)
    return results

  def get_results(self, sampled_pages):
    results = []
    for i in range(0, 1000):
      randomized_data = sampled_pages.sample(frac=1).reset_index(drop=True)
      e = self.how_many_pages_to_review_before_80_percent_of_terms_found(randomized_data)
      results.append(e)
    results = pd.DataFrame(results)
    return {'mean': results.mean()[0], 'std': results.std()[0]}

  def cumulative_terms(self, content_df):
    terms = set([])
    cumulative_terms = []
    for i, row in content_df.iterrows():
      row_count = 0
      for current_term in row['taxons']:
        if not current_term in terms:
          terms |= set([current_term])
      cumulative_terms.append( len(terms) )
    return cumulative_terms

  def how_many_pages_to_review_before_80_percent_of_terms_found(self, content_df):
    cumulative_terms_list = self.cumulative_terms(content_df)
    return sum(s < self.eighty_percent_of_terms for s in cumulative_terms_list)

  def calc_80_percent_of_total_terms(self):
    return self.cumulative_terms(self.content_dictionary)[-1] * 0.8

