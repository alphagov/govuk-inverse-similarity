import pandas as pd
from tqdm import tqdm
import time
from multicore_runner import run_multicore

class DifferenceSampler:
  def __init__(self, model_class):
    self.model = model_class.load_model()
    self.corpus = model_class.load_corpus()

  def sample_pages(self, content_dictionary, affinity_threshold, cores=1):
    content_dictionary['topics'] = run_multicore(cores, self.assign_topics, self.corpus)
    self.topic_affinity_threshold = affinity_threshold
    return self.naive_clustering_by_topic(content_dictionary)

  def assign_topics(self, corpus_pages, index):
    print ' - process', index, 'assigning topics to', len(corpus_pages), 'pages'
    topics = []
    for bow in corpus_pages:
      topics.append(self.model[bow])
    return {index: topics}

  def naive_clustering_by_topic(self, content):
    # filter topics with probability < eg 30%
    # then throw away the probabilities
    # sort topic indices numerically
    # these are the topic groups
    topic_groups = []
    for index, row in content.iterrows():
      topics = []
      for topic in row['topics']:
        if topic[1] >= self.topic_affinity_threshold:
          topics.append(topic[0])
      topics.sort
      topic_groups.append( tuple(topics) )

    content['topic_group'] = topic_groups

    # use sets to see if a topic group has been used before
    # - if so, ignore the page
    # - if not, add it to the list of pages to review
    previously_seen_topic_groups = set([])
    pages_to_review = []
    for index, row in content.iterrows():
      topic_group = row['topic_group']
      if topic_group not in previously_seen_topic_groups:
        previously_seen_topic_groups.add(topic_group)
        pages_to_review.append(row)

    return pd.DataFrame(pages_to_review)
