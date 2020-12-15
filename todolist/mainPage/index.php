<!DOCTYPE html>
<html lang="ru">
<head>
    <link rel="stylesheet" href="main.css">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Main page</title>
</head>
<body>
    <header class="header">
        <div class="header__inner">
            <div class="header__title"><?php 
            if ($_COOKIE['user'] == ''):
             ?>
                <a href="/todolist/registration/reg.html"><button class="header__button">Зарегистрироваться</button></a>
                <span class="title">Вы ещё не авторизованы</span>
                <a href="/todolist/login/login.html"><button class="header__button">Авторизоваться</button></a>
            </div>
            <?php else: ?>
            <div class="user--center">
                <span class="title">Здравствуйте <?=$_COOKIE['user']?></span>
                <a href="exit.php"><button class="header__button">Выйти</button></a>
            </div>
            <?php endif; ?>
        </div>
    </header>
    <section class="data-table">
        <div class="container">
            <div class="data-table__inner">
                <table>
                    <tr>
                        <th class="header-table">№</th>
                        <th class="header-table">Фамилия</th>
                        <th class="header-table">Имя</th>
                        <th class="header-table">Отчество</th>
                        <th class="header-table">Номер телефона</th>
                        <th class="header-table">Должность</th>
                        <th class="header-table">Отделение</th>
                    </tr>
                    <?php
                    include "db.php";

                    $request = mysqli_query($induction, "SELECT id_employee, mname, fname, lname, phone_number, position, department_name FROM `employee`, `department` where `employee`.fk_id_department_code = `department`.id_department_code");
                    while ($result = mysqli_fetch_assoc($request))
                    { 
                        ?>
                    <tr>
                        <td class="body-table"><?php echo $result['id_employee'] ?></td>
                        <td class="body-table"><?php echo $result['mname'] ?></td>
                        <td class="body-table"><?php echo $result['fname'] ?></td>
                        <td class="body-table"><?php echo $result['lname'] ?></td>
                        <td class="body-table"><?php echo $result['phone_number'] ?></td>
                        <td class="body-table"><?php echo $result['position'] ?></td>
                        <td class="body-table"><?php echo $result['department_name'] ?></td>
                    </tr>
                    <?php 
                    }
                     ?>
                </table>
            </div>
        </div>
    </section>
    <section class="todolist">
        <div class="container">
            <div class="todolist__inner">


                <div class="searching-place">
                    <div class="searching-place__item">
                        <form action="select.php" method="POST">
                            <select name="department" id="">
                            <?php
                            include "db.php";

                            $requestDepartment = mysqli_query($induction, "SELECT id_department_code, department_name FROM `department`");
                            while ($result = mysqli_fetch_assoc($requestDepartment))
                            { 
                            ?>
                                <option value="<?php echo $result['id_department_code'] ?>"><?php echo $result['department_name'] ?></option>
                            <?php 
                            }
                            ?>
                            </select>
                            <input type="submit" value="Найти" class="searching-place__button">
                        </form>
                    </div>
                </div>

                
            </div>
        </div>
    </section>   
</body>
</html>