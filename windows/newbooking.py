from tkinter import *

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
