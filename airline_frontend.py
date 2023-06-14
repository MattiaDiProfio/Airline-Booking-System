from tkinter import *
from tkinter import messagebox
from mysql.connector.errors import *
from tkinter import ttk
from database_interface import DatabaseInterface
import re
import time
import csv 
from graph import *

def email_is_valid(email):
    # check whether input follows the format of a conventional email address
    pattern = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
    match = pattern.match(email)
    return True if match else False

def password_is_valid(password):
    # check whether input follows format of specified password requirements
    pattern = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!?@])[\w\d@!?]{5,30}$")
    match = pattern.match(password)
    return True if match else False

def username_is_valid(username):
    # check wheter input follows username requirements
    pattern = re.compile(r"^[a-zA-Z0-9]{5,30}$")
    match = pattern.match(username)
    return True if match else False

def fullname_is_valid(fullname):
    # check whether input follows full name requirements
    pattern = re.compile(r"^[a-zA-Z ]{5,30}$")
    match = pattern.match(fullname)
    return True if match else False

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

class NewBookingWindow(Frame):
    def __init__(self, username, db, network):
        super().__init__()
        self.username = username
        self.db = db
        self.network = network
        self.top = Toplevel()
        self.frame = Frame(self.top)
        self.top.title("New Booking")
        self.top.resizable(False, False)
        self.top.geometry("400x225")
        self.top.configure(bg='#003f88')

        Label(self.top, text = "Select departure, arrival, and seat below", bg='#003f88', fg='#ffffff', font = ('Calibri', 12, 'bold')).pack(pady=15)

        # ttk's combo box allows for dropdown functionality 
        # user can choose any city from the graph's set of vertices
        self.departure_options = self.network.get_vertices()
        self.departure_combo = ttk.Combobox(self.top, value = self.departure_options)
        self.departure_combo.current(0)
        self.departure_combo.bind("<<ComboboxSelected>>", self.update_arrival_combo)
        self.departure_combo.pack(pady=5)

        # arrival combobox contains only the vertices which can be reached from the selected starting point
        self.arrival_options = self.departure_options
        self.arrival_combo = ttk.Combobox(self.top, value = self.arrival_options)
        self.arrival_combo.current(0)
        self.arrival_combo.bind("<<ComboboxSelected>>", self.update_seat_selection)
        self.arrival_combo.config(state = DISABLED)
        self.arrival_combo.pack(pady=5)

        # seats combobox holds all free seats for the selected flight/connection
        self.seating_options = ["A1","A2","A3","A4","B1","B2","B3","B4","C1","C2","C3","C4","D1","D2","D3","D4"]
        self.seating_combo = ttk.Combobox(self.top, value = self.seating_options)
        self.seating_combo.current(0)
        self.seating_combo.bind("<<ComboboxSelected>>", self.unlock_button)
        self.seating_combo.config(state = DISABLED)
        self.seating_combo.pack(pady=5)

        self.booking_button = Button(self.top, text = 'Book',font = ('Calibri', 12, 'bold'), width=10, fg='#003f88', activeforeground='#003f88', bg='#fdc500', activebackground='#f1a13b', state=DISABLED, relief=FLAT, command = self.complete_booking)
        self.booking_button.pack(pady=10)

    def update_arrival_combo(self, event):
        # use the Graph's class all_reachables method to chnage the combobox's entries to the value returned by the graph method
        available_destinations = self.network.all_reachables(self.departure_combo.get())
        self.arrival_combo['values'] = available_destinations
        self.arrival_combo.delete(0, "end")
        self.arrival_combo.config(state = NORMAL)

    def update_seat_selection(self, event):
        # returns a list of all the seats with a corresponding 'empty' value in the table for this trip, under the 'user' column
        trip_name = f"{self.departure_combo.get()}_{self.arrival_combo.get()}" 
        freebies = []
        try:
            self.db.create_flight_table(trip_name)
        except ProgrammingError:
            pass
        freebies = self.db.fetch_free_seats(trip_name)
        self.seating_combo['values'] = freebies
        self.seating_combo.delete(0, "end")
        self.seating_combo.config(state = NORMAL)
        
    def unlock_button(self, event): 
        self.booking_button.config(state = NORMAL)

    def complete_booking(self):
        # updates the 'user' value with the username in the table for this trip
        name = f"{self.departure_combo.get()}_{self.arrival_combo.get()}"
        seat = self.seating_combo.get()
        self.db.place_booking(name, seat, self.username)
        # display an info message to the user with the details of the selected trip
        info_msg = f"Your booking for the jouney from {self.departure_combo.get()} to {self.arrival_combo.get()}, seat number {self.seating_combo.get()} has been successfully executed."
        messagebox.showinfo("Booking Successful", info_msg)
        self.top.destroy()

