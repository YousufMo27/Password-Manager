#imports
import sqlite3
import hashlib
from tkinter import *
from tkinter import simpledialog
from tkinter import ttk
from functools import partial
import easygui
import customtkinter
import uuid
import pyperclip
import base64
import os


#setting up database
with sqlite3.connect("passwords.db") as db:
    cursor = db.cursor()

#creaes a table if the primary password does not exist yet
cursor.execute("""
CREATE TABLE IF NOT EXISTS primarypassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL,
resetKey TEXT NOT NULL);
""")

#creates a table if the website, username and password data isn't empty
cursor.execute("""
CREATE TABLE IF NOT EXISTS Passwords(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")
#inputGetter function takes user input via popup screens
def inputGetter(string):
    #popup screen
    input = easygui.enterbox(string, title="Enter Data")
    #input gets returned
    return input

#custom tkinter sets the theme to be blue and appearance to dark
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

#Opening Window
screen = Tk()
screen['bg'] = '#242424'
#title of the window is passwords
screen.title("Passwords")

#hashedPass uses the hashlib module to hash any input it's given
#in this case the password and returns that input
def hashedPass(input):
    hash = hashlib.sha256(input)
    hash = hash.hexdigest()
    #returning hashed password
    return hash
#function for the first screen
def primaryScreen():
    for widget in screen.winfo_children():
        widget.destroy()
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
            deletePass = "DELETE FROM primarypassword WHERE id = 1"
            cursor.execute(deletePass)
            #hashing the password
            hashPass = hashedPass(input.get().encode("utf-8"))
            randomKey = str(uuid.uuid4().hex)
            resetKey = hashedPass(randomKey.encode('utf-8'))
            #inserting the password into database
            insert_password = """INSERT INTO primarypassword(password, resetKey)
            VALUES(?,?) """
            cursor.execute(insert_password, [(hashPass),(resetKey)])
            #commiting the change
            db.commit()
            #the function which displays all the saved passwords is called
            resetScreen(randomKey)
        else:
            label.config(text="Passwords do not match")
    #button modified and improved using custom tkinter module
    button = customtkinter.CTkButton(frame, text="Save", command= passwordSave)
    button.pack(pady=(14,0))

#resetScreen function displays the key to the user
def resetScreen(resetKey):
    for widget in screen.winfo_children():
        widget.destroy()
    screen.geometry("700x350")
    #using labels for thegui
    opening_Label = Label(text="Reset Password",fg="white",bg="#242424",font=('Georgia 20'))
    #centers the label
    opening_Label.pack()
    opening_Label.pack(pady=(20,0))

    #frame places the login prompt all in one 
    frame = Frame(screen, width=350, height=150, bg="#242424")
    frame.pack()
    frame.pack(pady = (35,0))

    #label and entry used for first input and text
    label = Label(frame, text="Save Key",fg="white",bg="#242424")
    label.config(anchor=CENTER)
    label.pack()

    #label_One and entry used for second input and text
    label_One = Label(frame, text = resetKey,fg="white",bg="#242424")
    label_One.config(anchor=CENTER)
    label_One.pack()

    #copyToClipboard function copies the key to the users clipboard
    def copyToClipboard():
        pyperclip.copy(label_One.cget("text"))

    #button modified and improved using custom tkinter module
    button = customtkinter.CTkButton(frame, text="Copy to Clipboard", command= copyToClipboard)
    button.pack(pady=(14,0))
    #returnToContainer takes user to container screen
    def returnToContainer():
        passwordContainer()
    #button calls the returnToContainer function
    button = customtkinter.CTkButton(frame, text="Return to Container", command= returnToContainer)
    button.pack(pady=(14,0))

#resetWindow shows the window in which the user must input the reset Key
def resetWindow():
    for widget in screen.winfo_children():
        widget.destroy()
    screen.geometry("700x350")
    #using labels for thegui
    opening_Label = Label(text="Enter Key",fg="white",bg="#242424",font=('Georgia 20'))
    #centers the label
    opening_Label.pack()
    opening_Label.pack(pady=(20,0))

    #frame places the login prompt all in one 
    frame = Frame(screen, width=350, height=150, bg="#242424")
    frame.pack()
    frame.pack(pady = (35,0))

    #label and entry used for first input and text
    label = Label(frame, text="Enter Key",fg="white",bg="#242424")
    label.config(anchor=CENTER)
    label.pack()
    #entry used for user input
    input = Entry(frame,width=20,font=('Arial',11))
    input.pack()
    input.focus()


    #label_One and entry used for second input and text
    label_One = Label(frame,fg="white",bg="#242424")
    label_One.config(anchor=CENTER)
    label_One.pack()
    #getKey hashes the key then executes
    def getKey():
        recoveryKeyCheck = hashedPass(str(input.get()).encode('utf-8'))
        cursor.execute('SELECT * FROM primarypassword WHERE id = 1 AND resetKey = ?',[(recoveryKeyCheck)])
        return cursor.fetchall()
    #verifyKey checks to see if the key is valid
    def verifyKey():
        verified = getKey()
        #if correct then taken to the primary screen
        if verified:
            primaryScreen()
        else:
            #program extended until user inputs correct key
            input.delete(0, 'end')
            label_One.config(text='incorrect key, please try again')

    #button modified and improved using custom tkinter module
    button = customtkinter.CTkButton(frame, text="Done", command= verifyKey)
    button.pack(pady=(14,0))


#Login Function
def masterLogin():
    for widget in screen.winfo_children():
        widget.destroy()
    screen.geometry("700x400")

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
    input = Entry(frame,width=20,font=('Arial',11),show="*5")
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

    def resetPassword():
        resetWindow()
    #Enter button modified with CTk
    enterBtn = customtkinter.CTkButton(frame, text="Login", command= passwordCheck, height = 30, width=130)
    enterBtn.pack(pady=(14,0))

    enterBtn = customtkinter.CTkButton(frame, text="Reset Password", command= resetPassword, height = 30, width=130)
    enterBtn.pack(pady=(14,0))

#passwordContainer holds all the passwords and displays them
def passwordContainer():
    for widget in screen.winfo_children():
        widget.destroy()
        
    frame = Frame(screen)
    frame.pack(fill=BOTH, expand=1)

    #scrollbar setup for when it's necessary to scroll
    canvas = Canvas(frame,bg="#242424")
    canvas.pack(side=LEFT,fill=BOTH,expand = 1)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL,command=canvas.yview)
    scrollbar.pack(side=RIGHT,fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
    secondFrame = Frame(canvas,bg="#242424")
    canvas.create_window((0,0), window=secondFrame, anchor="nw")

    #function adds information to database
    def addInfo():
        #strings declared for each respective column
        website = "Website"
        username = "Username"
        password = "Password"
        #inputGetter function called
        websiteInput = inputGetter(website)
        usernameInput = inputGetter(username)
        passwordInput = inputGetter(password)
        #values are inserted into database
        insert_values = """INSERT INTO Passwords(website,username,password)
        VALUES(?,?,?)"""
        #executes and commit
        cursor.execute(insert_values,(websiteInput,usernameInput,passwordInput))
        db.commit()
        #function call of the password screen
        passwordContainer()
    #deleteInfo fucntion deletes data if user wished
    def deleteInfo(input):
        cursor.execute("DELETE FROM Passwords WHERE id = ?", (input,))
        db.commit()
        passwordContainer()
    #setting screen geometry
    screen.geometry("700x350")
    #Label used for the text on screen
    label = Label(secondFrame, text="Passwords",bg="#242424",fg = "white", font = ("Arial",12))
    label.grid(column=1,padx=(112,50),pady=(10,12))
    #button used for adding password
    button = customtkinter.CTkButton(secondFrame, text="Add Password", command= addInfo)
    button.grid(column=1, padx=(112,50),pady=(0,20))
    #column labels
    webLabel = Label(secondFrame, text="Website",fg="white",bg="#242424")
    webLabel.grid(row = 2, column=0, padx=55)
    userLabel = Label(secondFrame, text="Username",bg="#242424",fg="white")
    userLabel.grid(row = 2, column=1, padx=55)
    passLabel = Label(secondFrame, text="Password",bg="#242424",fg="white")
    passLabel.grid(row = 2, column=2, padx=55)
    #execute
    cursor.execute("SELECT * FROM Passwords")
    #if there is no data
    if (cursor.fetchall() != None):
        i = 0
        #loop begins
        while True:
            #fetches data from passwords db
            cursor.execute("SELECT * FROM Passwords")
            arr = cursor.fetchall() 
            if (len(arr) == 0):
                break
            #labels for website, username, and Password data
            label = Label(secondFrame, text=(arr[i][1]),bg="#242424",fg="white")
            label.grid(column=0, row = i+3)
            label = Label(secondFrame, text=(arr[i][2]),bg="#242424",fg="white")
            label.grid(column=1, row = i+3)
            label = Label(secondFrame, text=(arr[i][3]),bg="#242424",fg="white")
            label.grid(column=2, row = i+3)
            #remove button
            button = Button(secondFrame, text="Remove",command= partial(deleteInfo,arr[i][0]),bg="#242424",fg="white")
            button.grid(column=3,row=i+3,pady=10)
            #i keeps incrementing as the loop runs
            i = i+1
            cursor.execute("SELECT * FROM Passwords")
            #only when there is less data than the value of i the loop will end
            if (len(cursor.fetchall()) <= i):
                break

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
