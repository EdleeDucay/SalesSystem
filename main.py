import sqlite3
import time
import hashlib
import re
import math
import os.path
import datetime
import random
import string
from getpass import getpass
from command1 import *
from command2 import *
from command4 import *
from command5 import *


connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return

def sql_file(filename):
    global connection, cursor
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    cursor.executescript(sqlFile)
    connection.commit()

def none_na(none):
    if none is None:
       return "NA"
    return none

def string_check(string):
    return string.lower()

def signup():
    global connection, cursor

    print("To signup, enter the information as prompted and a profile will be created for you in the database")
    print("To return to the main menu, enter 'return' at any point")
    while True:
        email = input("Enter email: ")
        if email.lower() == "return":
            return
        elif re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            cursor.execute("SELECT * FROM users WHERE email = ? ;", (email, ))
            if cursor.fetchone() is None:
                break
            else:
                print("Email is present in the database, try returning and logging in")
        elif email:
            print("Invalid email format. Try again")
    while True:
        name = input("Enter name: ")
        if name.lower() == "return":
            return
        elif re.match("^\w{1,16}$", name):
            break
        elif email:
            print("Invalid name format (Limit of 16 word characters). Try again")
    while True:
        city = input("Enter city: ")
        if city.lower() == "return":
            return
        elif re.match("^[a-zA-Z-]{1,15}$", city):
            break
        elif city:
            print("Invalid city (Limit of 15 alphabetical characters). Try again")
    while True:
        gender = input("Enter gender('M' = male,'F' = female): ").lower()
        if gender == "return":
            return
        elif gender == "m" or gender == "f":
            break
        elif gender:
            print("Invalid gender. Try again")
    while True:
        password = getpass("Enter password: ")
        if password.lower() == "return":
            return
        elif re.match("^[a-zA-Z0-9_./',;:?!]{1,4}$", password):
            break
        elif password:
            print("Invalid password format (Limit of 4 alpha numeric characters or (_./',;?!)). Try again")
    
    data = (email, name, password, city, gender)
    cursor.execute("INSERT INTO users VALUES(?,?,?,?,?);", data)
    connection.commit()
    print("Signup complete")
    actions(data)
    return

def actions(user):
    global connection, cursor

    print("Welcome " + user[0] + " you can now access the database")
    menu = '''=== Enter one of the commands below ===
(1) List products
(2) Search for sales
(3) Post a sale
(4) Search for users
(5) Logout
(6) Help'''

    while True:
        print(menu)
        i = input("Enter action: ")
        if i == "1":
            products(connection, cursor, user)
        elif i == "2":
            search_sales(connection, cursor, user)
        elif i == "3":
            post_sale(connection, cursor, user)
        elif i == "4":
            search_users(connection, cursor, user)
        elif i == "5":
            print('Logging Out...')
            return
        elif i == "6":
            print("Your options are:")
            print("'list products' - View products in database and perform actions with them")
            print("'search for sales' - View sales in database and perform actions with them")
            print("'post a sale' - Add a sale to the database")
            print("'search for users' - View users in database and perform actions with them")
            print("'logout' - Logout and return to menu")
        elif i:
            print("Invalid command. Try 'help'")
        
def login():
    global connection, cursor
    
    print("To login, enter your email and password as prompted")
    print("To return to the main menu, enter 'return' at any point")
    while True:
        while True:
            email = input("Enter email: ")
            if email == "return":
                return
            elif re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                break
            elif email:
                print("Invalid email format. Try again")
        while True:
            password = getpass("Enter password: ")
            if password == "return":
                return
            elif re.match("^[a-zA-Z0-9_./',;:?!]{1,4}$", password):
                break
            elif password:
                print("Invalid password format (Limit of 4 alpha numeric characters or (_./',;?!)). Try again")
        cursor.execute("SELECT * FROM users WHERE email = ? and pwd = ? ;", (email, password))
        user = cursor.fetchone()
        if user is not None:
            print("Successful login")
            actions(user)
            return
        else:

            print("User does not exist or password incorrect, try again or sign up instead")


def main():
    global connection, cursor
    
    print("Welcome to Project 1, all commands should be typed into the terminal when prompted")
    print("Please enter a database to work with (eg. 'dbname.db') \nor enter 'new' to work with a fresh database with some test data (name: 'project1.db')")
    while True:
        i = input("Enter name: ")
        if i.lower() == "new":
            path="./project1.db"
            connect(path)
            sql_file("tables.sql")
            sql_file("test-data.sql")
            break
        elif i:
            if os.path.isfile(i):
                path = "./" + i
                connect(path)
                break
            else:
                print ("DB does not exist")
            
    
    connection.create_function("na", 1, none_na)
    connection.create_function("lower", 1, string_check)
    print("Database login/signup")
    menu = '''You may: 
(1) Sign up as a user for the database
(2) Login as a existing user in the database
(3) Exit the application'''
    
    while True:
        print(menu)
        i = input("Enter action: ")
        if i == "1":
            signup()
        elif i == "2":
            login()
        elif i == "3":
            break
        elif i:
            print("Invalid command. Try again")


    connection.commit()
    connection.close()
    return

if __name__ == "__main__":
    main()
