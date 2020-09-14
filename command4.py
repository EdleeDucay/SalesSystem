import sqlite3
import time
import datetime
import random
import string

def create_sid():
    # Random but unique sale ID generator
    nums = ''
    for _ in range(4):
        nums += random.choice(string.digits + string.ascii_letters)
    sid = nums
    return sid

def check_sid(connection, cursor, sid):
    # Returns True or false if the sid is unique
    #global connection, cursor
    cursor.execute(''' SELECT sid FROM sales;''')
    allSIDs = cursor.fetchall()
    for i in allSIDs:
        if i == sid:
            return False
    return True

def post_sale(connection, cursor, user):

    print("To post a sale, enter the product id, sale end date and time, sale description, condition, and a reserved price as prompted")
    print("To return to the main menu, enter 'return' at any point")

    while True:
        # Error check product id and store it into a variable
        while True:
            input_pid = input("Enter a product id (optional): ").lower()

            if input_pid == "return":
                return
            elif len(input_pid) == 0:
                break
            elif len(input_pid) <= 4:
                cursor.execute("SELECT pid FROM products WHERE lower(pid) = ? ;", (input_pid,))
                pid = cursor.fetchone()
                if pid is not None:
                    print("product id added")
                    break
                else:
                    print("Invalid product id, pid has incorrect format or does not exist")
            else:
                print("Invalid product id, pid has incorrect format or does not exist")
        # Error check sale end date and store it into a variable
        while True:
            input_edate = input("Enter the sale end date (YYYY-MM-DD): ").lower()
            if input_edate == "return":
                return
            try:
                temp = datetime.datetime.strptime(input_edate, '%Y-%m-%d')
                #now = datetime.datetime.today().strftime('%Y-%m-%d')
                now = datetime.datetime.now()
                if temp > now:
                    print("sale end date added")
                    break
                else:
                    print("sale end date must be in the future, try again")
            except ValueError:
                print("Incorrect date format, try again")
                
        # Error check description and store it into a variable
        while True:
            input_sdescr = input("Enter a description of the sale: ").lower()
            if input_sdescr == "return":
                return
            elif len(input_sdescr) == 0:
                print("Invalid description, try again")
            elif len(input_sdescr) <= 25:
                print("Sale description added")
                break
            else:
                print("Sale description too long, maximum 25 characters")
        # Error check condition and store it in a variable
        while True:
            input_cond = input("Enter a description of the condition: ").lower()
            if input_cond == "return":
                return
            elif len(input_cond) == 0:
                print("Invalid condition, try again")
            elif len(input_cond) <= 10:
                print("Condition added")
                break
            else:
                print("Condition too long, maximum 10 characters")
        # Error check reserved price and store it in a variable
        while True:
            input_rprice = input("Enter the reserved price (optional): ").lower()
            if input_rprice == "return":
                return
            elif len(input_rprice) == 0:
                break
            else:
                try:
                    val = int(input_rprice)
                    print("Reserved price added")
                    break
                except:
                    print("reserved price must be a numerical value, try again")
        break
    # Create unique sid for sale
    sid = create_sid()
    while True:
        if check_sid(connection, cursor, sid) == False:
            sid = create_sid()
        else:
            break
    # insert all data into sql database
    cursor.execute('''INSERT into sales values (?, ?, ?, ?, ?, ?, ?);''', 
        (sid, user[0], pid[0], input_edate, input_sdescr, input_cond, input_rprice))
    connection.commit()
    print("Sale posted successfully")
    return
