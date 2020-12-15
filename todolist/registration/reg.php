<?php 
 $login = filter_var(trim($_POST['login']), FILTER_SANITIZE_STRING);
 $pass = filter_var(trim($_POST['pass']), FILTER_SANITIZE_STRING);
 $validPass = filter_var(trim($_POST['validPass']), FILTER_SANITIZE_STRING);
 $fname = filter_var(trim($_POST['fname']), FILTER_SANITIZE_STRING);
 $mname = filter_var(trim($_POST['mname']), FILTER_SANITIZE_STRING);
 $lname = filter_var(trim($_POST['lname']), FILTER_SANITIZE_STRING);
 $number = filter_var(trim($_POST['number']), FILTER_SANITIZE_STRING);
 $department = filter_var(trim($_POST['department']), FILTER_SANITIZE_STRING);

 if ($pass != $validPass) {
   echo "<script>alert(\"Пароли не совпадают.\");</script>";
   header('Refresh:0; url=/todolist/registration/reg.html');
   exit();
 }

 $mysql = new mysqli('localhost:3306', 'root', 'root', 'laba4');
 $mysql->query("INSERT INTO `employee` (`login`, `password`, `mname`, `fname`, `lname`, `phone_number`, `fk_id_department_code`) VALUES('$login', '$pass', '$mname', '$fname', '$lname', '$number', '$department')"); 

 echo $mysql->error;

 $mysql->close(); 

 if ($mysql == false)
 {
    echo "Ошибка подключения";
 }

 header('Location: /todolist/login/login.html');

 ?>