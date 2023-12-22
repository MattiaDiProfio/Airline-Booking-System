from tkinter import *

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
