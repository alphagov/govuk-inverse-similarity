import csv

class OutputBuilder():
  def __init__(self, sample_dictionary):
    self.sample_dictionary = sample_dictionary

  def write_to_file(self, filename):
    self.prepared_sample().to_csv(filename, encoding='utf-8')

  def prepared_sample(self):
    self.sample_dictionary['URL'] = "https://www.gov.uk" + self.sample_dictionary['basepath']
    columns = ['URL', 'title', 'description']
    return self.sample_dictionary[columns]
