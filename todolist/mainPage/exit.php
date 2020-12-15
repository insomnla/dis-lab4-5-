<?php 
setcookie('user', $user['Fname'], time() - 3600, "/");

header('Location: /todolist/mainPage/index.php');
?>