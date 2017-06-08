import pandas as pd
from tqdm import tqdm
from multiprocessing import Process, Queue
import time

class DifferenceSampler:
  def __init__(self, model_class):
    self.model = model_class.load_model()
    self.corpus = model_class.load_corpus()

  def sample_pages(self, content_dictionary, affinity_threshold, cores=1):
    content_dictionary['topics'] = self.assign_topics_multicore(cores)
    self.topic_affinity_threshold = affinity_threshold
    return self.naive_clustering_by_topic(content_dictionary)

  def assign_topics_multicore(self, cores):
    pages = self.pages_for_each_core(cores)
    q = Queue()
    topics_unsorted = {}
    sorted_topics = []
    for i in range(0, cores):
      process = Process(target=self.assign_topics, args=(q, pages[i], i))
      process.start()
    while(True):
      topics_unsorted.update( q.get() )
      if len(topics_unsorted) == cores:
        break
      time.sleep(10)
    for i in range(0, cores):
      sorted_topics.extend(topics_unsorted[i])
    return sorted_topics

  def pages_for_each_core(self, cores):
    pages = []
    pages_per_core = len(self.corpus) / cores
    for i in range(0, cores):
      start = pages_per_core * i
      if i == (cores - 1):
        end = len(self.corpus)
      else:
        end = (pages_per_core * (i+1))
      pages.append(self.corpus[start:end])
    return pages


  def assign_topics(self, q, corpus_pages, i):
    topics = []
    print 'Process', i, 'assigning topics to', len(corpus_pages), 'pages'
    for bow in corpus_pages:
      topics.append(self.model[bow])
    q.put({i: topics})

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
