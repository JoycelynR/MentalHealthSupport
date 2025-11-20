<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors', 1);

require('../includes/db.php'); // Path to your db.php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    // Get and trim form inputs
    $username   = trim($_POST['username']);
    $fullname   = trim($_POST['fullname']);
    $email      = trim($_POST['email']);
    $contact    = trim($_POST['contact']);        // optional
    $password   = $_POST['password'];
    $confirm    = $_POST['confirm_password'];
    $role       = $_POST['role'];
    $gender     = !empty($_POST['gender']) ? $_POST['gender'] : NULL;         // optional
    $birth_date = !empty($_POST['birth_date']) ? $_POST['birth_date'] : NULL; // optional

    // Basic required fields validation
    if (empty($username) || empty($fullname) || empty($email) || empty($password) || empty($confirm) || empty($role)) {
        $error = "Please fill in all required fields.";
        header("Location: ../views/register.php?error=" . urlencode($error));
        exit;
    }

    // Optional contact validation
    if (!empty($contact)) {
        $contact_clean = str_replace([' ', '-', '(', ')'], '', $contact);
        if (!preg_match('/^[0-9]{10,15}$/', $contact_clean)) {
            $error = "Invalid contact number.";
            header("Location: ../views/register.php?error=" . urlencode($error));
            exit;
        }
    } else {
        $contact_clean = NULL;
    }

    // Check passwords match
    if ($password !== $confirm) {
        $error = "Passwords do not match.";
        header("Location: ../views/register.php?error=" . urlencode($error));
        exit;
    }

    // Hash password
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    // Check if username or email already exists
    $stmt = $conn->prepare("SELECT id FROM users WHERE username = ? OR email = ?");
    $stmt->bind_param("ss", $username, $email);
    $stmt->execute();
    $stmt->store_result();
    if ($stmt->num_rows > 0) {
        $error = "Username or email already exists.";
        header("Location: ../views/register.php?error=" . urlencode($error));
        exit;
    }
    $stmt->close();

    // Insert new user
    $stmt = $conn->prepare("INSERT INTO users (username, fullname, email, contact, password, role, gender, birth_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("ssssssss", $username, $fullname, $email, $contact_clean, $hashed_password, $role, $gender, $birth_date);

    if ($stmt->execute()) {
        $_SESSION['success'] = "Registration successful! You can now log in.";
        header("Location: ../views/login.php");
        exit;
    } else {
        $error = "Error registering user: " . $stmt->error;
        header("Location: ../views/register.php?error=" . urlencode($error));
        exit;
    }

    $stmt->close();
    $conn->close();

} else {
    // Redirect if accessed directly
    header("Location: ../views/register.php");
    exit;
}
?>
