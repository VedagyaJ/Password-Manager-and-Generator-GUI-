from password_generator import GeneratePassword
from login_system import LoginSystem
from cryptography.fernet import Fernet
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import json
import pyperclip

root = Tk()
root.title("Password Generator and Manager")

class PasswordManager:
    def __init__(self, username):
        self.username = username

        # Create the file where the passwords are stored
        if not os.path.isfile(f"Passwords\{self.username}.json"):
            with open(f"Passwords\{self.username}.json", "w") as f:
                f.write('{"services": [], "passwords": []}')

        # Save the passwords and services lists in variables
        with open(f"Passwords\{self.username}.json", "r") as f:
            data = json.load(f)
            self.account_passwords = data["passwords"]
            self.account_services = data["services"]

        self.key = self.make_key()
        self.fer = Fernet(self.key)

        self.logged_in()

    def make_key(self):
        if not os.path.isfile(f"Keys\Account Passwords\{self.username}.key"):
            key = Fernet.generate_key()
            with open(f"Keys\Account Passwords\{self.username}.key", "wb") as key_file:
                key_file.write(key)

            return key

        else:
            file = open(f"Keys\Account Passwords\{self.username}.key", "rb")
            key = file.read()
            file.close()

            return key

    def clear_screen(self):
        for widget in root.winfo_children():
            widget.destroy()

    def back(self):
        self.clear_screen()
        self.logged_in()

    def logged_in(self):
        # Make the logged in window
        title = Label(root, text=f"Welcome, {self.username}!", font=("Arial", 20, "bold"), anchor=W)

        self.options_frame = LabelFrame(root, padx=5, pady=5, bd=2)
        generate_button = Button(self.options_frame, text="Generate Password", width=25, pady=20, command=self.generate_password_window)
        view_button = Button(self.options_frame, text="View Existing Passwords", width=25, pady=20, command=self.view_password_window)
        add_button = Button(self.options_frame, text="Add Your Own Password", width=25, pady=20, command=lambda: self.add_window(True))
        file_button = Button(self.options_frame, text="Add a JSON File", width=25, pady=20, command=self.upload_menu)

        # Show widgets on screen
        title.grid(row=0, column=0, pady=10, padx=5, sticky=W+E)
        self.options_frame.grid(row=1, column=0)
        generate_button.grid(row=0, column=0)
        view_button.grid(row=0, column=1)
        add_button.grid(row=2, column=0)
        file_button.grid(row=2, column=1)

    def generate_password_window(self):
        # Make the window for generating passwords
        self.clear_screen()

        # Checkbox Variables
        self.includeUpper = StringVar()
        self.includeNumbers = StringVar()
        self.includeSpecial = StringVar()

        title = Label(root, text=f"Settings for Password Generation", font=("Arial", 20, "bold"), anchor=W)

        self.options_frame = LabelFrame(root, padx=5, pady=5, bd=2)
        pass_length_label = Label(self.options_frame, text="Length:   ")
        self.length_spinbox = Spinbox(self.options_frame, from_=1, to=32, state="readonly")
        include_label = Label(self.options_frame, text="Include: ")

        # Checkboxes
        upper_check = Checkbutton(self.options_frame, text="Uppercase Letters", variable=self.includeUpper, onvalue="yes", offvalue="no", anchor=W)
        num_check = Checkbutton(self.options_frame, text="Numbers", variable=self.includeNumbers, onvalue="yes", offvalue="no", anchor=W)
        special_check = Checkbutton(self.options_frame, text="Special Characters", variable=self.includeSpecial, onvalue="yes", offvalue="no", anchor=W)

        upper_check.deselect()
        num_check.deselect()
        special_check.deselect()

        # Buttons
        gen_pass_btn = Button(self.options_frame, text="Generate", command=self.generate_password)
        back_btn = Button(self.options_frame, text="Back", command=self.back)

        # Show widgets on screen
        title.grid(row=0, column=0, pady=10, padx=5, sticky=W+E)
        self.options_frame.grid(row=1, column=0)
        pass_length_label.grid(row=0, column=0)
        self.length_spinbox.grid(row=0, column=1)
        include_label.grid(row=1, column=0)

        upper_check.grid(row=1, column=1, sticky=W+E)
        num_check.grid(row=2, column=1, sticky=W+E)
        special_check.grid(row=3, column=1, sticky=W+E)

        gen_pass_btn.grid(row=4, column=1)
        back_btn.grid(row=4, column=0)

    def generate_password(self):
        # Generate the password
        length = int(self.length_spinbox.get())
        have_numbers = self.includeNumbers.get()
        have_uppercase = self.includeUpper.get()
        have_special = self.includeSpecial.get()

        self.generated_password = GeneratePassword(length, have_numbers, have_uppercase, have_special).make_password()
        
        # Remove the previous password label, if it exists
        if hasattr(self, 'password_label'):
            self.password_label.destroy()

        # Show the new password on the screen
        self.password_label = Label(self.options_frame, text=f"Password:  {self.generated_password}", font=("Arial", 10, "bold"))

        add_btn = Button(self.options_frame, text="Add Password to Account", command=self.add_window)

        self.password_label.grid(row=5, column=0, columnspan=2, pady=(5, 0))
        add_btn.grid(row=6, column=0, columnspan=2)

    def add_window(self, direct=False):
        self.clear_screen()

        # Make the window for adding passwords
        title = Label(root, text="Add Password to Account", font=("Arial", 20, "bold"), anchor=W)

        self.adding_frame = LabelFrame(root, padx=5, pady=5, bd=2)

        password_label = Label(self.adding_frame, text="Password: ")
        password_entry = Entry(self.adding_frame)
        if not direct:
            password_entry.insert(0, self.generated_password)
        service_label = Label(self.adding_frame, text="Service: ")
        service_entry = Entry(self.adding_frame)

        back_button = Button(self.adding_frame, text="Back", command=self.back)
        store_button = Button(self.adding_frame, text="Add", command=lambda: self.store_password(password_entry.get(), service_entry.get(), True))
        
        # Showing widgets on screen
        title.grid(row=0, column=0, pady=10, padx=5, sticky=W+E)
        self.adding_frame.grid(row=1, column=0)
        password_label.grid(row=0, column=0)
        password_entry.grid(row=0, column=1)
        service_label.grid(row=1, column=0, pady=5)
        service_entry.grid(row=1, column=1, pady=5)
        back_button.grid(row=2, column=0)
        store_button.grid(row=2, column=1)

    def view_password_window(self):
        self.clear_screen()

        # Make the window for viewing passwords
        title = Label(root, text="My Passwords", font=("Arial", 20, "bold"), anchor=W)

        password_frame = LabelFrame(root, padx=5, pady=5, bd=2)
        service_heading = Label(password_frame, text="Services", font=("Arial", 15, "bold"), anchor=W)
        password_heading = Label(password_frame, text="Passwords", font=("Arial", 15, "bold"), anchor=W)

        # Make a Label for all passwords
        for i in range(len(self.account_passwords)):
            Label(password_frame, text=f"{self.account_services[i]}").grid(row=i+1, column=0, pady=(0, 3))
            Label(password_frame, text=f"{str(self.fer.decrypt(self.account_passwords[i].encode()).decode())}").grid(row=i+1, column=1, pady=(0, 3))

            Button(password_frame, text="Copy", command=lambda i=i: pyperclip.copy(str(self.fer.decrypt(self.account_passwords[i].encode()).decode()))).grid(row=i+1, column=2, padx=(5, 0), pady=(0, 3))

            Button(password_frame, text="Delete", command=lambda i=i: self.delete_password(self.account_services[i], self.account_passwords[i])).grid(row=i+1, column=3, padx=(5, 0), pady=(0, 3))

        back_button = Button(root, text="Back", command=self.back)

        # Show widgets on screen
        title.grid(row=0, column=0, pady=10, padx=5, sticky=W+E)
        password_frame.grid(row=1, column=0)
        service_heading.grid(row=0, column=0, sticky=W+E)
        password_heading.grid(row=0, column=1, padx=7, sticky=W+E)
        back_button.grid(row=2, column=0, columnspan=1, pady=(5, 0))

    def store_password(self, password, service, show_label=False):
        if show_label:
            Label(self.adding_frame, text="Password successfully added to Account").grid(row=3, column=0, columnspan=2, pady=(5, 0))

        # Store the data in the JSON file
        with open(f"Passwords\{self.username}.json", "w") as f:
            self.account_passwords.append(str(self.fer.encrypt(password.encode()).decode()))
            self.account_services.append(service)
            json.dump({"services": self.account_services, "passwords": self.account_passwords}, f)

    def store_multiple_passwords(self, services, passwords, frame=False):
        if frame:
            Label(frame, text="Password successfully added to Account").grid(row=len(passwords)+1, column=0, pady=(5, 0), columnspan=2)

        # Store the data in the JSON file
        for i in range(len(passwords)):
            with open(f"Passwords\{self.username}.json", "w") as f:
                self.account_passwords.append(str(self.fer.encrypt(passwords[i].encode()).decode()))
                self.account_services.append(services[i])
                json.dump({"services": self.account_services, "passwords": self.account_passwords}, f)

    def delete_password(self, service, password):
        # Deleting the data
        response = messagebox.askyesno("", "Are you sure you wish to delete this password?")
        if response:
            self.account_services.remove(service)
            self.account_passwords.remove(password)
            self.view_password_window()
        else:
            return

    def upload_menu(self):
        self.clear_screen()

        # Make the window for uploading passwords
        title = Label(root, text="Upload JSON File", font=("Arial", 20, "bold"), anchor=W)

        self.upload_frame = LabelFrame(root, padx=5, pady=5, bd=2)
        note = Label(self.upload_frame, text="Note: The JSON file has to be in the following format. The data you want to store goes in between the speech marks.", font=("Arial", 10, "bold"))
        f_format = Label(self.upload_frame, text='{"services": [" ", " "], "passwords": [" ", " "]}', font=("Comic Sans", 11, "bold"))

        upload_button = Button(self.upload_frame, text="Upload File", command=self.upload_file)
        back_button = Button(root, text="Back", command=self.back)

        # Show widgets on screen
        title.grid(row=0, column=0, pady=10, padx=5, sticky=W+E)
        self.upload_frame.grid(row=1, column=0)
        note.grid(row=0, column=0)
        f_format.grid(row=1, column=0)
        upload_button.grid(row=2, column=0, pady=(10, 0))
        back_button.grid(row=2, column=0, pady=(10, 0))

    def upload_file(self):
        # Get the filename
        root.filename = filedialog.askopenfilename(initialdir=".", title="Select a JSON File", filetypes=[("JSON Files", "*.json")])

        # Open the file and store the data
        with open(root.filename, "r") as f:
            try:
                data = json.load(f)
                self.file_services = data["services"]
                self.file_passwords = data["passwords"]
                self.file_info_window()
            except:
                self.incorrect_format = Label(self.upload_frame, text="This file is not in the correct format.").grid(row=3, column=0)

    def file_info_window(self):
        self.clear_screen()

        # Make the window for the data uploaded from the file
        title = Label(root, text="Upload JSON File", font=("Arial", 20, "bold"), anchor=W)
        data_frame = LabelFrame(root, padx=5, pady=5, bd=2)

        service_heading = Label(data_frame, text="Services", font=("Arial", 15, "bold"), anchor=W)
        password_heading = Label(data_frame, text="Passwords", font=("Arial", 15, "bold"), anchor=W)
        
        back_button = Button(data_frame, text="Back", command=self.back)

        for i in range(len(self.file_passwords)):
            Label(data_frame, text=f"{self.file_services[i]}").grid(row=i+1, column=0, pady=(0, 3))
            Label(data_frame, text=f"{self.file_passwords[i]}").grid(row=i+1, column=1, pady=(0, 3))

        store_button = Button(data_frame, text="Add", command=lambda: self.store_multiple_passwords(self.file_services, self.file_passwords, data_frame))

        # Show widgets on screen
        title.grid(row=0, column=0, pady=10, padx=5, sticky=W+E)
        data_frame.grid(row=1, column=0)
        service_heading.grid(row=0, column=0, sticky=W+E)
        password_heading.grid(row=0, column=1, padx=7, sticky=W+E)
        store_button.grid(row=len(self.file_passwords)+2, column=1, pady=(5, 0))
        back_button.grid(row=len(self.file_passwords)+2, column=0, pady=(5, 0))

def process_login(username):
    password_manager = PasswordManager(username)

login_system = LoginSystem(root, process_login)

mainloop()