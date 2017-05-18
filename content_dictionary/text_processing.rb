require 'nokogiri'

def words
  filter_punctuation(
    html_to_text(
      [
        body_content,
        title,
        basepath
      ].join(' ')
    )
  )
end


def html_to_text(html)
  Nokogiri::HTML(html).text
end

def filter_punctuation(words)
  words
    .gsub(/[\/\-,\n\.:]/, ' ')
    .strip
    .gsub(/\d+/, '')
    .split(/\s+/)
    .join(' ')
    .downcase
end
