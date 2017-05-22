import content_dictionary as cd
from textacy import preprocess
from HTMLParser import HTMLParser
from gensim.utils import lemmatize
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora
import re
import textacy
import glob
import pickle
import os

_curr_path = os.path.dirname(os.path.realpath(__file__))

content_dictionary = cd.content_dictionary

class MLStripper(HTMLParser):
  def __init__(self):
    self.reset()
    self.fed = []
  def handle_data(self, d):
    self.fed.append(d)
  def get_data(self):
    return ''.join(self.fed)

def strip_tags(html):
  s = MLStripper()
  s.feed(html)
  return s.get_data()

PUNCTUATION_REGEX = re.compile(r'\W|[_0-9]', flags=re.UNICODE)

def preprocess_unicode(raw_text):
  raw_text = preprocess.transliterate_unicode(raw_text.lower())
  raw_text = preprocess.replace_urls(raw_text, replace_with=u'')
  raw_text = preprocess.replace_emails(raw_text, replace_with=u'')
  raw_text = preprocess.replace_phone_numbers(raw_text, replace_with=u'')
  raw_text = preprocess.replace_numbers(raw_text, replace_with=u'')
  raw_text = preprocess.replace_currency_symbols(raw_text, replace_with=u'')
  return raw_text

def phrases_in_raw_text_via_textacy(raw_text):
  """
  Builds a list of phrases from raw text using textacy.
  """
  all_lemmas = lemmatize(raw_text, stopwords=STOPWORDS_UNICODE)
  curated_words = [word.split('/')[0] for word in all_lemmas]
  curated_text = ' '.join(curated_words)

  doc = textacy.Doc(unicode(curated_text.decode('ascii', 'ignore')), lang=u'en')

  all_phrases = []
  all_phrases += textacy.extract.ngrams(doc, 2, filter_stops=True, filter_punct=True, filter_nums=True)
  all_phrases += textacy.extract.ngrams(doc, 3, filter_stops=True, filter_punct=True, filter_nums=True)
  all_phrases += textacy.extract.ngrams(doc, 4, filter_stops=True, filter_punct=True, filter_nums=True)
  all_phrases += textacy.extract.ngrams(doc, 5, filter_stops=True, filter_punct=True, filter_nums=True)

  phrases = [unicode(phrase) for phrase in all_phrases]

  return phrases

def clean_text(htmlsoup):
  wordsalad = strip_tags(htmlsoup)
  alphabet_spaghetti = re.sub(PUNCTUATION_REGEX, ' ', wordsalad)
  return preprocess_unicode(alphabet_spaghetti)


def load_stopwords():
  stopwords = []
  for filename in glob.glob('../stopwords/*.txt'):
    with open(filename) as fileobj:
      for line in fileobj:
        line = preprocess_unicode(line.decode('utf8').strip())
        line = preprocess.remove_punct(line)
        if line:
          stopwords.append(line)

  return stopwords + [word.decode('utf8') for word in STOPWORDS]


STOPWORDS_UNICODE = load_stopwords()
STOPWORDS_BYTES = [word.encode('utf8') for word in STOPWORDS_UNICODE]

def dictionary():
  filename = os.path.join(_curr_path, '..', 'data', 'dictionary')

  if os.path.isfile(filename):
    dictionary = corpora.Dictionary.load(filename)
  else:
    phrases = get_phrases()
    dictionary = corpora.Dictionary(phrases)
    dictionary.filter_extremes(no_below=20, no_above=0.15, keep_n=None)
    corpora.Dictionary.save(_filename)

  return dictionary

def phrases():
  filename = os.path.join(_curr_path, '..', 'data', 'phrases.pickle')

  if os.path.isfile(filename):
    print "Loading phrases"
    phrases = pickle.load( open( filename, "rb" ) )
  else:
    print "generating phrases"
    phrases = []

    for index, row in content_dictionary.iterrows():
      text = clean_text(' '.join([row['body'], row['title'], row['basepath']]))
      phrases.append(phrases_in_raw_text_via_textacy(text))

    pickle.dump( phrases, open(filename, 'wb'))
  return phrases

