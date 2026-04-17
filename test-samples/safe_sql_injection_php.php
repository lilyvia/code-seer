<?php

// Safe: Use PDO prepared statements
function getUser($pdo, $id) {
    $stmt = $pdo->prepare('SELECT * FROM users WHERE id = :id');
    $stmt->execute(['id' => $id]);
    return $stmt->fetch();
}

// Safe: Use mysqli prepared statements
function getUserMysqli($mysqli, $id) {
    $stmt = $mysqli->prepare('SELECT * FROM users WHERE id = ?');
    $stmt->bind_param('i', $id);
    $stmt->execute();
    return $stmt->get_result()->fetch_assoc();
}
