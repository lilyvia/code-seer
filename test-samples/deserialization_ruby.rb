require 'msgpack'
require 'oj'

user_data = params[:data]

Marshal.load(user_data)
Marshal.restore(user_data)
YAML.load(user_data)
JSON.load(user_data)
Oj.load(user_data)
Oj.object_load(user_data)
MessagePack.unpack(user_data)
MessagePack.load(user_data)
JSON.parse(user_data, create_additions: true)
