<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="main.css"> 
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo List</title>
</head>
<body>
    <div class="table-todolist">
        <div class="todolist-header">
            Список задач
        </div>
        <?php  
        $department = filter_var(trim($_POST['department']), FILTER_SANITIZE_STRING);

        $mysql = new mysqli('localhost:3306', 'root', 'root', 'laba4');
        $result = $mysql->query("SELECT * FROM `todo_list` where fk_id_department_code = '$department'");
        
        echo $mysql->error;

        while ($request = mysqli_fetch_assoc($result))
        { 
            $i++;
        ?>
        <div class="todolist__item">
            <div class="table-title">
            <?php echo $i ?>. <?php echo $request['Title'] ?>
            </div>
            <div class="table-discription">
            <?php echo $request['Description'] ?>
            </div>
        </div>
        <?php
        }
        ?>
    </div>
</body>
</html>