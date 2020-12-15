import tkinter as tk # подключение библиотеки для работы с графическим интерфесом
from tkinter import ttk # подключение библиотеки для работы с графическим интерфесом
from tkinter import * # подключение библиотеки для работы с графическим интерфесом
import pymysql # подключение библиотеки для работы с базой данных
from tkinter import messagebox


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db # переменные из других классов
        self.view_records() # вызов функции при старте приложения

    def init_main(self):

        header_frame = Frame(root, bg="#CD853F", width=3600,
        height=50, borderwidth=10) # создание рабочей области для вывода информации из базы данных
        header_frame.place(rely=.15, anchor="c", bordermode=OUTSIDE) # её размещение

        center_frame = Frame(root) # создание рабочей области для вывода информации из базы данных
        center_frame.place(relx=.5, rely=.54, anchor="c", bordermode=OUTSIDE) # её размещение

        self.tree = ttk.Treeview(center_frame, columns=(
        'id_employee', 'login', 'password', 'mname', 'fname', 'lname', 'phone_number', 'position', 'department_code', 'department_name'), height=25, show='headings') # таблица иметирующая таблицу в базе данных
        self.tree.column('id_employee', width=30, anchor=tk.CENTER) # создание столбцов
        self.tree.column('login', width=100, anchor=tk.CENTER)
        self.tree.column('password', width=100, anchor=tk.CENTER)
        self.tree.column('mname', width=200, anchor=tk.CENTER)
        self.tree.column('fname', width=200, anchor=tk.CENTER)
        self.tree.column('lname', width=200, anchor=tk.CENTER)
        self.tree.column('phone_number', width=200, anchor=tk.CENTER)
        self.tree.column('position', width=200, anchor=tk.CENTER)
        self.tree.column('department_code', width=100, anchor=tk.CENTER)
        self.tree.column('department_name', width=250, anchor=tk.CENTER)

        self.tree.heading('id_employee', text='№')
        self.tree.heading('login', text='Логин')
        self.tree.heading('password', text='Пароль')
        self.tree.heading('mname', text='Фамилия')
        self.tree.heading('fname', text='Имя')
        self.tree.heading('lname', text='Отчество')
        self.tree.heading('phone_number', text='Номер телефона')
        self.tree.heading('position', text='Должность')
        self.tree.heading('department_code', text='Код отделения')
        self.tree.heading('department_name', text='Название отделения')
        self.tree.pack() # размещение таблицы

        btn_new_category = Button(root, text='Добавить работника', bg='#FFE4C4', compound=TOP, fg='black', font=('Times new roman', 15), command=Add) # создание кнопоки для добавления
        btn_new_category.place(x=10, y=100) # размещение кнопки для добавления

        btn_delete = Button(root, text='Удалить', bg='#FFE4C4', compound=TOP,
        fg='black', font=('Times new roman', 15), command=Delete) # создание кнопки для удаления
        btn_delete.place(x=207, y=100) # размещение кнопки для удаления

        btn_update = Button(root, text='Добавить должность', bg='#FFE4C4', compound=TOP, fg='black', font=('Times new roman', 15), command=Update)
        btn_update.place(x=301, y=100)

        btn_todo_list = Button(root, text='Вывести с/з', bg='#FFE4C4', compound=TOP, fg='black', font=('Times new roman', 15), command=Todo_list)
        btn_todo_list.place(x=604, y=100)

        btn_refresh = Button(root, text='Обновить', bg='#FFE4C4', fg='black', font=('Times new roman', 15))
        btn_refresh.place(x=500, y=100)
        btn_refresh.bind('<Button-1>', lambda event: self.view_records())

        btn_without_position = Button(root, text='Вывести пользователей без должности', bg='#FFE4C4', fg='black', font=('Times new roman', 15))
        btn_without_position.place(x=1242, y=100)
        btn_without_position.bind('<Button-1>', lambda event: self.view_without_position())

    def records(self, login, password, mname, fname, lname, phone_number, position, department_code): # функция принимающая входными параметрами переменные из других классов
        self.db.insert_data(login, password, mname, fname, lname, phone_number, position, department_code) # вызов функции из класса db по вводу данных в sql таблицу
        self.view_records() # вызов функции

    def records_todo_list(self, title, description, department_code1, process): # функция принимающая входными параметрами переменные из других классов
        self.db.insert_data_todo_list(title, description, department_code1, process) # вызов функции из класса db по вводу данных в sql таблицу

    def view_records(self): # функция по заполнению
        self.db.conn.commit()
        self.db.c.execute('''SELECT id_employee, login, password, mname, fname, lname, phone_number, position, fk_id_department_code, department_name FROM employee, department where employee.fk_id_department_code = department.id_department_code''') # вызов всех столбцов базы данных
        [self.tree.delete(i) for i in self.tree.get_children()] # цикл for для заполнения имитирующей таблицы
        [self.tree.insert('', 'end', values=row)
        for row in self.db.c.fetchall()] # длинна базы данных

    def view_without_position(self):
        self.db.conn.commit()
        self.db.c.execute('''SELECT id_employee, login, password, mname, fname, lname, phone_number, position, fk_id_department_code, department_name FROM employee, department where employee.fk_id_department_code = department.id_department_code order by position, mname, fname, lname''') # вызов всех столбцов базы данных
        [self.tree.delete(i) for i in self.tree.get_children()] 
        [self.tree.insert('', 'end', values=row)
        for row in self.db.c.fetchall()] 

    def remove(self): # функция для кнопки удаления
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM employee WHERE id_employee = %s''',
            (self.tree.set(selection_item, '#1'),)) # удаление из базы данных id совпадающим с выбраным id причём цикл for позволяет удалять не только один выпранный элемент за раз
            self.db.conn.commit() # сохранение базы данных
        self.view_records()

    def update_position(self, pos_name): # функция для кнопки удаления
        for selection_item in self.tree.selection():
            self.db.c.execute('''UPDATE employee SET position = '{}' WHERE id_employee = %s'''.format(pos_name),
            (self.tree.set(selection_item, '#1'),)) # удаление из базы данных id совпадающим с выбраным id причём цикл for позволяет удалять не только один выпранный элемент за раз
            self.db.conn.commit() # сохранение базы данных
        self.view_records()

    def update_process(self, process1): # функция для кнопки удаления
        print ('получил')
        for selection_item in self.tree.selection():
            self.db.c.execute('''UPDATE todo_list SET process = '{}' WHERE id_todo_list = %s'''.format(process1),
            (self.tree.set(selection_item, '#1'),)) # удаление из базы данных id совпадающим с выбраным id причём цикл for позволяет удалять не только один выпранный элемент за раз
            self.db.conn.commit() # сохранение базы данных


class Add(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_add()
        self.view = app

    def init_add(self):

        self.title('Добавить нового сотрутдника') # создание дополнительного окна которое будет вызываться при вызове класса add
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 200
        height = height - 150
        self.geometry('400x300+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        label_login = tk.Label(
        self, bg='#FFE4C4', text='Логин', font=('Times new roman', 15)) # создание лэйбла с текстом
        label_login.place(x=50, y=20) # размещение на окне лэйбла с текстом
        
        label_password = tk.Label(
        self, bg='#FFE4C4', text='Пароль', font=('Times new roman', 15))
        label_password.place(x=50, y=50)

        label_mname = tk.Label(
        self, bg='#FFE4C4', text='Фамилия', font=('Times new roman', 15))
        label_mname.place(x=50, y=80)

        label_fname = tk.Label(
        self, bg='#FFE4C4', text='Имя', font=('Times new roman', 15))
        label_fname.place(x=50, y=110)

        label_lname = tk.Label(
        self, bg='#FFE4C4', text='Отчество', font=('Times new roman', 15))
        label_lname.place(x=50, y=140)

        label_phone_number = tk.Label(
        self, bg='#FFE4C4', text='Номер телефона', font=('Times new roman', 15))
        label_phone_number.place(x=50, y=170)

        label_position = tk.Label(
        self, bg='#FFE4C4', text='Должность', font=('Times new roman', 15))
        label_position.place(x=50, y=200)

        label_department_code = tk.Label(
        self, bg='#FFE4C4', text='Код отделения', font=('Times new roman', 15))
        label_department_code.place(x=50, y=230)

        self.entry_login = ttk.Entry(self) # создание поля для ввода
        self.entry_login.place(x=250, y=20) # размещение поля для ввода

        self.entry_password = ttk.Entry(self)
        self.entry_password.place(x=250, y=50)

        self.entry_mname = ttk.Entry(self)
        self.entry_mname.place(x=250, y=80)

        self.entry_fname = ttk.Entry(self)
        self.entry_fname.place(x=250, y=110)

        self.entry_lname = ttk.Entry(self)
        self.entry_lname.place(x=250, y=140)

        self.entry_phone_number = ttk.Entry(self)
        self.entry_phone_number.place(x=250, y=170)

        self.entry_position = ttk.Entry(self)
        self.entry_position.place(x=250, y=200)

        self.entry_department_code = ttk.Entry(self)
        self.entry_department_code.place(x=250, y=235)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=260)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=260)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_login.get(),
        self.entry_password.get(), self.entry_mname.get(), self.entry_fname.get(), self.entry_lname.get(), self.entry_phone_number.get(), self.entry_position.get(), self.entry_department_code.get()))# бинд кнопки на срабатывание при нажатии на неё левой кнопкой мыши

        self.grab_set() # метод для выделения этого окна при попытки уйти на другое
        self.focus_set() # метод который не позволяет изменять размеры окна



class Delete(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_delete()
        self.view = app

    def init_delete(self):

        self.title('Подтверждение')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 150
        height = height - 100
        self.geometry('300x200+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        lbl_info = Label(self, font=('Times new roman', 23),
        bg="#FFE4C4", text='Вы уверены?')
        lbl_info.place(x=60, y=50)

        btn_yes = Button(self, width=7, font=(
        'Times new roman', 15), text='Да', command=self.yes)
        btn_no = Button(self, width=7, font=(
        'Times new roman', 15), text='Нет', command=self.no)

        btn_yes.place(x=60, y=110)
        btn_no.place(x=150, y=110)

        self.grab_set()
        self.focus_set()

    def yes(self): # функция срабатывающая при нажатии на да
        self.view.remove()
        self.destroy()

    def no(self): # функция срабатывающая при нажатии на нет
        self.destroy()

class Todo_list(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_todo_list()
        self.view = app
        self.db = db
        self.view_todo_list()

    def init_todo_list(self):
        self.title('Список задач')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 500
        height = height - 400
        self.geometry('1000x800+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        header_frame = Frame(self, bg="#CD853F", width=3600,
        height=50, borderwidth=10) # создание рабочей области для вывода информации из базы данных
        header_frame.place(rely=.15, anchor="c", bordermode=OUTSIDE) # её размещение

        center_frame = Frame(self) # создание рабочей области для вывода информации из базы данных
        center_frame.place(relx=.5, rely=.54, anchor="c", bordermode=OUTSIDE) # её размещение

        self.tree = ttk.Treeview(center_frame, columns=(
        'id_todo_list', 'title', 'description', 'fk_id_department_name', 'process'), height=25, show='headings') # таблица иметирующая таблицу в базе данных
        self.tree.column('id_todo_list', width=30, anchor=tk.CENTER) # создание столбцов
        self.tree.column('title', width=80, anchor=tk.CENTER)
        self.tree.column('description', width=300, anchor=tk.CENTER)
        self.tree.column('fk_id_department_name', width=200, anchor=tk.CENTER)
        self.tree.column('process', width=200, anchor=tk.CENTER)

        self.tree.heading('id_todo_list', text='№')
        self.tree.heading('title', text='Заголовок')
        self.tree.heading('description', text='Описание')
        self.tree.heading('fk_id_department_name', text='Отделение')
        self.tree.heading('process', text='Процесс выполнения')
        self.tree.pack() # размещение таблицы

        btn_add_todo_list = Button(self, text='Добавить список задач', bg='#FFE4C4', compound=TOP, fg='black', font=('Times new roman', 15), command=Add_todo_list)
        btn_add_todo_list.place(x=126, y=100)

        btn_update_todo_list = Button(self, text='Обновить список задач', bg='#FFE4C4', compound=TOP, fg='black', font=('Times new roman', 15), command=Update_todo_list)
        btn_update_todo_list.place(x=344, y=100)

        btn_refresh1 = Button(self, text='Обновить', bg='#FFE4C4', fg='black', font=('Times new roman', 15))
        btn_refresh1.place(x=563, y=100)
        btn_refresh1.bind('<Button-1>', lambda event: self.view_todo_list())



    def view_todo_list(self): # функция по заполнению
        self.db.conn.commit()
        self.db.c.execute('''SELECT id_todo_list, title, description, department_name, process FROM todo_list, department where todo_list.fk_id_department_code = department.id_department_code''') # вызов всех столбцов базы данных
        [self.tree.delete(i) for i in self.tree.get_children()] # цикл for для заполнения имитирующей таблицы
        [self.tree.insert('', 'end', values=row)
        for row in self.db.c.fetchall()] # длинна базы данных

class Add_todo_list(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_add_todo_list()
        self.view = app
        self.db = db

    def init_add_todo_list(self):

        self.title('Добавить новую задачу') # создание дополнительного окна которое будет вызываться при вызове класса add
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 200
        height = height - 100
        self.geometry('400x200+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        label_title = tk.Label(
        self, bg='#FFE4C4', text='Заголовок', font=('Times new roman', 15)) # создание лэйбла с текстом
        label_title.place(x=50, y=20) # размещение на окне лэйбла с текстом
        
        label_description = tk.Label(
        self, bg='#FFE4C4', text='Описание', font=('Times new roman', 15))
        label_description.place(x=50, y=50)

        label_departmant_code1 = tk.Label(
        self, bg='#FFE4C4', text='Код отделение', font=('Times new roman', 15))
        label_departmant_code1.place(x=50, y=80)

        label_process = tk.Label(
        self, bg='#FFE4C4', text='Процесс', font=('Times new roman', 15))
        label_process.place(x=50, y=110)

        self.entry_title = ttk.Entry(self) # создание поля для ввода
        self.entry_title.place(x=250, y=20) # размещение поля для ввода

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=250, y=50)

        self.entry_department_code1 = ttk.Entry(self)
        self.entry_department_code1.place(x=250, y=80)

        self.entry_process = ttk.Entry(self)
        self.entry_process.place(x=250, y=110)

        btn_cancel1 = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel1.place(x=300, y=160)

        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x=220, y=160)
        self.btn_add.bind('<Button-1>', lambda event: self.view.records_todo_list(self.entry_title.get(),
        self.entry_description.get(), self.entry_department_code1.get(), self.entry_process.get()))# бинд кнопки на срабатывание при нажатии на неё левой кнопкой мыши

        self.grab_set() # метод для выделения этого окна при попытки уйти на другое
        self.focus_set() # метод который не позволяет изменять размеры окна



class Update(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_update()
        self.view = app

    def init_update(self):

        self.title('Добавить должность')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 250
        height = height - 100
        self.geometry('500x200+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        label_pos_name = tk.Label(
        self, bg='#FFE4C4', text='Новая должность', font=('Times new roman', 15))
        label_pos_name.place(x=180, y=20)

        self.entry_pos_name = ttk.Entry(self, width=75)
        self.entry_pos_name.place(x=20, y=60)

        btn_yes = Button(self, width=7, font=(
        'Times new roman', 15), text='Добавить', command=self.button_add)
        btn_no = Button(self, width=7, font=(
        'Times new roman', 15), text='Закрыть', command=self.button_close)

        btn_yes.place(x=170, y=140)
        btn_no.place(x=260, y=140)

        self.grab_set()
        self.focus_set()

    def button_add(self):
        self.view.update_position(self.entry_pos_name.get())
        self.destroy()

    def button_close(self):
        self.destroy()

class Update_todo_list(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_update_todo_list()
        self.view = app

    def init_update_todo_list(self):

        self.title('Обновить список задач')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 250
        height = height - 100
        self.geometry('500x200+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        label_pos_name = tk.Label(
        self, bg='#FFE4C4', text='Новый процесс работы', font=('Times new roman', 15))
        label_pos_name.place(x=180, y=20)

        self.entry_process1 = ttk.Entry(self, width=75)
        self.entry_process1.place(x=20, y=60)

        btn_yes = Button(self, width=7, font=(
        'Times new roman', 15), text='Добавить', command=self.button_add)
        btn_no = Button(self, width=7, font=(
        'Times new roman', 15), text='Закрыть', command=self.button_close)

        btn_yes.place(x=170, y=140)
        btn_no.place(x=260, y=140)

        self.grab_set()
        self.focus_set()

    def button_add(self):
        self.view.update_process(self.entry_process1.get())
        print ("Отправил")
        self.destroy()

    def button_close(self):
        self.destroy()


class DB:
    def __init__(self):
        try:
            self.conn = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="laba4") #скрипт для подключения к базе данных
            self.c = self.conn.cursor()
        except:
            messagebox.showinfo("Ошибка", "Недействительное подключение к базе данных")
            

    def insert_data(self, login, password, mname, fname, lname, phone_number, position, department_code): # функция для добавления данных в базу данных
        self.c.execute('''INSERT INTO employee(id_employee, login, password, mname, fname, lname, phone_number, position, fk_id_department_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
        (None, login, password, mname, fname, lname, phone_number, position, department_code))
        self.conn.commit()

    def insert_data_todo_list(self, title, description, department_code1, process): # функция для добавления данных в базу данных
        self.c.execute('''INSERT INTO todo_list(id_todo_list, title, description, fk_id_department_code, process) VALUES (%s, %s, %s, %s, %s)''',
        (None, title, description, department_code1, process))
        self.conn.commit()


if __name__ == "__main__":
    root = Tk()
    db = DB()
    app = Main(root)
    app.place() # создание приложения
    root.title('Приложение для администратора') # Название созданого приложения
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    width = width // 2
    height = height // 2
    width = width - 800
    height = height - 400
    root.geometry('1600x800+{}+{}'.format(width, height)) # создание адаптивной ширины и высоты для окна
    root.config(bg="#FFE4C4") # задний фон для приложения
    root.resizable(False, False)
    root.mainloop() # циклирование приложения