"""
Window for user

Created by Dmytro Kyrychkov
19/05/2019
"""
from tkinter import *
import wd_confirmation
import wd_change
import wdf_login


def start(user):
    """Create user window"""
    root = Tk()
    root.title('Власний кабінет: ' + user.login)
    root.geometry('400x370')
    root.resizable(0, 0)

    # Name option
    name_label = Label(root, text='Імя: ' + user.name, padx=5, pady=5)
    name_label.place(x=30, y=30, width=190)

    name_change_button = Button(root, text='Змінити',
                                command=lambda: wd_change.start_change_button('name', user.login))
    name_change_button.place(x=220, y=30, width=150)

    # Surname option
    surname_label = Label(root, text='Прізвище: ' + user.surname, padx=5, pady=5)
    surname_label.place(x=30, y=60, width=190)

    surname_change_button = Button(root, text='Змінити',
                                   command=lambda: wd_change.start_change_button('surname', user.login))
    surname_change_button.place(x=220, y=60, width=150)

    # Date option
    date_label = Label(root, text='Дата народження: {} {} {}'.format(user.day, user.month, user.year), padx=5, pady=5)
    date_label.place(x=30, y=90, width=190)

    date_change_button = Button(root, text='Змінити', command=lambda: wd_change.start_change_date(user.login))
    date_change_button.place(x=220, y=90, width=150)

    # Telephone option
    telephone_label = Label(root, text='Телефон: ' + user.telephone, padx=5, pady=5)
    telephone_label.place(x=30, y=120, width=190)

    telephone_change_button = Button(root, text='Змінити',
                                     command=lambda: wd_change.start_change_button('telephone', user.login))
    telephone_change_button.place(x=220, y=120, width=150)

    # Login option
    login_label = Label(root, text='Логін: ' + user.login, padx=5, pady=5)
    login_label.place(x=30, y=160, width=190)

    login_change_button = Button(root, text='Змінити',
                                 command=lambda: wd_change.start_change_login(root, user.login))
    login_change_button.place(x=220, y=160, width=150)

    # Password option
    password = StringVar(root)
    repeat_password = StringVar(root)

    password_label = Label(root, text='Новий пароль: ', padx=5, pady=5)
    password_label.place(x=30, y=190, width=190)
    password_entry = Entry(root, textvariable=password, show='•')
    password_entry.place(x=220, y=190, width=150)

    repeat_password_label = Label(root, text='Повторити пароль: ', padx=5, pady=5)
    repeat_password_label.place(x=30, y=220, width=190)
    repeat_password_entry = Entry(root, textvariable=repeat_password, show='•')
    repeat_password_entry.place(x=220, y=220, width=150)

    password_change_button = Button(root, text='Змінити',
                                    command=lambda: wd_change.start_change_password(password, repeat_password,
                                                                                    user.login, root)
                                    )
    password_change_button.place(x=220, y=250, width=150)

    # Status option
    status_label = Label(root, text='Статус: ' + user.permission, padx=5, pady=5)
    status_label.place(x=30, y=280, width=340)

    # Buttons
    update_button = Button(root, text=' Оновити ', command=lambda: update_window(user.login, root))
    update_button.place(x=30, y=320, width=165)
    exit_button = Button(root, text=' Вихід ', command=lambda: wd_confirmation.start('Бажаєте вийти?', root.destroy))
    exit_button.place(x=205, y=320, width=165)

    root.mainloop()


def update_window(login, root):
    """Update user window"""
    root.destroy()
    wdf_login.open_user(login)
