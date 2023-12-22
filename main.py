import sys
sys.path.append('../')
from tkinter import *
from tkinter import messagebox
from mysql.connector.errors import *
from tkinter import ttk
from database_interface import DatabaseInterface
import re
import time
import csv 
from graph import *

# Import utility functions
from utils import *

# Import windows
from windows.signup import SignupWindow
from windows.login import LoginWindow
from windows.settings import SettingsWindow
from windows.newbooking import NewBookingWindow
from windows.userflights import UserFlightsWindow
from windows.userdashboard import UserDashboard
from windows.home import HomeWindow

if __name__ == "__main__":
    db = DatabaseInterface()
    g = Graph()

    # Populate the network of flights using the data from csv file
    with open('available_flights.csv') as f:
        reader = list(csv.reader(f))
        for i in range(1, len(reader)):
            g.add_edge(reader[i][0], reader[i][1].lstrip())
        
    app = HomeWindow(db, g)
