
## Introduction

This project aims to implement a simple reservation system for a fictional airline company. While it was an option to build a web-based version of this project I went for a desktop-based approach, inspired by one of the projects from one of my university courses which revolved around Java Swing.

Some of the features and functionalities included are:
- creation / deletion of an account as well as login
- input validation using mySQL and regex
- supported update of user information
- place booking / cancel booking for a specific flight
- storage of all trips booked by a specific user

### Components

- The UI has been implemented using a class-based approach, with the aim of keeping the code more concise and structured as well as allowing for easier sharing of information and creation/deletion of windows
- A directed, unweighted graph class has been used to represent the network of available flights offered by the company
- A Database Interface class was developed to keep all the database-related code in one file, and also by choosing a class-based implementation passing the instance of the interface between windows was much smoother

## Requirements

In order to make this project run on your machine, you will need to install a couple of things first if you don't have them already.
- The database operations are executed using **MySQL Database** and the Python **mysql** module.
- The GUI is implemented using **Python Tkinter** and all of its associated submodules, imported at the top of the **airline_frontend** file.

## Credits & Reflections

Both the frontend and the backend for this project have been designed and implemented by myself. Altough the idea of a GUI-based management system is fairly popular, I found it as a great opportunity to explore and build using a new framework (Tkinter), as well as getting more practice working with different technologies at once.
