#! ../.venv/bin/python

"""
Generate a spreadsheet of inversely-similar content for the purposes of
building the beginnings of a taxonomy.
"""
import argparse
import os
import sys

from content_dictionary import ContentDictionary
from lda_model import LdaModel
from difference_sampler import DifferenceSampler
from output_builder import OutputBuilder

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument(
  '--theme-name',
  metavar='THEME',
  dest='theme_name',
  help='name of the theme, which will be used to magic up filenames etc',
  required=True
)

parser.add_argument(
  '--topics',
  type=int,
  dest='num_topics',
  help='the number of topics with which to train the LDA model',
  default=50
)

parser.add_argument(
  '--affinity-threshold',
  type=float,
  dest='affinity_threshold',
  help='threshold affinity value for the topic clustering algorithm',
  default=0.1
)

parser.add_argument(
  '--data-dir',
  dest='data_dir',
  help='directory for working data',
  default='../data'
)

parser.add_argument(
  '--niceness',
  dest='niceness',
  help='how many milliseconds to wait before repeating an API call',
  default=10,
  type=int
)

parser.add_argument(
  '--remote',
  dest='remote_url',
  help='content store URL',
  default='https://www.gov.uk/api/content'
)

if __name__ == '__main__':
  args = parser.parse_args()

  basepaths_filename = args.theme_name + '_basepaths.csv'
  content_dictionary_filename = args.theme_name + '_content_dictionary.json'
  model_filename = args.theme_name + '_model'
  output_filename = args.theme_name + '_sample_spreadsheet.csv'

  def absolute_path(filename):
    path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(path, args.data_dir, filename)

  def file_exists(filename):
    if filename is None:
      return False
    return os.path.isfile( absolute_path(filename) )

  if file_exists(content_dictionary_filename):
    print 'Loading content dictionary'
    content_dictionary = ContentDictionary().load(
      filename=absolute_path(content_dictionary_filename)
    )
  elif file_exists(basepaths_filename):
    print 'Building content dictionary...'
    content_dictionary = ContentDictionary().build(
      basepaths_filename=absolute_path(basepaths_filename),
      dictionary_filename=absolute_path(content_dictionary_filename),
      url=args.remote_url,
      niceness=args.niceness
    )
  else:
    print "Error, file not found."
    sys.exit(1)

  model_class = LdaModel( absolute_path(model_filename), num_topics=args.num_topics )

  if model_class.no_pretrained_model_exists():
    print 'Training model'
    model_class.train_model(
      content_dictionary=content_dictionary
    )
  else:
    print 'Loading model'

  print 'Clustering and sampling'
  sampled_pages = DifferenceSampler(model_class).sample_pages(
    content_dictionary=content_dictionary,
    affinity_threshold=args.affinity_threshold,
  )

  print str( len(sampled_pages) ) + ' sampled / ' + str( len(content_dictionary) ) + ' total'

  print 'Writing output spreadsheet'
  OutputBuilder(sampled_pages).write_to_file(
    absolute_path(output_filename)
  )

  print '✅ Done'

