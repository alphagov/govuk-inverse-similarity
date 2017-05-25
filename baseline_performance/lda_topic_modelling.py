from gensim import corpora, models
import gensim
import content_dictionary as cd
import dictionary_and_phrases as dp
import data
import os
import pandas as pd

# prerequisites
content_dictionary = cd.content_dictionary
phrases = dp.phrases()
dictionary = dp.dictionary()
corpus = [dictionary.doc2bow(text) for text in phrases]

def lda_model(num_topics):
  filename = "lda_model_%s" % num_topics

  if data.isfile(filename):
    print "Loading model"
    lda = gensim.models.LdaModel.load( data.filename_from_data_directory(filename) )
  else:
    print "Generating model"
    lda = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=50)
    lda.save( data.filename_from_data_directory(filename) )

  return lda

def naive_clustering_by_topic(content, topic_affinity_threshold):
  # filter topics with probability < eg 30%
  # then throw away the probabilities
  # sort topic indices numerically
  # these are the topic groups
  topic_groups = []
  for index, row in content.iterrows():
    topics = []
    for topic in row['topics']:
      if topic[1] >= topic_affinity_threshold:
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

  return pages_to_review

for num_topics in [10, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]:
  # get pretrained model
  lda = lda_model(num_topics)
  # find topics for each page
  topics = []
  for bow in corpus:
    topics.append(lda[bow])
  # assign to our page data
  content_dictionary['topics'] = topics

  for topic_affinity_threshold in [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]:
    # cluster by inverse similarity
    pages_to_review = naive_clustering_by_topic(content_dictionary, topic_affinity_threshold)

    # get the cumulative topic count
    inverse_similarity_order = cd.calc_cumulative_concepts( pd.DataFrame(pages_to_review) )
    magic_number = cd.threshold_analysis(pd.DataFrame(inverse_similarity_order), 0.8)

    print '80% of terms found in', magic_number[0], 'pages, with', num_topics, 'num topics, and', topic_affinity_threshold, 'topic affinity threshold.', len(pages_to_review), 'pages in set.'
