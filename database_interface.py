import mysql.connector
from mysql.connector.errors import *
from config import USER, DBPASSWORD

class DatabaseInterface():
    def __init__(self):
        # initialise the database and cursor
        self.db = mysql.connector.connect(host = 'localhost', user = USER, passwd = DBPASSWORD, database = 'airline')
        self.cursor = self.db.cursor(buffered=True)
        # create the 'users' table, if already exist then command is ignored
        try: self.cursor.execute("CREATE TABLE users (fullname VARCHAR(50), email VARCHAR(60), username VARCHAR(30), password VARCHAR(30))")
        except ProgrammingError: pass

    def create_flight_table(self, table_name):
        # create a table for a trip, initialise each seat on the plane for this trip as empty
        starting_seats = ["A1","A2","A3","A4","B1","B2","B3","B4","C1","C2","C3","C4","D1","D2","D3","D4"]
        query = f"CREATE TABLE {table_name} (seat VARCHAR(4), user VARCHAR(50))"
        self.cursor.execute(query)
        for seat in starting_seats:
            query = f"INSERT INTO {table_name} (user, seat) VALUES ('empty', '{seat}')"
            self.cursor.execute(query)
            self.db.commit()

    def insert_newuser(self, fullname, email, username, password):
        # add new user to the 'users' table
        query = f"INSERT INTO users (fullname, email, username, password) VALUES ('{fullname}', '{email}', '{username}', '{password}')"
        self.cursor.execute(query)
        self.db.commit()

    def place_booking(self, trip, seat, username):
        # changes the row with the selected seat from empty to the username for the specified trip
        query = f"UPDATE {trip} SET user='{username}' WHERE seat='{seat}'"
        self.cursor.execute(query)
        self.db.commit()

    def cancel_booking(self, trip, seat):
        # reverses the effects of the place_booking method
        query = f"UPDATE {trip} SET user='empty' WHERE seat='{seat}'"
        self.cursor.execute(query)
        self.db.commit()

    def fetch_free_seats(self, table_name):
        # finds and returns all free seats for the table (trip) in a list 
        freebies = []
        self.cursor.execute(f"SELECT seat FROM {table_name} WHERE user='empty'")
        for row in self.cursor:
            freebies.append(row[0])
        return freebies

    def delete_user(self, username, password):
        # removes the user with username from the 'users' table
        query = f"DELETE FROM users WHERE username='{username}' AND password='{password}'"
        self.cursor.execute(query)
        self.db.commit()

    def print_table(self, table_name):
        # prints the contents of a given table
        self.cursor.execute(f"SELECT * FROM {table_name}")
        for row in self.cursor:
            print(row)

    def user_exists(self, username, password):
        # returns True if the user is already in the table, False otherwise
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return len(rows)

    def username_exists(self, username):
        query = f"SELECT * FROM users WHERE username='{username}'"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return len(rows)

    def update_record(self, curr_username, settings):
        # updates the details for a given username
        data = ', '.join([f"{k}='{settings[k]}'" for k in settings.keys()])
        query = f"UPDATE users SET {data} WHERE username='{curr_username}'"
        self.cursor.execute(query)
        self.db.commit()
        
if __name__ == "__main__":
    db = DatabaseInterface()