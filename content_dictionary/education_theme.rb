# USAGE
# From the command line:
# $ ruby -r './education_theme' -e 'EducationTheme.new.save_as_json'

require 'http'
require 'uri'

class EducationTheme
  API_HOST = "www.gov.uk".freeze
  API_PATH = "/api/search.json".freeze
  EDUCATION_TAXONOMY = "c58fdadd-7743-46d6-9629-90bb3ccc4ef0".freeze

  def initialize
    @urls = construct_urls
  end

  def content_items
    save_as_json unless File.exists?(filename)
    from_file
  end

  def save_as_json
    File.write(filename, JSON.pretty_generate(results))
  end

  def from_file
    JSON.parse(File.read(filename))
  end

  private

  def filename
    File.join(__dir__, 'data', '_education_theme.json')
  end

  def results
    @urls
      .map { |url| HTTP.get(url) }
      .map { |doc| JSON.parse(doc) }
      .map { |json| json["results"] }
      .flatten
      .map { |hsh| hsh.merge(basepath: hsh['_id']) }
  end

  def construct_urls
    urls = []
    10.times do |i|
      urls << URI::HTTPS.build(host: API_HOST, path: API_PATH, query: params(i))
    end
    urls
  end

  def params(i)
    URI.encode_www_form({
      count: 1000,
      start: i * 1000,
      'filter_part_of_taxonomy_tree[]': EDUCATION_TAXONOMY,
      fields: 'taxons'
    })
  end
end
