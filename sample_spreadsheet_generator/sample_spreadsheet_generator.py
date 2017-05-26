#! ../baseline_performance/.venv/bin/python

"""
Generate a spreadsheet of inversely-similar content for the purposes of
building the beginnings of a taxonomy.
"""
import argparse
import os
import sys

parser = argparse.ArgumentParser(description=__doc__)
content_source_parser = parser.add_mutually_exclusive_group(required=True)

content_source_parser.add_argument(
  '--basepaths',
  metavar='filename',
  dest='basepaths_filename',
  help='file should contain GOV.UK basepaths on seperate lines',
)

content_source_parser.add_argument(
  '--content-dictionary',
  metavar='filename',
  dest='content_dictionary_filename',
  help='filename of a previously generated content-dictionary'
)

parser.add_argument(
  '--model',
  metavar='filename',
  dest='model_filename',
  help='filename of a trained LDA model, or filename for the newly trained model',
  default='trained_lda_model'
)

parser.add_argument(
  '--topics',
  type=int,
  dest='num_topics',
  help='the number of topics with which to train the LDA model',
  default=100
)

parser.add_argument(
  '--affinity-theshold',
  type=float,
  dest='affinity_threshold',
  help='threshold affinity value for the topic clustering algorithm',
  default=0.3
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

  def absolute_path(filename):
    path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(path, args.data_dir, filename)

  def file_exists(filename):
    if filename is None:
      return False
    return os.path.isfile( absolute_path(filename) )

  if file_exists(args.basepaths_filename):
    content_directory = content.build_content_directory(
      filename=absolute_path(args.basepaths_filename),
      url=args.remote_url,
      niceness=args.niceness
    )
  elif file_exists(args.content_dictionary_filename):
    content_directory = content.load_content_directory(
      filename=absolute_path(args.content_dictionary_filename)
    )
  else:
    print "Error, file not found."
    sys.exit(1)

  if file_exists(args.model_filename):
    lda_model = lda_model.load_model(
      filename=absolute_path(args.model_filename)
    )
  else:
    lda_model = lda_model.train_model(
      filename=absolute_path(args.model_filename),
      content_directory=content_directory,
      num_topics=args.num_topics
    )

  sampled_pages = difference_sampler.sample_pages(
    lda_model=lda_model,
    content_directory=content_directory,
    affinity_threshold=args.affinity_threshold,
  )

  # do something with the sampled pages. Dunno, save them maybe?