class UserFlightsWindow(Frame):
    def __init__(self, username, db):
        self.username = username
        self.db = db
        self.top = Toplevel()
        self.frame = Frame(self.top)   
        title = f"Bookings for {self.username}"
        self.top.title(title)
        self.top.resizable(False, False)
        self.top.configure(bg='#003f88')

        #print a list of all the tables in the DB
        self.db.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema = 'airline'")
        user_trips_tables = [x[0] for x in self.db.cursor if x[0] != 'users'] # ignore the users table
        self.user_trips = []
        # fetch all tables where the username is mentioned
        for trip in user_trips_tables:
            self.db.cursor.execute(f"SELECT seat FROM {trip} WHERE user='{self.username}'")
            for seat in self.db.cursor:
                self.user_trips.append((f"{' to '.join(list(map(lambda x: x[0].upper() + x[1:], trip.split('_'))))}", seat[0]))

        Label(self.top, text = "Select all the bookings you which to cancel", bg='#003f88', fg='#ffffff', font = ('Calibri', 12, 'bold')).pack(pady=10, padx=15)

        # frame used to position the check buttons with right-alignment
        self.f_trips = Frame(self.top)
        self.f_trips.pack(pady=5)
        self.f_trips.configure(bg='#003f88')

        # hold the values for each check button, 1 = selected, 0 = not selected
        self.check_variables = { f"{trip}" : IntVar() for trip in self.user_trips}
        if not self.user_trips:
            Label(self.top, text = "No bookings found, please place new booking", bg='#003f88', fg='#fdc500', font = ('Calibri', 12, 'bold')).pack(padx=15, pady=10)
        else:
            # display a list of all flights the user has booked
            for trip in self.user_trips:
                Checkbutton(self.f_trips, text=f"{trip[0]}, seat {trip[1]}", variable = self.check_variables[f'{trip}'], onvalue = 1, offvalue = 0, bg='#003f88', activebackground='#003f88', activeforeground='#ffffff', selectcolor='#003f88' , fg='#ffffff', font = ('Calibri', 12)).pack(anchor=W)
            Button(self.top, text="Cancel selected", font = ('Calibri', 12, 'bold'), width=15, fg='#003f88', activeforeground='#003f88', bg='#fdc500', activebackground='#f1a13b', relief=FLAT, command=self.cancel_bookings).pack(pady=15, padx=5)


    def cancel_bookings(self):
        # cancel all the bookings from the list where the user has ticked the box
        for trip in self.check_variables.items():
            if trip[1].get() == 1:
                t = trip[0].split("'")
                trip = t[1].replace(" to ", "_")
                seat = t[3]
                self.db.cancel_booking(trip, seat)

        messagebox.showinfo('Successful cancellation', 'All the selected trips have been cancelled.')
        self.top.destroy()

class UserDashboard(Frame):
    def __init__(self, username, password, network):
        super().__init__()
        self.top = Toplevel()
        self.db = db
        self.network = network # graph structure storing all routes offered
        self.frame = Frame(self.top)
        self.top.title('Dashboard')
        self.top.geometry("300x175")
        self.top.resizable(False, False)

        #hold the details for the user which is logged in currently
        self.username = username
        self.password = password

        Label(self.top, text = f'Welcome back {username}', font = ('Calibri', 15, 'bold'), fg='#ffffff', bg='#003f88').pack(pady=12)

        # frame used for positioning purposes only
        self.f_up = Frame(self.top)
        self.f_up.pack(pady=5)
        self.f_up.configure(bg='#003f88')

        # frame used for positioning purposes only
        self.f_down = Frame(self.top)
        self.f_down.pack(pady=5)
        self.f_down.configure(bg='#003f88')

        self.top.configure(bg='#003f88')

        Button(self.f_up, text = 'Settings',font = ('Calibri', 12, 'bold'), width=10, fg='#003f88', activeforeground='#003f88', bg='#fdc500', activebackground='#f1a13b', relief=FLAT, command = self.show_settings_window).pack(side=LEFT,fill= BOTH, expand= True, padx=5)
        Button(self.f_up, text = 'Book flight',font = ('Calibri', 12, 'bold'), width=10, fg='#003f88', activeforeground='#003f88', bg='#fdc500', activebackground='#f1a13b', relief=FLAT, command = self.show_newbooking_window).pack(side=RIGHT,fill= BOTH, expand= True, padx=5)
        Button(self.f_down, text = 'My flights',font = ('Calibri', 12, 'bold'), width=10, fg='#003f88', activeforeground='#003f88', bg='#fdc500', activebackground='#f1a13b', relief=FLAT, command = self.show_userflights_window).pack(side=LEFT,fill= BOTH, expand= True, padx=5)
        Button(self.f_down, text = 'Log out',font = ('Calibri', 12, 'bold'), width=10, fg='#003f88', activeforeground='#003f88', bg='#fdc500', activebackground='#f1a13b', relief=FLAT, command = self.log_out).pack(side=RIGHT,fill= BOTH, expand= True, padx=5)

    def show_settings_window(self):
        SettingsWindow(self.username, self.password, self.apply_settings, self.db)

    def show_newbooking_window(self):
        NewBookingWindow(self.username, self.db, self.network)

    def show_userflights_window(self):
        UserFlightsWindow(self.username, self.db)

    def log_out(self):
        self.top.destroy()

    def apply_settings(self, update_settings):
        # string format the settings received through the form to accomodate the Database Interface methods
        settings = {k[4:] : update_settings[k].get() for k in update_settings.keys() if update_settings[k].get() != ''}
        if settings == {}:
            pass # nothing happens
        else:
            # use the Database interface class's method to update the values of a row in the 'users' table
            self.db.update_record(self.username, settings) 
            messagebox.showinfo('Update Successfull', 'Your information has been successfully updated')

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

if __name__ == "__main__":
    db = DatabaseInterface()
    g = Graph()

    # populate the network of flights using the data from the attached csv file
    with open('available_flights.txt') as f:
        reader = list(csv.reader(f))
        for i in range(1, len(reader)):
            g.add_edge(reader[i][0], reader[i][1].lstrip())
        
    app = HomeWindow(db, g)
