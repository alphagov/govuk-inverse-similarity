import os
import json
import pickle

def filename_from_data_directory(filename):
  curr_path = os.path.dirname(os.path.realpath(__file__))
  data_path = os.path.join(curr_path, '..', 'data')
  return os.path.join(data_path, filename)

def isfile(filename):
  return os.path.isfile(filename_from_data_directory(filename))

def get_file_contents(fn):
  filename = filename_from_data_directory(fn)
  file = open(filename, 'r')
  data = file.read()
  file.close()
  return data

def load_json_data(filename):
  return json.loads( get_file_contents(filename) )

def load_pickle_data(fn):
  filename = filename_from_data_directory(fn)
  return pickle.load( open( filename, "rb" ) )

def write_pickle_data(data, fn):
  filename = filename_from_data_directory(fn)
  pickle.dump( data, open(filename, 'wb'))

