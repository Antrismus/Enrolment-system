"""
Log in form

Created by Dmytro Kyrychkov
17/05/2019
"""
from tkinter import *
from tkinter import messagebox
import wd_confirmation
import wd_registration
import sqlite3
import wdf_login


def start():
    """Create Login window"""
    # Create window
    root = Tk()
    root.title('Вхід (Головна)')
    root.geometry('270x150')
    root.resizable(0, 0)

    # login container
    login = StringVar()

    # Create Label and Entry for login
    login_label = Label(root, text='Логін: ', padx=5, pady=5)
    login_label.place(x=30, y=20)
    login_entry = Entry(root, textvariable=login)
    login_entry.place(x=100, y=25)

    # password container
    password = StringVar()

    # Create Label and Entry for password
    password_label = Label(root, text='Пароль: ', padx=5, pady=5)
    password_label.place(x=30, y=50)
    password_entry = Entry(root, textvariable=password, show="•")
    password_entry.place(x=100, y=50)

    # Buttons
    login_button = Button(root, text=' Увійти ', command=lambda: log_in(login, password_entry, root))
    login_button.place(x=30, y=110)
    root.bind('<Return>', lambda event: log_in(login, password_entry, root))
    registration_button = Button(root, text=' Реєстрація ', command=wd_registration.start)
    registration_button.place(x=85, y=110)
    exit_button = Button(root, text=' Вихід ', command=lambda: wd_confirmation.start('Бажаєте вийти?', root.destroy))
    exit_button.place(x=200, y=110)

    root.mainloop()


def log_in(login, password, root):
    """Login function"""
    try:
        # Connect to users databases
        database = sqlite3.connect('databases\\users.db')
        cursor = database.cursor()

        cursor.execute('SELECT * FROM users WHERE login = "{}"'.format(login.get()))
        ans = cursor.fetchall()
        if len(ans) != 0:
            if password.get() == ans[0][1]:
                messagebox.showinfo('Вхід', 'Успішний вхід')
                root.destroy()
                wdf_login.open_user(login.get())
            else:
                messagebox.showinfo('Вхід', 'Неправильний логін або пароль')
        else:
            messagebox.showinfo('Вхід', 'Неправильний логін або пароль')

        cursor.close()
        database.close()
    except Exception as e:
        messagebox.showinfo('Щось пішло не так', 'Ууупс... Щось зламалось...\n' + str(e))
