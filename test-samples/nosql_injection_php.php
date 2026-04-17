<?php
// 正样本 - $where 表达式注入
function vulnerableWhereExpression($collection, $expr) {
    $collection->find(['$where' => $expr]);
}

// 正样本 - findOne $where 注入
function vulnerableWhereFindOne($collection, $expr) {
    $collection->findOne(['$where' => $expr]);
}

// 正样本 - countDocuments $where 注入
function vulnerableWhereCount($collection, $expr) {
    $collection->countDocuments(['$where' => $expr]);
}

// 正样本 - 动态构造 filter（数组赋值）
function vulnerableDynamicFilterArray($collection) {
    $filter = [];
    $filter[$_GET['field']] = $_GET['value'];
    $collection->find($filter);
}

// 正样本 - 直接使用 $_POST 作为 filter
function vulnerableDirectPostFilter($collection) {
    $collection->find($_POST);
}

// 正样本 - aggregate pipeline 注入
function vulnerableAggregate($collection, $pipeline) {
    $pipelineObj = json_decode($pipeline, true);
    $collection->aggregate($pipelineObj);
}

// 正样本 - 字符串拼接 $where
function vulnerableWhereConcat($collection, $username) {
    $whereExpr = "this.username == '" . $username . "'";
    $collection->find(['$where' => $whereExpr]);
}

// 正样本 - PHP 数组注入（URL: ?username[$ne]=1）
function vulnerableArrayInjection($collection) {
    $collection->find([
        'username' => $_GET['username'],
        'password' => $_GET['password']
    ]);
}
