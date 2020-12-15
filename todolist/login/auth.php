<?php


$login = filter_var(trim($_POST['login']), FILTER_SANITIZE_STRING);
$password = filter_var(trim($_POST['password']), FILTER_SANITIZE_STRING);

$mysql = new mysqli('localhost:3306', 'root', 'root', 'laba4');
$result = $mysql->query("SELECT * FROM `employee` WHERE `login` = '$login' AND `password` = '$password'");

$user = $result->fetch_assoc();

if (count($user) == 0) {
    echo "<script>alert(\"Неверный логин или пароль.\");</script>";
    header('Refresh:0; url=/todolist/login/login.html');
    exit();
}

setcookie('user', $user['Fname'], time() + 3600, "/");

$mysql->close();

header('Location: /todolist/mainPage/index.php');

 ?>