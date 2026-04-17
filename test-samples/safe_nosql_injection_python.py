from pymongo import MongoClient
from flask import request

def safe_fixed_filter(collection, email):
    # 负样本 - 使用固定字段和类型转换
    collection.find({"email": str(email)})

def safe_allowlisted_field(collection, field, value):
    # 负样本 - 使用允许名单验证字段名
    allowed_fields = {"email", "status", "role"}
    if field not in allowed_fields:
        raise ValueError("invalid field")
    collection.find({field: str(value)})

def safe_typed_query(collection, username, password):
    # 负样本 - 显式构造查询（不使用动态字段）
    collection.find({
        "username": str(username),
        "password": str(password)
    })

def safe_count_documents(collection, status):
    # 负样本 - countDocuments 使用固定字段
    collection.count_documents({"status": str(status)})

def safe_aggregate(collection):
    # 负样本 - aggregate 使用硬编码 pipeline
    pipeline = [
        {"$match": {"status": "active"}},
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ]
    collection.aggregate(pipeline)

def safe_static_dict(collection, user_id):
    # 负样本 - 静态字典构造
    query = {"user_id": str(user_id)}
    collection.find(query)

def safe_schema_validation(collection, data):
    # 负样本 - 使用 schema 验证输入
    from pydantic import BaseModel, constr
    
    class UserQuery(BaseModel):
        username: constr(min_length=1, max_length=50)
        email: constr(min_length=1, max_length=100)
    
    query = UserQuery(**data)
    collection.find({"username": query.username})
