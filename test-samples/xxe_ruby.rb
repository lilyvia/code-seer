require 'nokogiri'
require 'rexml/document'
require 'ox'

user_xml = params[:xml]
Nokogiri::XML(user_xml)
Nokogiri::XML::Reader(user_xml)
REXML::Document.new(user_xml)
Ox.parse(user_xml)
Ox.load(user_xml)
