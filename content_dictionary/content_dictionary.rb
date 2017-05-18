# USAGE
# From the command line:
# $ ruby -r './content_dictionary' -e 'ContentDictionary.new.compile'

require_relative 'page'
require_relative 'education_theme'
require 'http'

class ContentDictionary
  FILENAME = "education_content_dictionary.json".freeze

  def compile
    @doc = theme.map do |r|
      attr_hash = page(r['_id'])
      attr_hash[:taxons] = r['taxons']
      attr_hash
    end.reject { |hsh| hsh.keys == [:taxons] }

    save_as_json
  end

  def page(basepath)
    Page.new(basepath).to_h
  end

  def theme
    @_theme ||= EducationTheme.new.content_items
  end

  def filename
    File.join(__dir__, 'data', FILENAME)
  end

  def save_as_json
    File.write(filename, JSON.pretty_generate(@doc))
  end
end

