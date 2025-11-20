<?php
// Database connection parameters
$servername = "localhost";      // MySQL server
$username   = "root";           // default XAMPP username
$password   = "";               // default XAMPP password (empty)
$dbname     = "mentalhealth_app"; // your database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
// echo "Connected successfully"; // optional for testing
?>
