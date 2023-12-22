from tkinter import *

class SettingsWindow(Frame):
    def __init__(self, username, password, func, db):
        super().__init__()
        self.func = func
        self.top = Toplevel()
        self.frame = Frame(self.top)
        self.top.title("Settings")
        self.db = db
        self.username = username
        self.password = password

        self.new_username, self.new_email, self.new_password = StringVar(), StringVar(), StringVar()

        self.settings_updates = {
            'new_email' : self.new_email,
            'new_username' : self.new_username,
            'new_password' : self.new_password
        }
        
        Label(self.top, text="Replace your credentials by filling-in the fields below", bg='#003f88', fg='#ffffff', font=('Calibri',12,'bold')).pack(pady=15)
        # frame used to position widgets on window, allows for the use of both 'grid' and 'pack' layout managers
        self.f_entries = Frame(self.top)
        self.f_entries.pack(pady=5)
        self.f_entries.configure(bg='#003f88')
        self.top.configure(bg='#003f88')
        self.top.geometry("400x225")
        self.top.resizable(False, False)

        Label(self.f_entries, text='New email', bg='#003f88', fg='#ffffff', font=('Calibri',12,'bold')).grid(row=0, column=0, padx=5)
        Entry(self.f_entries, textvariable=self.new_email).grid(row=0, column=1)
        Label(self.f_entries, text='New username', bg='#003f88', fg='#ffffff', font=('Calibri',12,'bold')).grid(row=1, column=0, padx=5)
        Entry(self.f_entries, textvariable=self.new_username).grid(row=1, column=1)
        Label(self.f_entries, text='New password', bg='#003f88', fg='#ffffff', font=('Calibri',12,'bold')).grid(row=2, column=0, padx=5)
        Entry(self.f_entries, textvariable=self.new_password, show="*").grid(row=2, column=1)

        # frame used to position the buttons for this window
        self.f_buttons = Frame(self.top)
        self.f_buttons.pack(pady=12)
        self.f_buttons.configure(bg='#003f88')
        self.top.configure(bg='#003f88')

        Button(self.f_buttons, text="Apply changes", font=('Calibri',12,'bold'), width=15, fg='#003f88', activeforeground='#003f88', bg='#fdc500', activebackground='#f1a13b', relief=FLAT, command=self.send_data).pack(side=LEFT, fill=BOTH, expand=TRUE, padx=5)
        Button(self.f_buttons, text="Delete account", font=('Calibri',12,'bold'), width=15, fg='#003f88', activeforeground='#003f88', bg='#fdc500', activebackground='#f1a13b', relief=FLAT, command=self.delete_account).pack(side=RIGHT, fill=BOTH, expand=TRUE, padx=5)

    def send_data(self):
        # check whether form input is valid and new username is not already used by someone else
        if self.settings_updates['new_email'].get() and not email_is_valid(self.settings_updates['new_email'].get()):
            messagebox.showerror('Invalid email', 'Please ensure that the email is in the correct format following "username@domainname.extension"')
            SettingsWindow(self.func, self.db)
        if self.settings_updates['new_username'].get() and (not username_is_valid(self.settings_updates['new_username'].get()) or self.db.username_exists(self.settings_updates['new_username'].get())):
            messagebox.showerror('Invalid username', 'Please ensure that the username is between 5-30 alphanumeric characters, othewise the userame chosen is already in use.')
            SettingsWindow(self.func, self.db)
        if self.settings_updates['new_password'].get() and not password_is_valid(self.settings_updates['new_password'].get()):
            messagebox.showerror('Invalid password', 'Please ensure that the password contains at least 1 uppercase letter, 1 lowercase letter, 1 number, 1 special character [!@?]')
            SettingsWindow(self.func, self.db)

        self.func(self.settings_updates)
        self.top.destroy()

    def delete_account(self):
        # add barrier against accidental clicks by asking user through prompt 
        check = messagebox.askyesno('Account Deletion', 'You are about to delete your account, are you sure?')
        if check:
            #delete this user's bookings from the database
            self.db.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema = 'airline'")
            user_trips_tables = [x[0] for x in self.db.cursor if x[0] != 'users']
            self.user_trips = []
            for trip in user_trips_tables:
                self.db.cursor.execute(f"SELECT seat FROM {trip} WHERE user='{self.username}'")
                for seat in self.db.cursor:
                    self.user_trips.append((trip, seat[0]))

            for trip in self.user_trips:
                trip_name, seat = trip[0], trip[1]
                self.db.cancel_booking(trip_name, seat)
            
            # delete user from the 'users' table
            self.db.delete_user(self.username, self.password)
            messagebox.showinfo('Account Deletion Successfull', 'Your account has been deleted.')
            self.quit()
