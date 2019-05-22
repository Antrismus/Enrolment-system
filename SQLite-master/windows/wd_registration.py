"""
Registration in form

Created by Dmytro Kyrychkov
19/05/2019
"""
from tkinter import *
from tkinter import messagebox
import sqlite3
import datetime


def start():
    """Create registration window"""
    # Create window
    root = Toplevel()
    root.title('Реєстрація')
    root.geometry('325x350')
    root.resizable(0, 0)
    root.grab_set()
    root.focus_set()

    # login container
    login = StringVar(root)

    # Create Label and Entry for login
    login_label = Label(root, text='Створіть Логін: ', padx=5, pady=5)
    login_label.place(x=30, y=20)
    login_entry = Entry(root, textvariable=login)
    login_entry.place(x=160, y=25)

    # passwords container
    password = StringVar(root)
    repeat_password = StringVar(root)

    # Create Label and Entry for password
    password_label = Label(root, text='Створіть пароль: ', padx=5, pady=5)
    password_label.place(x=30, y=60)
    password_entry = Entry(root, textvariable=password, show='•')
    password_entry.place(x=160, y=60)

    repeat_password_label = Label(root, text='Повторити пароль: ', padx=5, pady=5)
    repeat_password_label.place(x=30, y=90)
    repeat_password_entry = Entry(root, textvariable=repeat_password, show='•')
    repeat_password_entry.place(x=160, y=90)

    # Name and surname containers
    name = StringVar(root)
    surname = StringVar(root)

    # Create Label and Entry for name and surname
    name_label = Label(root, text='Імя:  ', padx=5, pady=5)
    name_label.place(x=30, y=130)
    name_entry = Entry(root, textvariable=name)
    name_entry.place(x=160, y=130)
    surname_label = Label(root, text='Прізвище: ', padx=5, pady=5)
    surname_label.place(x=30, y=160)
    surname_entry = Entry(root, textvariable=surname)
    surname_entry.place(x=160, y=160)

    # Date of birthday containers
    day = IntVar(root)
    month = StringVar(root)
    year = IntVar(root)

    # Create input for data
    day_label = Label(root, text=' Дата народження:', padx=5, pady=5)
    day_label.place(x=0, y=200, width=315)

    day_options = range(1, 32)
    month_options = [
        'Січень',
        'Лютий',
        'Березень',
        'Квітень',
        'Травень',
        'Червень',
        'Липень',
        'Серпень',
        'Вересень',
        'Жовтень',
        'Листопад',
        'Грудень'
    ]
    year_options = range(datetime.date.today().year - 150, datetime.date.today().year)

    day_input = OptionMenu(root, day, *day_options)
    day_input.place(x=35, y=230, width=50)
    month_input = OptionMenu(root, month, *month_options)
    month_input.place(x=85, y=230, width=100)
    year_input = OptionMenu(root, year, *year_options)
    year_input.place(x=185, y=230, width=100)

    # Telephone number container
    telephone = StringVar(root)

    # Telephone input
    telephone_label = Label(root, text='Телефон: ', padx=5, pady=5)
    telephone_label.place(x=30, y=270)
    telephone_entry = Entry(root, textvariable=telephone)
    telephone_entry.place(x=160, y=270)

    # Buttons
    login_button = Button(root, text=' Підтвердити ',
                          command=lambda: register(login_entry, password, repeat_password,
                                                   name, surname,
                                                   day, month, year,
                                                   telephone, root)
                          )
    login_button.place(x=30, y=310, width=100)
    exit_button = Button(root, text=' Скасувати ', command=root.destroy)
    exit_button.place(x=190, y=310, width=100)
    root.bind('<Return>', lambda event: register(login_entry, password, repeat_password,
                                                 name, surname,
                                                 day, month, year,
                                                 telephone, root)
              )


def check_password(password, repeat_password):
    """Check if password correct"""
    # title for message box
    title = 'Проблема з паролем'

    # password can't be shorter then 3 symbol
    if len(password.get()) < 3:
        messagebox.showinfo(title, 'Пароль замалий')
    # password must be the same as repeat password
    elif password.get() != repeat_password.get():
        messagebox.showinfo(title, 'Пароль не співпадає')
    else:
        return True
    return False


def check_login(login):
    """Check if login correct"""
    # title for message box
    title = 'Проблема з Логіном'
    # login must have more than 3 element
    if len(login.get()) < 3:
        messagebox.showinfo(title, 'Логін замалий')
    else:
        return True
    return False


def is_high_year(year):
    """Check if year is high"""
    if year % 400 == 0:
        return 1
    elif year % 100 == 0:
        return 0
    elif year % 4 == 0:
        return 1
    else:
        return 0


def check_date(day, month, year):
    """Check if date correct"""
    month_options = {
        'Січень': 31,
        'Лютий': 28 + is_high_year(int(year.get())),
        'Березень': 31,
        'Квітень': 30,
        'Травень': 31,
        'Червень': 30,
        'Липень': 31,
        'Серпень': 31,
        'Вересень': 30,
        'Жовтень': 31,
        'Листопад': 30,
        'Грудень': 31
    }

    if month_options[month.get()] >= int(day.get()):
        return True
    messagebox.showinfo('Проблема з датою', 'Не коректнно задано дату')
    return False


def register(login, password, repeat_password, name, surname, day, month, year, telephone, root):
    """Function for registration new user (Add him into a user database)"""
    # Check if login and password are correct
    if not check_login(login) and not check_password(password, repeat_password):
        return 0

    # Check if date unreal
    if not check_date(day, month, year):
        return 0

    try:
        # Connect to the users database
        database = sqlite3.connect('databases\\users.db')
        cursor = database.cursor()

        # Create a new user database if haven't one
        cursor.execute('CREATE TABLE IF NOT EXISTS users(' +
                       'login TEXT PRIMARY KEY,' +
                       'password TEXT,' +
                       'name TEXT,' +
                       'surname TEXT,' +
                       'day TEXT,' +
                       'month TEXT,' +
                       'year TEXT,' +
                       'telephone TEXT,' +
                       'permission TEXT)')
        # Insert a new user into the database
        cursor.execute('INSERT INTO users VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "user")'
                       .format(login.get(), password.get(), name.get(), surname.get(), day.get(), month.get(),
                               year.get(), telephone.get()
                               )
                       )

        database.commit()
        cursor.close()
        database.close()

        # Send message about success and close window
        messagebox.showinfo('Підтвердження', 'Успішна реєстрація')
        root.destroy()
    except sqlite3.IntegrityError:
        """If login is exist"""
        messagebox.showinfo(' Проблема з Реєстрацією ', ' Логін вже зайнято ')
    except Exception as e:
        """Other problems with database"""
        messagebox.showinfo(' Проблема з Реєстрацією ', ' Проблема з Реєстрацією\n' + str(e))
