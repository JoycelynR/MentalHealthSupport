<?php include 'header.php'; ?>

<div class="container">
    <h2>Login</h2>

    <?php if(isset($error)) echo "<p class='error'>$error</p>"; ?>

    <form action="../auth/login_process.php" method="POST">
        <input type="text" name="login" placeholder="Email or Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>

    <!-- Toggle button for registration -->
    <button class="toggle-btn" onclick="location.href='register.php'">Register</button>
</div>

<?php include 'footer.php'; ?>
