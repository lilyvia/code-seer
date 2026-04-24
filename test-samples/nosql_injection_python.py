from pymongo import MongoClient
from flask import request

def vulnerable_where_expression(collection, expr):
    # 正样本 - $where 表达式注入
    collection.find({"$where": expr})

def vulnerable_where_find_one(collection, expr):
    # 正样本 - find_one $where 注入
    collection.find_one({"$where": expr})

def vulnerable_where_count(collection, expr):
    # 正样本 - count_documents $where 注入
    collection.count_documents({"$where": expr})

def vulnerable_dynamic_filter_dict(collection):
    # 正样本 - 动态构造 filter（字典赋值）
    filter = {}
    filter[request.args.get("field")] = request.args.get("value")
    collection.find(filter)

def vulnerable_dynamic_filter_direct(collection):
    # 正样本 - 直接使用 request.json 作为 filter
    collection.find(request.json)

def vulnerable_aggregate(collection):
    # 正样本 - aggregate pipeline 注入
    pipeline = [{"$match": request.json.get("filter")}]
    collection.aggregate(pipeline)

def vulnerable_where_concat(collection, username):
    # 正样本 - 字符串拼接 $where
    where_expr = f"this.username == '{username}'"
    collection.find({"$where": where_expr})

def vulnerable_json_parse(collection):
    # 正样本 - 从 JSON 字符串解析 filter
    import json
    filter_str = request.args.get("filter")
    filter_obj = json.loads(filter_str)
    collection.find(filter_obj)

def false_negative_expansion_nosql_python(collection, request):
    collection.aggregate([{ '$match': request.json }])
    collection.find(request.args)

def false_negative_additional_nosql_python(redis, es, table, Document, userCmd, userQuery, userExpr, userFilter):
    redis.execute_command(userCmd)
    es.search(body=userQuery)
    table.query(KeyConditionExpression=userExpr)
    Document.find(userFilter)
