require 'mongo'

# 负样本 - 使用固定字段和类型转换
def safe_fixed_filter(collection, email)
  collection.find({ "email" => email.to_s })
end

# 负样本 - 使用允许名单验证字段名
def safe_allowlisted_field(collection, field, value)
  allowed_fields = %w[email status role]
  raise "invalid field" unless allowed_fields.include?(field)
  collection.find({ field => value.to_s })
end

# 负样本 - 显式构造查询（不使用动态字段）
def safe_typed_query(collection, username, password)
  collection.find({
    "username" => username.to_s,
    "password" => password.to_s
  })
end

# 负样本 - count_documents 使用固定字段
def safe_count_documents(collection, status)
  collection.count_documents({ "status" => status.to_s })
end

# 负样本 - aggregate 使用硬编码 pipeline
def safe_aggregate(collection)
  pipeline = [
    { "$match" => { "status" => "active" } },
    { "$group" => { "_id" => "$category", "count" => { "$sum" => 1 } } }
  ]
  collection.aggregate(pipeline)
end

# 负样本 - 静态 hash 构造
def safe_static_hash(collection, user_id)
  query = { "user_id" => user_id.to_s }
  collection.find(query)
end

# 负样本 - Mongoid 使用强参数
def safe_mongoid_strong_params(params)
  allowed = params.permit(:username, :email)
  User.where(allowed.to_h)
end
