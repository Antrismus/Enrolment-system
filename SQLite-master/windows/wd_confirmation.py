"""
Confirmation module
    ask - aks in form
    wtd - what to do if 'Ok'

Created by Dmytro Kyrychkov
18/05/2019
"""
from tkinter import *


def start(ask, wtd):
    """Create confirmation window"""
    # Create Top-window
    dialog_window = Toplevel()
    dialog_window.title('Вихід')
    dialog_window.geometry('300x150+300+150')
    dialog_window.resizable(0, 0)
    dialog_window.grab_set()
    dialog_window.focus_set()

    # Create Top-Frame and ask
    frame = Frame(dialog_window)
    frame.place(height=75, width=300)
    text = Label(frame, text=ask)
    text.place(x=75, y=37, height=15, width=150)

    # Create Bottom-Frame and Buttons
    frame1 = Frame(dialog_window)
    frame1.place(height=75, width=300, y=75)
    btn1 = Button(frame1, text='Так', command=lambda: wtd_and_destroy(wtd, dialog_window))
    btn1.place(relx=.3, rely=.5, anchor='c', height=30, width=60)
    btn2 = Button(frame1, text=' Ні ', command=dialog_window.destroy)
    btn2.place(relx=.7, rely=.5, anchor='c', height=30, width=60)

    dialog_window.bind('<Return>', lambda event: wtd_and_destroy(wtd, dialog_window))


def wtd_and_destroy(wtd, root):
    """Template function for close dialog window and start function wtd (what to do)"""
    root.destroy()
    wtd()
