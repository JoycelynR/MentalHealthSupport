-- goes on very top of every dashboard that needs protection
-- change title to match dashboard ( change doctor)

<?php
session_start();
if (!isset($_SESSION['role']) || $_SESSION['role'] !== 'doctor') {
    header("Location: login.php");
    exit;
}
?>
