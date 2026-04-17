<?php
// 负样本 - 使用固定字段和类型转换
function safeFixedFilter($collection, $email) {
    $collection->find(['email' => (string)$email]);
}

// 负样本 - 使用允许名单验证字段名
function safeAllowlistedField($collection, $field, $value) {
    $allowedFields = ['email', 'status', 'role'];
    if (!in_array($field, $allowedFields)) {
        throw new Exception('invalid field');
    }
    $collection->find([$field => (string)$value]);
}

// 负样本 - 显式构造查询（不使用动态字段）
function safeTypedQuery($collection, $username, $password) {
    $collection->find([
        'username' => (string)$username,
        'password' => (string)$password
    ]);
}

// 负样本 - countDocuments 使用固定字段
function safeCountDocuments($collection, $status) {
    $collection->countDocuments(['status' => (string)$status]);
}

// 负样本 - aggregate 使用硬编码 pipeline
function safeAggregate($collection) {
    $pipeline = [
        ['$match' => ['status' => 'active']],
        ['$group' => ['_id' => '$category', 'count' => ['$sum' => 1]]]
    ];
    $collection->aggregate($pipeline);
}

// 负样本 - 静态数组构造
function safeStaticArray($collection, $userId) {
    $query = ['user_id' => (string)$userId];
    $collection->find($query);
}

// 负样本 - 数组注入防护（检测数组输入）
function safeArrayInjectionProtection($collection) {
    $username = is_array($_GET['username']) ? '' : (string)$_GET['username'];
    $password = is_array($_GET['password']) ? '' : (string)$_GET['password'];
    $collection->find([
        'username' => $username,
        'password' => $password
    ]);
}
