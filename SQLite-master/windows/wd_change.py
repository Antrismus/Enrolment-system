"""
Create change widow

Created by Dmytro Kyrychkov
19/05/2019
"""
from tkinter import *
from tkinter import messagebox
import wd_confirmation
import wd_registration
import wd_user
import sqlite3
import datetime


def start_change_button(element, login):
    """Create window for changes simple option"""
    root = Toplevel()
    root.title('Змінити: ' + element)
    root.geometry('270x130')
    root.resizable(0, 0)
    root.focus_set()
    root.grab_set()

    label = Label(root, text=element)
    label.place(x=30, y=30)

    # New element
    new_element = StringVar()
    new_element_entry = Entry(root, textvariable=new_element)
    new_element_entry.place(x=100, y=30, width=140)

    # Buttons
    close_btn = Button(root, text='Закрити', command=root.destroy)
    close_btn.place(x=30, y=80, width=100)

    save_btn = Button(root, text='Зберегти', command=lambda: wd_confirmation.start(
        'Бажаєте змінити?',
        lambda: save(element, new_element, login, root)
    ))
    save_btn.place(x=140, y=80, width=100)

    root.bind('<Return>', lambda event: wd_confirmation.start(
        'Бажаєте змінити?',
        lambda: save(element, new_element, login, root)
    ))


def start_change_date(login):
    """Create window for changes date"""
    root = Toplevel()
    root.title('Змінити: Дату')
    root.geometry('450x130')
    root.resizable(0, 0)
    root.focus_set()
    root.grab_set()

    # Date of birthday containers
    day = IntVar(root)
    month = StringVar(root)
    year = IntVar(root)

    # Create input for data
    day_label = Label(root, text=' Дата народження:', padx=5, pady=5)
    day_label.place(x=30, y=20)

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
    day_input.place(x=155, y=20, width=50)
    month_input = OptionMenu(root, month, *month_options)
    month_input.place(x=205, y=20, width=100)
    year_input = OptionMenu(root, year, *year_options)
    year_input.place(x=305, y=20, width=100)

    # Buttons
    close_btn = Button(root, text='Закрити', command=root.destroy)
    close_btn.place(x=30, y=80, width=100)

    save_btn = Button(root, text='Зберегти', command=lambda: wd_confirmation.start(
        'Бажаєте змінити?',
        lambda: save_date(day, month, year, login, root)
    ))
    save_btn.place(x=310, y=80, width=100)

    root.bind('<Return>', lambda event: wd_confirmation.start(
        'Бажаєте змінити?',
        lambda: save_date(day, month, year, login, root)
    ))


def start_change_login(main_root, login):
    """Create window for changes login"""
    root = Toplevel()
    root.title('Змінити: Логін')
    root.geometry('270x130')
    root.resizable(0, 0)
    root.focus_set()
    root.grab_set()

    label = Label(root, text='Логін')
    label.place(x=30, y=30)

    # New element
    new_element = StringVar()
    new_element_entry = Entry(root, textvariable=new_element)
    new_element_entry.place(x=100, y=30, width=140)

    # Buttons
    close_btn = Button(root, text='Закрити', command=root.destroy)
    close_btn.place(x=30, y=80, width=100)

    save_btn = Button(root, text='Зберегти', command=lambda: wd_confirmation.start(
        'Бажаєте змінити?',
        lambda: save_login(new_element, login, root, main_root)
    ))
    save_btn.place(x=140, y=80, width=100)

    root.bind('<Return>', lambda event: wd_confirmation.start(
        'Бажаєте змінити?',
        lambda: save_login(new_element, login, root, main_root)
    ))


def start_change_password(password, repeat_password, login, root):
    """Chane password"""
    wd_confirmation.start('Змінити пароль?', lambda: save_password(password, repeat_password, login, root))


def save(element, new_element, login, root, destroy=True):
    """Save changes"""
    try:
        database = sqlite3.connect('databases\\users.db')
        cursor = database.cursor()

        cursor.execute('UPDATE users SET {} = "{}" WHERE login = "{}";'.format(element, new_element.get(), login))
        database.commit()

        cursor.close()
        database.close()
        if destroy:
            root.destroy()
        return True
    except Exception as e:
        messagebox.showinfo('Помилка', str(e))
        return False


def save_date(day, month, year, login, root):
    """Save date"""
    if wd_registration.check_date(day, month, year):
        save('day', day, login, root, False)
        save('month', month, login, root, False)
        save('year', year, login, root, True)


def save_login(new_element, login, root, main_root):
    """Save login"""
    # Check and try to save
    if wd_registration.check_login(new_element) and save('login', new_element, login, root):
        try:
            wd_user.update_window(new_element.get(), main_root)
        except Exception as e:
            messagebox.showinfo('Зміна Логіну', 'Проблема зі зміною логіну:' + str(e))


def save_password(password, repeat_password, login, root):
    """Save password"""
    if wd_registration.check_password(password, repeat_password):
        save('password', password, login, root, False)
