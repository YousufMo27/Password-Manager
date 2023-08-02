import sqlite3
import hashlib
from tkinter import *
import customtkinter


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


screen = customtkinter.CTk()


screen.title("Passwords")


def primaryScreen():
    screen.geometry("700x350")


    frame = Frame(screen, width=350, height=150, bg="#242424")
    frame.pack()
    frame.pack(pady=90)


    label = Label(frame, text="Create Primary Password",fg="white",bg="#242424")
    label.config(anchor=CENTER)
    label.pack()
    input = Entry(frame,width=20)
    input.pack()
    input.focus()
    input.pack(pady=2)


    label_One = Label(frame, text = "Re-enter Password",fg="white",bg="#242424")
    label_One.config(anchor=CENTER)
    label_One.pack()
    second_Input = Entry(frame,width=20)
    second_Input.pack()
    second_Input.focus()
    second_Input.pack(pady=2)


    def passwordSave():
        if (input.get() == second_Input.get()):
            pass
        else:
            label.config(text="Passwords do not match")


    button = customtkinter.CTkButton(frame, text="Save", command= passwordSave)
    button.pack(pady=10)


#Login Function
def masterLogin():
    screen.geometry("350x150")


    label = Label(screen, text="Enter Primary Password")
    label.config(anchor=CENTER)
    label.pack()




    input = Entry(screen,width=20)
    input.pack()
    input.focus()


    label_One = Label(screen)
    label_One.config(anchor=CENTER)
    label_One.pack()


    def passwordCheck():
        password = "test"


        if (password == input.get()):
            passwordContainer()
        else:
            input.delete(0, 'end')
            label_One.config(text="Wrong Password")


    enterBtn = Button(screen,text="Enter", command=passwordCheck)
    enterBtn.pack(pady=10)


def passwordContainer():
    for widget in screen.winfo_children():
        widget.destroy()
    screen.geometry("700x350")


    label = Label(screen, text="Passwords")
    label.config(anchor=CENTER)
    label.pack()


primaryScreen()
#masterLogin()


screen.mainloop()

