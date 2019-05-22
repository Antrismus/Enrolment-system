"""
Admin window

Created by Dmytro Kyrychkov
21/05/2019
"""
from tkinter import *
from tkinter import messagebox
import wd_user
import wd_confirmation
import wdf_login
import sqlite3


def start(filter_element='', filter_value=''):
    """Start admin window"""
    root = Tk()
    root.title('Панель адміністрування')
    root.geometry("820x205")
    root.resizable(0, 0)

    # Filters container
    element = StringVar(root)
    variable = StringVar(root)

    # User options
    users = create_users_dictionary(filter_element, filter_value)

    # User container
    select_user = StringVar(root)
    select_user.set(next(iter(users)))

    # Main Label
    label = Label(root, text=' Користувачі:', padx=5, pady=5)
    label.place(x=10, y=20, width=800)

    # Users input
    users_input = OptionMenu(root, select_user, *users)
    users_input.place(x=10, y=50, width=800)

    # Filter option
    filter_option = [
        '',
        'login',
        'name',
        'surname',
        'telephone',
        'password',
        'day',
        'month',
        'year'
    ]

    # Filters Label
    filter_text = Label(root, text='Фільтер')
    filter_text.place(x=0, y=90, width=800)
    filter_label = Label(root, text='Поле:')
    filter_label.place(x=10, y=120, height=30)
    variable_label = Label(root, text='Значення:')
    variable_label.place(x=160, y=120, height=30)

    # Filters Input
    filter_input = OptionMenu(root, element, *filter_option)
    filter_input.place(x=50, y=120, width=100)
    variable_input = Entry(root, textvariable=variable)
    variable_input.place(x=230, y=122, height=25)

    # Active filters
    filter_button = Button(root, text='Фільтрувати', command=lambda: update_window(element.get(), variable.get(), root))
    filter_button.place(x=610, y=120, width=200)

    # Button
    open_button = Button(text='Відкрити', command=lambda: wd_user.start(wdf_login.User(users[select_user.get()])))
    open_button.place(x=10, y=170, width=200)
    deleted_button = Button(text='Видалити', command=
                            lambda: wd_confirmation.start('Видалити користувача?',
                                                          lambda: deleted_user(
                                                              wdf_login.User(users[select_user.get()]), root)
                                                          )
                            )
    deleted_button.place(x=220, y=170, width=200)
    close_button = Button(text='Вийти', command=lambda: wd_confirmation.start('Бажаєте вийти?', root.destroy))
    close_button.place(x=610, y=170, width=200)

    root.mainloop()


def update_window(element, variable, root):
    """Update admin window"""
    root.destroy()
    start(element, variable)


def create_users_dictionary(element='', variable=''):
    """Create users dictionary with filter"""
    users = sqlite3.connect('databases\\users.db')
    cursor = users.cursor()

    # If filter is empty
    if element == '':
        cursor.execute('SELECT * FROM users')
    else:
        try:
            cursor.execute('SELECT * FROM users WHERE {} = "{}"'.format(element, variable))
        except Exception as e:
            # Send Error message
            messagebox.showinfo('Помилка при отриманні даних', str(e))
            # Select all
            cursor.execute('SELECT * FROM users WHERE {} = "{}"'.format(element, variable))
    # Create dictionary
    users_dictionary = {}
    for i in cursor.fetchall():
        user_information = 'Login: {} | Password: {} | Name: {} | Surname: {} | Birth Day: {} {} {} | ' \
                               'Telephone: {} | Permission: {} '.format(i[0], i[1], i[2], i[3], i[4],
                                                                        i[5], i[6], i[7], i[8])
        users_dictionary[user_information] = i
    return users_dictionary


def deleted_user(user, root):
    """Delete user"""
    database = sqlite3.connect('databases\\users.db')
    cursor = database.cursor()

    cursor.execute('SELECT * FROM users WHERE login = "{}"'.format(user.login))
    database.commit()
    permission = cursor.fetchall()
    database.commit()

    # Check permission
    if permission[0][8] == 'user':
        cursor.execute('DELETE FROM users WHERE login = "{}"'.format(user.login))
        database.commit()
    else:
        messagebox.showinfo('Видалення', 'Не можливо видалити користувача з правами адміністратора')

    cursor.close()
    database.close()
    # Update window with new users
    update_window('', '', root)
