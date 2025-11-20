<?php
session_start();
require('../includes/db.php');


$login = $_POST['login'];
$password = $_POST['password'];

$stmt = $conn->prepare("SELECT * FROM users WHERE email = ? OR username = ?");
$stmt->bind_param("ss", $login, $login);
$stmt->execute();

$result = $stmt->get_result();
$user = $result->fetch_assoc();

if (!$user || !password_verify($password, $user['password'])) {
    die("Invalid credentials.");
}

session_regenerate_id(true);

$_SESSION['user_id'] = $user['id'];
$_SESSION['role'] = $user['role'];

switch ($user['role']) {
    case "user":
        header("Location: user_dashboard.php");
        break;
    case "doctor":
        header("Location: doctor_dashboard.php");
        break;
    case "pharmacy":
        header("Location: pharmacy_dashboard.php");
        break;
    case "admin":
        header("Location: admin_dashboard.php");
        break;
}
?>
