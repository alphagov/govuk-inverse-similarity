import urllib, json, time

class ContentDictionary():
  def load(self, filename):
    with open(filename, 'rb') as infile:
      return json.loads( infile.read() )

  def build(self, basepaths_filename, dictionary_filename, url, niceness):
    self.basepaths_filename = basepaths_filename

    pages = []
    for path in self.basepaths():
      page_data = Page(url, path).to_dict()
      if bool(page_data):
        print path
        pages.append(page_data)
      time.sleep(niceness)

    with open(dictionary_filename, 'w') as outfile:
      json.dump(pages, outfile)

    return pages

  def basepaths(self):
    file = open(self.basepaths_filename, 'r')
    data = file.read().split("\n")
    file.close()
    return data

class Page():
  def __init__(self, url, basepath):
    self.data = self.fetch_data(url + basepath)
    self.unprocessable_types = [
      'smart_answer',
      'organisation',
      'policy',
      'national_statistics_announcement',
      'statistics_announcement'
    ]

  def to_dict(self):
    if self.processable():
      return {
        'content_id': self.data['content_id'],
        'basepath': self.data['base_path'],
        'title': self.data['title'],
        'body': self.body_content()
      }
    else:
      return {}

  def processable(self):
    return self.data is not None and self.processable_content_type() and self.body_content()

  def processable_content_type(self):
    return self.data['document_type'] not in self.unprocessable_types

  def body_content(self):
    if ( self.data['schema_name'] in ['transaction','local_transaction'] ):
      body_keys = ['introductory_paragraph','more_information','introduction']
      details_dict = self.data['details']
      for key in details_dict.keys():
        if key not in body_keys:
          del details_dict[key]
      return ' '.join(details_dict)

    elif ( 'parts' in self.data['details'].keys() ):
      return " ".join( part['body'] for part in self.data['details']['parts'] )

    elif ( 'collection_groups' in self.data['details'].keys() ):
      return " ".join( part['body'] for part in self.data['details']['collection_groups'] )

    elif ( self.data['document_type'] == 'licence' ):
      return self.data['details']['licence_short_description'] + self.data['details']['licence_overview']
    elif 'body' in self.data.keys():
      return self.data['details']['body']
    else:
      return None

  def fetch_data(self, url):
    try:
      response = urllib.urlopen(url)
      return json.loads(response.read())
    except:
      pass
