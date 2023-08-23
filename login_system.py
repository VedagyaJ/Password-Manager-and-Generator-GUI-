from tkinter import *
import os
import json
from cryptography.fernet import Fernet

# Login System
class LoginSystem:
    def __init__(self, root, function):
        self.root = root
        self.function = function

        # Create the file where the data is stored
        if not os.path.isfile('database.json'):
            with open('database.json', 'w') as f:
                f.write('{"usernames": [], "passwords": []}')

        # Load the data into variables
        with open('database.json', 'r') as f:
            data = json.load(f)
            self.available_accounts_usernames = data['usernames']
            self.available_accounts_passwords = data['passwords']

        self.create_buttons()

    def create_buttons(self):
        self.login_btn = Button(self.root, text="Login", padx=51, pady=20, command=self.login)
        self.signup_btn = Button(self.root, text="Sign Up", padx=45, pady=20, command=self.signup)

        # Show Widgets on Screen
        self.login_btn.grid()
        self.signup_btn.grid(row=1, column=0)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def back(self):
        self.clear_screen()
        self.create_buttons()

    def login(self):
        self.clear_screen()
        self.login_window()

    def login_window(self):
        # Login Widgets
        self.username_label = Label(self.root, text="Username: ")
        self.username_entry = Entry(self.root)

        self.password_label = Label(self.root, text="Password: ")
        self.password_entry = Entry(self.root, show="*")

        submit_btn = Button(self.root, text="Submit", command=self.login_submit, padx=40)
        back_btn = Button(self.root, text="Back", command=self.back)

        # Show Widgets on Screen
        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        self.password_label.grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1, pady=5)
        submit_btn.grid(row=2, column=1)
        back_btn.grid(row=2, column=0)

    def login_submit(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()

        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)

        if self.username in self.available_accounts_usernames:
            key = self.make_key(self.username)
            fer = Fernet(key)

            if self.password == str(fer.decrypt(self.available_accounts_passwords[self.available_accounts_usernames.index(self.username)].encode()).decode()):

                # Clear the screen and call the function in main.py when someone logs in
                self.clear_screen()
                self.function(self.username)

            else:
                Label(self.root, text="Access Denied").grid(row=4, column=0, columnspan=2)

        else:
            Label(self.root, text="Access Denied").grid(row=4, column=0, columnspan=2)

    def signup(self):
        self.clear_screen()
        self.signup_window()

    def signup_window(self):
        # Signup Widgets
        self.username_label = Label(self.root, text="Username: ")
        self.username_entry = Entry(self.root)

        self.password_label = Label(self.root, text="Password: ")
        self.password_entry = Entry(self.root, show="*")

        self.confirm_password_label = Label(self.root, text="Confirm Password: ")
        self.confirm_password_entry = Entry(self.root, show="*")

        submit_btn = Button(self.root, text="Submit", command=self.signup_submit, padx=40)
        back_btn = Button(self.root, text="Back", command=self.back)

        # Show Widgets on Screen
        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        self.password_label.grid(row=1, column=0, pady=(5, 0))
        self.password_entry.grid(row=1, column=1, pady=(5, 0))
        self.confirm_password_label.grid(row=2, column=0)
        self.confirm_password_entry.grid(row=2, column=1, pady=5)
        submit_btn.grid(row=3, column=1, columnspan=2)
        back_btn.grid(row=3, column=0)

    def signup_submit(self):
        # Get the Username and Password from the Entry widgets
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        confirm_pass =  self.confirm_password_entry.get()

        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.confirm_password_entry.delete(0, END)

        Label(self.root, text="                                                                                               ").grid(row=4, column=0, columnspan=2)

        if self.username in self.available_accounts_usernames:
            Label(self.root, text="                                                                                               ").grid(row=4, column=0, columnspan=2)
            Label(self.root, text="This username is already taken").grid(row=4, column=0, columnspan=2)
        else:

            if len(self.password) < 8:
                Label(self.root, text="                                                                                               ").grid(row=4, column=0, columnspan=2)
                Label(self.root, text="This password should be more than 8 characters.").grid(row=4, column=0, columnspan=2)
            
            else:
                if self.password == confirm_pass:
                    key = self.make_key(self.username)
                    fer = Fernet(key)

                    # Store it in the JSON file
                    self.available_accounts_usernames.append(self.username)
                    self.available_accounts_passwords.append(str(fer.encrypt(self.password.encode()).decode()))

                    with open('database.json', 'w') as f:
                        json.dump({'usernames': self.available_accounts_usernames, 'passwords': self.available_accounts_passwords}, f)
                    Label(self.root, text="                                                                                               ").grid(row=4, column=0, columnspan=2)
                    Label(self.root, text="Your account has been created.").grid(row=4, column=0, columnspan=2)
                else:
                    Label(self.root, text="                                                                                               ").grid(row=4, column=0, columnspan=2)
                    Label(self.root, text="The passwords don't match.").grid(row=4, column=0, columnspan=2)

    def make_key(self, username):
        if not os.path.isfile(f"Keys\Master Password\{username}.key"):
            key = Fernet.generate_key()
            with open(f"Keys\Master Password\{username}.key", "wb") as key_file:
                key_file.write(key)

            return key

        else:
            file = open(f"Keys\Master Password\{username}.key", "rb")
            key = file.read()
            file.close()
            
            return key