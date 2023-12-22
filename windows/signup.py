import sys
sys.path.append('../')
from tkinter import *

class SignupWindow(Frame):
    def __init__(self, db, func):
        super().__init__()
        self.db = db # allows database queries to be executed from this window
        self.func = func # function allows to send form data back to the parent window
        self.top = Toplevel()
        self.frame = Frame(self.top)
        self.top.title("Signup")
        self.top.geometry("400x225")

        Label(self.top, text="Fill-in the fields below with your credentials", bg='#003f88', fg='#ffffff', font=('Calibri', 12, 'bold')).pack(pady=10)

        # frame used to position widgets within the window
        self.f = Frame(self.top)
        self.f.pack(pady=12)
        self.f.configure(bg='#003f88')
        self.top.configure(bg='#003f88')

        self.fullname, self.email, self.username, self.password = StringVar(), StringVar(), StringVar(), StringVar()

        Label(self.f, text='Full Name', bg='#003f88', fg='#ffffff', font=('Calibri',12,'bold')).grid(row=0, column=0, padx=5)
        Entry(self.f, textvariable=self.fullname).grid(row=0, column=1)
        Label(self.f, text='Email', bg='#003f88', fg='#ffffff', font=('Calibri',12,'bold')).grid(row=1, column=0, padx=5)
        Entry(self.f, textvariable = self.email).grid(row=1, column=1)
        Label(self.f, text='Username', bg='#003f88', fg='#ffffff', font=('Calibri',12,'bold')).grid(row=2, column=0, padx=5)
        Entry(self.f, textvariable=self.username).grid(row=2, column=1)
        Label(self.f, text='Password', bg='#003f88', fg='#ffffff', font=('Calibri',12,'bold')).grid(row=3, column=0, padx=5)
        Entry(self.f, textvariable=self.password, show="*").grid(row=3, column=1)
        Button(self.top, text='Submit', font=('Calibri', 12, 'bold'), width=10, fg='#003f88', activeforeground='#003f88', bg='#fdc500', activebackground='#f1a13b', relief=FLAT, command=self.send_data).pack(pady=10)

        # store the origin of the data to simplify logic in other windows 
        self.form_data = {
            'origin' : 'signup', 
            'fullname' : self.fullname,
            'email' : self.email,
            'username' : self.username,
            'password' : self.password
        }

    def send_data(self):
        # check that form input is valid 
        if not (fullname_is_valid(self.fullname.get()) and email_is_valid(self.email.get()) and username_is_valid(self.username.get()) and password_is_valid(self.password.get())):
            # if input invalid, display error message and prompt user to try again
            messagebox.showerror('Invalid input', 'Please ensure that all field entries are between 5-30 alphanumeric characters, and "Password" should contain 1 uppercase letter, 1 lowercase letter, 1 number, 1 special character [!@?]')
            SignupWindow(self.db, self.func) 
        else:
            # input is valid, send data back to parent window and destroy current one
            self.func(self.form_data)
        self.top.destroy()
