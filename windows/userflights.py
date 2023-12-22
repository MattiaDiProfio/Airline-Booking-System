from tkinter import *

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
