require 'net/http'
require 'open-uri'
require 'rest-client'
require 'faraday'
require 'httparty'

user_url = params[:url]
Net::HTTP.get(URI(user_url))
open(user_url)
URI.open(user_url)
RestClient.get(user_url)
Faraday.get(user_url)
HTTParty.get(user_url)
Net::HTTP.get_response(URI(user_url))
Net::HTTP.post_form(URI(user_url), {})
