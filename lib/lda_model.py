from textacy import preprocess
from html.parser import HTMLParser
from gensim.utils import lemmatize
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora, models
import gensim
import textacy
import glob
import os
import pickle

class LdaModel():
  def __init__(self, filename, num_topics):
    self.filename = filename + '_' + str(num_topics)
    self.corpus_filename = self.filename + '_corpus'
    self.stopwords = self.stopwords()
    self.num_topics = num_topics

  # expects a pandas dataframe
  def train_model(self, content_dictionary, cores=1):
    dictionary, corpus = build_corpus(content_dictionary)
    model = gensim.models.ldamulticore.LdaMulticore(
      corpus,
      num_topics=self.num_topics,
      id2word=dictionary,
      passes=50,
      workers=cores
    )
    self.save_model(model)
    self.save_corpus(corpus)
    return model

  def build_corpus(self, content_dictionary):
    self.phrases = self.phrases_from_content(content_dictionary)
    dictionary = self.build_dictionary(self.phrases)
    corpus = [dictionary.doc2bow(text) for text in self.phrases]
    return dictionary, corpus

  def no_pretrained_model_exists(self):
    return not ( os.path.isfile(self.filename) and
      os.path.isfile(self.corpus_filename) )

  def save_model(self, model):
    model.save(self.filename)

  def load_model(self):
    return gensim.models.LdaModel.load(self.filename)

  def save_corpus(self, corpus):
    pickle.dump( corpus, open(self.corpus_filename, 'wb') )

  def load_corpus(self):
   return pickle.load( open( self.corpus_filename, "rb" ) )

  def build_dictionary(self, phrases):
    dictionary = corpora.Dictionary(phrases)
    # these parameters need tuning to the volume of content
    # the no_below parameter takes an absolute number of documents
    # no_above is a percentage of the corpus
    # see https://radimrehurek.com/gensim/corpora/dictionary.html
    dictionary.filter_extremes(no_below=20, no_above=0.15, keep_n=None)
    return dictionary

  def phrases_from_content(self, content_dictionary):
    phrases = []
    for index, row in content_dictionary.iterrows():
      raw_text = ' '.join([row['body'], row['title'], row['basepath'], row.get('description', '')])
      clean_text = self.clean_text(raw_text)
      phrases.append( self.phrases(clean_text) )
    return phrases

  def phrases(self, clean_text):
    all_lemmas = lemmatize( clean_text, stopwords=self.stopwords )
    curated_words = [word.split('/')[0] for word in all_lemmas]
    curated_text = ' '.join(curated_words)

    doc = textacy.Doc(str(curated_text.decode('ascii', 'ignore')), lang='en')

    all_phrases = []
    all_phrases += textacy.extract.ngrams(doc, 2, filter_stops=True, filter_punct=True, filter_nums=True)
    all_phrases += textacy.extract.ngrams(doc, 3, filter_stops=True, filter_punct=True, filter_nums=True)
    all_phrases += textacy.extract.ngrams(doc, 4, filter_stops=True, filter_punct=True, filter_nums=True)
    all_phrases += textacy.extract.ngrams(doc, 5, filter_stops=True, filter_punct=True, filter_nums=True)

    phrases = [str(phrase) for phrase in all_phrases]

    return phrases

  def clean_text(self, raw_text):
    raw_text = self.strip_tags(raw_text)
    raw_text = raw_text.lower()
    raw_text = preprocess.remove_punct(raw_text)
    raw_text = preprocess.transliterate_unicode(raw_text)
    raw_text = preprocess.replace_urls(raw_text, replace_with='')
    raw_text = preprocess.replace_emails(raw_text, replace_with='')
    raw_text = preprocess.replace_phone_numbers(raw_text, replace_with='')
    raw_text = preprocess.replace_numbers(raw_text, replace_with='')
    raw_text = preprocess.replace_currency_symbols(raw_text, replace_with='')
    return raw_text

  def strip_tags(self, htmlish):
    s = MLStripper()
    s.feed(htmlish)
    return s.get_data()

  def stopwords(self):
    stopwords = []
    for filename in glob.glob('../stopwords/*.txt'):
      with open(filename) as fileobj:
        for line in fileobj:
          line = self.clean_text(line.decode('utf8').strip())
          if line:
            stopwords.append(line)

    return stopwords + [word.decode('utf8') for word in STOPWORDS]

class MLStripper(HTMLParser):
  def __init__(self):
    self.reset()
    self.fed = []
  def handle_data(self, d):
    self.fed.append(d)
  def get_data(self):
    return ''.join(self.fed)
