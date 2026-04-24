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

// Safe: Use Laravel bindings instead of SQL concatenation
function getUserWithBindings($id) {
    return DB::select('SELECT * FROM users WHERE id = ?', [$id]);
}

// Safe: Use Doctrine named parameters instead of DQL concatenation
function getUserWithDoctrine($em, $name) {
    $query = $em->createQuery('SELECT u FROM User u WHERE u.name = :name');
    $query->setParameter('name', $name);
    return $query->getResult();
}
