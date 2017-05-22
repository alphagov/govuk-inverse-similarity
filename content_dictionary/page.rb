require 'http'

class Page
  attr_reader :basepath

  UNPROCESSABLE_FORMATS = %w(
    smart_answer
    organisation
    policy
    national_statistics_announcement
    statistics_announcement
  ).freeze

  def initialize(basepath)
    @basepath = basepath
  end

  def to_h
    if file_exists?
      load_as_json
    elsif processable?
      save_as_json(
        content_id: content_id,
        basepath: basepath,
        title: title,
        body: body_content
      )
    else
      {}
    end
  rescue
    {}
  end

  private

  def file_exists?
    File.exists?(filename)
  end

  def load_as_json
    JSON.parse(File.read(filename))
  end

  def save_as_json(attr_hash)
    File.write(filename, JSON.pretty_generate(attr_hash))
    attr_hash
  end

  def filename
    filename = basepath.gsub(/^\//, '').gsub('/', '_').gsub('-', '_')
    File.join(__dir__, '..', 'data', 'pages', "#{filename}.json")
  end

  def body_content
    @_body_content ||= begin
      if %w(transaction local_transaction).include? doc['schema_name']
        keys = %w(introductory_paragraph more_information introduction)
        doc['details']
          .select { |k,v| keys.include? k }
          .values
          .join(' ')
      elsif doc['details']['parts']
        doc['details']['parts'].each_with_object("") do |part, acc|
          acc << part['body']
        end
      elsif doc['details']['collection_groups']
        doc['details']['collection_groups'].each_with_object("") do |part, acc|
          acc << part['body']
        end
      elsif doc['document_type'] == 'licence'
        [
          doc['details']['licence_short_description'],
          doc['details']['licence_overview']
        ].join(' ')
      else
        doc['details']['body']
      end
    end
  end

  def processable?
    processable_format? && body_content
  end

  def processable_format?
    !UNPROCESSABLE_FORMATS.include?(doc['document_type'])
  end

  def title
    doc['title']
  end

  def content_id
    doc['content_id']
  end

  def doc
    @_doc ||= JSON.parse(HTTP.get(url))
  end

  def url
    "https://www.gov.uk/api/content#{basepath}"
  end
end
