#imports
import sqlite3
import hashlib
from tkinter import *
from tkinter import simpledialog
from functools import partial
import easygui
import customtkinter
import uuid
import pyperclip
import base64
import os
from cryptography.hazmat.primitives import hashes 
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
#backend and salt values
backend = default_backend()
saltValue = b'2444'
#kdf derives a key 
kdf = PBKDF2HMAC (
    #hashes using SHA256
    algorithm=hashes.SHA256(),
    length=32,
    salt=saltValue,
    iterations=100000,
    backend=backend
)
#encryption Key 
encryptionKey = 0

#encrypt function used to encrypt and the return the encrypted key
def encrypt(message: bytes, key: bytes) ->bytes:
    return Fernet(key).encrypt(message)

#encrypt function used to decrypt and the return the decrypted token
def decrypt(message: bytes, token: bytes) ->bytes:
    return Fernet(token).decrypt(message)

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
    input = easygui.enterbox(string, title="Input String")
    #input gets returned
    return input
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

            global encryptionKey
            encryptionKey = base64.urlsafe_b64encode(kdf.derive(input.get().encode()))

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

#resetScreen function used for the copy key screeen
def resetScreen(resetKey):
    for widget in screen.winfo_children():
        widget.destroy()
    screen.geometry("700x350")
    #using labels for thegui
    opening_Label = Label(text="Save The Key",fg="white",bg="#242424",font=('Georgia 20'))
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
    #function copies the key to the clipboard
    def copyToClipboard():
        pyperclip.copy(label_One.cget("text"))

    #button modified and improved using custom tkinter module
    button = customtkinter.CTkButton(frame, text="Copy to Clipboard", command= copyToClipboard)
    button.pack(pady=(14,0))
    #function returns to passwordContainer
    def returnToContainer():
        passwordContainer()
    #button used to call function
    button = customtkinter.CTkButton(frame, text="Return to Container", command= returnToContainer)
    button.pack(pady=(14,0))
#resetWindow function is the screen where the user inputs the recovery key
def resetWindow():
    for widget in screen.winfo_children():
        widget.destroy()
    screen.geometry("700x350")
    #using labels for the gui
    opening_Label = Label(text="Reset Password",fg="white",bg="#242424",font=('Georgia 20'))
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
    #getKey function hashes the key and then gets the key, returns remaining rows
    def getKey():
        recoveryKeyCheck = hashedPass(str(input.get()).encode('utf-8'))
        cursor.execute('SELECT * FROM primarypassword WHERE id = 1 AND resetKey = ?',[(recoveryKeyCheck)])
        return cursor.fetchall()
    #verifyKey will check if the inputted key is correct
    def verifyKey():
        #getKey function called
        verified = getKey()
        #if correct user will be returned to home screen
        if verified:
            primaryScreen()
        #otherwise user will be prompted to input again
        else:
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
    frame = Frame(screen, width=350, height=80, bg="#242424")
    frame.pack()
    frame.pack(pady = 60)

    #label used for prompt
    label = Label(frame, text="Enter Primary Password",bg="#242424",fg = "white", font = ("Arial",12))
    label.config(anchor=CENTER)
    label.pack(pady=(0,17))

    #entry used for user input
    input = Entry(frame,width=20,font=('Arial',11),show="*")
    input.pack()
    input.focus()

    #second label used
    label_One = Label(screen,bg = "#242424",fg="white", font = ("Arial",12))
    label_One.config(anchor=CENTER)
    label_One.pack(pady=(0,1))

    #getPrimaryPassword function 
    def getPrimaryPassword():
        checkHashedPass = hashedPass(input.get().encode("utf-8"))
        #encryptionKey encrypts the primary password
        global encryptionKey
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
            encryptionKey = base64.urlsafe_b64encode(kdf.derive(input.get().encode()))
            passwordContainer()
        #if incorrect
        else:
            #extends window time if incorrect password
            input.delete(0, 'end')
            label_One.config(text="Wrong Password")
  
    #resetPassword takes you to the window to enter the key
    def resetPassword():
        resetWindow()
    #Enter button modified with CTk
    enterBtn = customtkinter.CTkButton(frame, text="Login", command= passwordCheck, height = 30, width=130)
    enterBtn.pack(pady=(14,0))
    #reset password button
    enterBtn = customtkinter.CTkButton(frame, text="Reset Password", command= resetPassword, height = 30, width=130)
    enterBtn.pack(pady=(14,0))

#passwordContainer holds all the passwords and displays them
def passwordContainer():
    for widget in screen.winfo_children():
        widget.destroy()
    #function adds information to database
    def addInfo():
        #strings declared for each respective column
        website = "Website"
        username = "Username"
        password = "Password"
        #inputGetter function called with encrypted data
        websiteInput = encrypt(inputGetter(website).encode(),encryptionKey)
        usernameInput = encrypt(inputGetter(username).encode(),encryptionKey)
        passwordInput = encrypt(inputGetter(password).encode(),encryptionKey)
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
    #sets screen dimensions
    screen.geometry("700x350")
    #Label used for the text on screen
    label = Label(screen, text="Passwords",bg="#242424",fg = "white", font = ("Arial",12))
    label.grid(column=1,padx=(112,50),pady=(10,12))
    #button used for adding password
    button = customtkinter.CTkButton(screen, text="Add Password", command= addInfo)
    button.grid(column=1, padx=(112,50),pady=(0,20))
    #column labels
    webLabel = Label(screen, text="Website",fg="white",bg="#242424")
    webLabel.grid(row = 2, column=0, padx=55)
    userLabel = Label(screen, text="Username",bg="#242424",fg="white")
    userLabel.grid(row = 2, column=1, padx=55)
    passLabel = Label(screen, text="Password",bg="#242424",fg="white")
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
            #breaks if there are no entries in arrray
            if (len(arr) == 0):
                break
            #labels for website, username, and Password data
            label = Label(screen, text=(decrypt(arr[i][1], encryptionKey)),bg="#242424",fg="white")
            label.grid(column=0, row = i+3)
            label = Label(screen, text=(decrypt(arr[i][2], encryptionKey)),bg="#242424",fg="white")
            label.grid(column=1, row = i+3)
            label = Label(screen, text=(decrypt(arr[i][3], encryptionKey)),bg="#242424",fg="white")
            label.grid(column=2, row = i+3)
            #remove button
            button = Button(screen, text="Remove",command= partial(deleteInfo,arr[i][0]),bg="#242424",fg="white")
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

