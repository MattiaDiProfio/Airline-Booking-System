from tkinter import *

class LoginWindow(Frame):
    def __init__(self, db, func):
        super().__init__()
        self.db = db # allows database queries to be executed from this window
        self.func = func # allows data to be send to the window which invoked the current one
        self.top = Toplevel()
        self.frame = Frame(self.top)
        self.top.title("Login")
        self.top.geometry("400x180")
        self.username, self.password = StringVar(), StringVar()

        Label(self.top, text = "Fill-in the fields below with your credentials", bg='#003f88', fg='#ffffff', font = ('Calibri', 12, 'bold')).pack(pady=10)

        # frame to position window widgets
        self.f = Frame(self.top)
        self.f.pack(pady=9)
        self.f.configure(bg='#003f88')
        self.top.configure(bg='#003f88')
        
        Label(self.f, text='Username', bg='#003f88', fg='#ffffff', font=('Calibri',12,'bold')).grid(row=0, column=0, padx=5)
        Entry(self.f, textvariable=self.username).grid(row=0, column=1)
        Label(self.f, text='Password', bg='#003f88', fg='#ffffff', font=('Calibri',12,'bold')).grid(row=1, column=0, padx=5)
        Entry(self.f, textvariable=self.password, show="*").grid(row=1, column=1)
        Button(self.top, text='Submit',font=('Calibri', 12, 'bold'), width=10, fg='#003f88', activeforeground='#003f88', bg='#fdc500', activebackground='#f1a13b', relief=FLAT, command=self.send_data).pack(pady=10)

        # store the origin of the form data 
        self.form_data = {
            'origin' : 'login',
            'username' : self.username,
            'password' : self.password
        }

    def send_data(self):
        # validate user input 
        if not (username_is_valid(self.username.get()) and password_is_valid(self.password.get())):
            # if input is invalid prompt user to try again
            messagebox.showerror('Invalid input', 'Please ensure that all field entries are between 5-30 alphanumeric characters, and "Password" should contain at least 1 uppercase letter, 1 lowercase letter, 1 number, 1 special character [!@?]')
            LoginWindow(self.db, self.func) 
        else:
            self.func(self.form_data)
        self.top.destroy()
