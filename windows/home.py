from .login import LoginWindow
from .signup import SignupWindow
from tkinter import *
from tkinter import messagebox
from .userdashboard import UserDashboard

class HomeWindow(Tk):
    def __init__(self, db, network):
        super().__init__()
        self.db = db
        self.network = network # graph structure containing all routes offered 

        self.title("Home")
        self.geometry("300x150")
        self.resizable(False, False)
        self.configure(bg='#003f88')

        # frame used to position widgets on this window
        self.buttons_frame = Frame(self)
        self.buttons_frame.configure(bg='#003f88')

        Label(self, text = 'Welcome to Python Airlines', font = ('Calibri', 15, 'bold'), fg='#ffffff', bg='#003f88').pack(pady=25)
        Button(self.buttons_frame, text = 'Login', font = ('Calibri', 12, 'bold'), width=10, fg='#003f88', activeforeground='#003f88', activebackground='#f1a13b', bg='#fdc500', relief=FLAT, command = self.prompt_login).pack(side=LEFT,fill= BOTH, expand= True, padx= 10)
        Button(self.buttons_frame, text = 'Signup', font = ('Calibri', 12, 'bold'), width=10, fg='#003f88', activeforeground='#003f88', activebackground='#f1a13b', bg='#fdc500', relief=FLAT, command = self.prompt_signup).pack(side=RIGHT,fill= BOTH, expand= True, padx= 10)
        self.buttons_frame.pack()

        self.mainloop()

    def prompt_login(self):
        LoginWindow(self.db, self.get_form_data)
    
    def prompt_signup(self):
        SignupWindow(self.db, self.get_form_data)

    def get_form_data(self, form_data):
        # format the data received from the 'bridge' function passed as an argument to the signup or login window
        data = {}
        for key in form_data:
            if type(form_data[key]) == str:
                data[key] = form_data[key]
            else:
                data[key] = form_data[key].get()

        user_exists = self.db.user_exists(data['username'], data['password'])
        if data['origin'] == 'login' and user_exists == 1:
            #user has an account and they successfully logged in
            messagebox.showinfo('Login Successfull', 'Click "ok" to proceed to your dashboard')
            UserDashboard(data['username'], data['password'], self.network)

        elif data['origin'] == 'login' and user_exists == 0:
            #user doesnt have an account or they dont have the right credentials and they are trying to login
            response = messagebox.askretrycancel('Invalid Credentials', 'Retry login? Clicking "cancel" will direct you to the signup page')
            if response:
                LoginWindow(self.db, self.get_form_data)
            else:
                SignupWindow(self.db, self.get_form_data)

        elif data['origin'] == 'signup' and user_exists == 1:
            #user has an account but they are trying to sign up, direct them to login page
            messagebox.showwarning('Account Exists', 'Looks like you already have an account.')
            LoginWindow(self.db, self.get_form_data)

        else:
            #user signups up with new account
            self.db.insert_newuser(data['fullname'], data['email'], data['username'], data['password'])
            messagebox.showinfo('Signup Successfull', 'Click "ok" to proceed to your dashboard')
            UserDashboard(data['username'], data['password'], self.network)
