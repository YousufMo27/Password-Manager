#imports
import sqlite3
import hashlib
from tkinter import *
import customtkinter

#setting up database
with sqlite3.connect("passwords.db") as db:
    cursor = db.cursor()

#creaes a table if the primary password does not exist yet
cursor.execute("""
CREATE TABLE IF NOT EXISTS primarypassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
""")

#custom tkinter sets the theme to be blue and appearance to dark
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

#Opening Window
screen = customtkinter.CTk()
#title of the window is passwords
screen.title("Passwords")

#hashedPass uses the hashlib module to hash any input it's given
#in this case the password and returns that input
def hashedPass(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()
    #returning hashed password
    return hash
#function for the first screen
def primaryScreen():
    screen.geometry("700x350")
    #using labels for thegui
    opening_Label = Label(text="Password Manager",fg="white",bg="#242424",font=('Georgia 20'))
    #centers the label
    opening_Label.pack()
    opening_Label.pack(pady=(20,0))

    #frame places the login prompt all in one 
    frame = Frame(screen, width=350, height=150, bg="#242424")
    frame.pack()
    frame.pack(pady = (35,0))

    #label and entry used for first input and text
    label = Label(frame, text="Create Primary Password",fg="white",bg="#242424")
    label.config(anchor=CENTER)
    label.pack()
    input = Entry(frame,width=27)
    input.pack()
    input.focus()
    input.pack(pady=(0,20))

    #label_One and entry used for second input and text
    label_One = Label(frame, text = "Re-enter Password",fg="white",bg="#242424")
    label_One.config(anchor=CENTER)
    label_One.pack()
    second_Input = Entry(frame,width=27)
    second_Input.pack()
    second_Input.focus()
    second_Input.pack(pady=2)

    #passwordSave function used to save primary password
    def passwordSave():
        #conditional used to verify if both entered passwords match
        if (input.get() == second_Input.get()):
            #hashing the password
            hashPass = hashedPass(input.get().encode("utf-8"))
            #inserting the password into database
            insert_password = """INSERT INTO primarypassword(password)
            VALUES(?) """
            cursor.execute(insert_password, [(hashPass)])
            #commiting the change
            db.commit()
            #the function which displays all the saved passwords is called
            passwordContainer()
        else:
            label.config(text="Passwords do not match")
    #button modified and improved using custom tkinter module
    button = customtkinter.CTkButton(frame, text="Save", command= passwordSave)
    button.pack(pady=(14,0))


#Login Function
def masterLogin():
    screen.geometry("700x350")

    #labels used
    opening_Label = Label(text="Login Screen",fg="white",bg="#242424",font=('Georgia 20'))
    opening_Label.pack()
    opening_Label.pack(pady=(20,0))

    #frame used to keep login screen in one container
    frame = Frame(screen, width=350, height=150, bg="#242424")
    frame.pack()
    frame.pack(pady = 60)

    #label used for prompt
    label = Label(frame, text="Enter Primary Password",bg="#242424",fg = "white", font = ("Arial",12))
    label.config(anchor=CENTER)
    label.pack(pady=(0,17))

    #entry used for user input
    input = Entry(frame,width=20,font=('Arial',11))
    input.pack()
    input.focus()

    #second label used
    label_One = Label(screen,bg = "#242424",fg="white", font = ("Arial",12))
    label_One.config(anchor=CENTER)
    label_One.pack()

    #getPrimaryPassword function 
    def getPrimaryPassword():
        checkHashedPass = hashedPass(input.get().encode("utf-8"))
        #executes hashed password
        cursor.execute("SELECT * FROM primarypassword WHERE id = 1 AND password = ?", [(checkHashedPass)])
        #returns all remaining rows
        return cursor.fetchall()
    
    #passwordCheck function checks if the primary password is entered
    def passwordCheck():
        #getPrimaryPassword called
        passWord = getPrimaryPassword()
        #if password matches then taken to password container
        if (passWord):
            passwordContainer()
        #if incorrect
        else:
            #extends window time if incorrect password
            input.delete(0, 'end')
            label_One.config(text="Wrong Password")

    #Enter button modified with CTk
    enterBtn = customtkinter.CTkButton(frame, text="Login", command= passwordCheck, height = 30, width=130)
    enterBtn.pack(pady=(14,0))

#passwordContainer holds all the passwords and displays them
def passwordContainer():
    for widget in screen.winfo_children():
        widget.destroy()
    screen.geometry("700x350")

    #Label used for the text on screen
    label = Label(screen, text="Passwords",bg="#242424",fg = "white", font = ("Arial",12))
    label.config(anchor=CENTER)
    label.pack(pady=20)

#executes database
cursor.execute("SELECT * FROM primarypassword")

#if there are no rows then directed to master login
if cursor.fetchall():
    masterLogin()
#else you are taken to the login screen
else:
    primaryScreen()
#.mainloop keeps window running          
screen.mainloop()

