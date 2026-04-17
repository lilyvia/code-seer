require 'mongo'

# 正样本 - $where 表达式注入
def vulnerable_where_expression(collection, expr)
  collection.find({ "$where" => expr })
end

# 正样本 - find_one $where 注入
def vulnerable_where_find_one(collection, expr)
  collection.find_one({ "$where" => expr })
end

# 正样本 - count_documents $where 注入
def vulnerable_where_count(collection, expr)
  collection.count_documents({ "$where" => expr })
end

# 正样本 - 动态构造 filter（hash 赋值）
def vulnerable_dynamic_filter_hash(collection, params)
  filter = {}
  filter[params[:field]] = params[:value]
  collection.find(filter)
end

# 正样本 - 直接使用 params 作为 filter
def vulnerable_direct_params_filter(collection, params)
  collection.find(params)
end

# 正样本 - aggregate pipeline 注入
def vulnerable_aggregate(collection, pipeline)
  collection.aggregate(pipeline)
end

# 正样本 - 字符串拼接 $where
def vulnerable_where_concat(collection, username)
  where_expr = "this.username == '#{username}'"
  collection.find({ "$where" => where_expr })
end

# 正样本 - Mongoid where 注入
def vulnerable_mongoid_where(params)
  User.where(params[:filter])
end
