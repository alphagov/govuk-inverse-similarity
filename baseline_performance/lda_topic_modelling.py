from gensim import corpora, models
import gensim
import corpora_dictionary as cd
import os
import pandas as pd

_curr_path = os.path.dirname(os.path.realpath(__file__))

content_dictionary = cd.content_dictionary
phrases = cd.phrases()
dictionary = cd.dictionary()
corpus = [dictionary.doc2bow(text) for text in phrases]


def lda_model():
  filename = os.path.join(_curr_path, 'data', 'lda_model')

  if os.path.isfile(filename):
    print "Loading model"
    lda = gensim.models.LdaModel.load(filename)
  else:
    print "Generating model"
    lda = gensim.models.ldamodel.LdaModel(corpus, num_topics=650, id2word=dictionary, passes=50)
    lda.save(filename)

  return lda

lda = lda_model()

# find topics for each page
topics = []
for bow in corpus:
  topics.append(lda[bow])
content_dictionary['topics'] = topics

# filter topics with probability < eg 50%
# then throw away the probabilities
# sort topic indices numerically
# these are the topic groups
topic_groups = []
for index, row in content_dictionary.iterrows():
  topics = []
  for topic in row['topics']:
    if topic[1] >= 0.3:
      topics.append(topic[0])
  topics.sort
  topic_groups.append( tuple(topics) )

content_dictionary['topic_group'] = topic_groups

# use sets to see if a topic group has been used before
# - if so, ignore the page
# - if not, add it to the list of pages to review
previously_seen_topic_groups = set([])
pages_to_review = []
for index, row in content_dictionary.iterrows():
  topic_group = row['topic_group']
  if topic_group not in previously_seen_topic_groups:
    previously_seen_topic_groups.add(topic_group)
    pages_to_review.append(row)

