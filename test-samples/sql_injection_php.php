<?php

function vulnerable($db, $conn, $id, $name) {
    $db->query("SELECT * FROM users WHERE id = " . $id);
    mysqli_query($conn, "SELECT * FROM users WHERE id = " . $id);
    $db->query(sprintf("SELECT * FROM users WHERE name = '%s'", $name));
    mysqli_query($conn, sprintf("SELECT * FROM users WHERE name = '%s'", $name));
}
