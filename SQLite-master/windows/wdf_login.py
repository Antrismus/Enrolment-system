"""
Functions for login window
Class User

Created by Dmytro Kyrychkov
19/05/2019
"""
from tkinter import *
import sqlite3
import wd_user
import wd_admin


class User:
    """Class for contain user information"""
    def __init__(self, description):
        self.login = description[0]
        self.password = description[1]
        self.name = description[2]
        self.surname = description[3]
        self.day = description[4]
        self.month = description[5]
        self.year = description[6]
        self.telephone = description[7]
        self.permission = description[8]


def open_user(login):
    """Open user and start user or admin window"""
    # Read user from database
    users = sqlite3.connect('databases\\users.db')
    cursor = users.cursor()

    cursor.execute('SELECT * FROM users WHERE login="{}"'.format(login))
    description = cursor.fetchall()

    cursor.close()
    users.close()

    user = User(description[0])

    # Start user window
    if user.permission == 'user':
        wd_user.start(user)
    # Start admin window
    elif user.permission == 'admin':
        wd_admin.start('', '')
