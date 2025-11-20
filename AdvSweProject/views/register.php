<?php include 'header.php'; ?>

<div class="container">
    <h2>Register</h2>

    <?php if(isset($error)) echo "<p class='error'>$error</p>"; ?>

    <form action="../auth/register_process.php" method="POST">
    <input type="text" name="fullname" placeholder="Full Name" required>
    <input type="text" name="username" placeholder="Username" required>
    <input type="email" name="email" placeholder="Email" required>
    <input type="text" name="contact" placeholder="Contact Number (Optional)">
    
    <!-- Passwords -->
    <input type="password" name="password" placeholder="Password" required>
    <input type="password" name="confirm_password" placeholder="Confirm Password" required>

    <!-- Gender -->
    <select name="gender">
        <option value="">Select Gender (optional)</option>
        <option value="Male">Male</option>
        <option value="Female">Female</option>
        <option value="Other">Other</option>
    </select>

    <!-- Birth Date -->
    <input type="date" name="birth_date" placeholder="Birth Date (optional)">

    <!-- Role -->
    <select name="role" required>
        <option value="">Select Role</option>
        <option value="user">User</option>
        <option value="doctor">Doctor</option>
        <option value="pharmacy">Pharmacy</option>
        <option value="admin">Admin</option>
    </select>

    <button type="submit">Register</button>
</form>

<!-- Toggle button for login -->
<button class="toggle-btn" onclick="location.href='login.php'">Login</button>
</div>

<?php include 'footer.php'; ?>
