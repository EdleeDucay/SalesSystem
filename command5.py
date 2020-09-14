import sqlite3
import datetime
import random
import string
import time

def search_users(connection, cursor, user):
    # Function 5 entering a keyword that will retrieve all user profiles that match
    # the keyword either in name or email

    while True:
        keyword = input("Enter a keyword to search for a user: ")
        cursor.execute('''SELECT lower(email) as email, name, city FROM users
                        WHERE email like ?
                        OR name like ? ;''', ('%'+keyword+'%', '%'+keyword+'%',))
        search = cursor.fetchall()
        if not search:
            print("0 matches found")
            return

        print("Keyword search results:")
        col_names = [name[0] for name in cursor.description]
        print("{:<20}|{:<16}|{:<15}".format(col_names[0], col_names[1], col_names[2]))
        for result in search:
            print("{:<20}|{:<16}|{:<15}".format(result[0], result[1], result[2]))

        on = True
        while on:
            email = input("Select the user by entering the email of the desired user: ").lower()
            if email == "return":
                return
            elif len(email) > 0:
                for item in search:
                    if item[0] == email:
                        on = False
                        break
                if on == True:
                    print("email does not exist in the list, try again")
            else:
                print("The email you have entered does not exist in the search criteria you provided")

        print(email + " has been selected")
        menu = '''=== Enter one of the commands below ===
(1) Write a review
(2) List all active listings of the selected user
(3) List all reviews of the selected user
(4) Return the main menu
            '''
        while True:
            print(menu)
            i = input("Enter action: ")
            if i == "1":
                write_review(connection, cursor, email, user)
            elif i == "2":
                list_user_sales(connection, cursor, email)
            elif i == "3":
                list_user_reviews(connection, cursor, email)
            elif i == "4":
                return
            elif i:
                print("Invalid command, try again")



        #temp = cursor.fetchone()
        #print(temp)

def write_review(connection, cursor, email, user):

    print("To post a review you must write a review and provide a rating (between 1 and 5 inclusive")
    print("The review cannot be longer than 20 characters")
    while True:
        while True:
            review = input("Review: ")
            if len(review) > 20:
                print("you have surpassed the character limit, try again")
            elif len(review) == 0:
                print("Review is empty, please try again, or enter 'return' if you wish to return to previous menu")
            elif review == "return":
                return
            else:
                break
        while True:
            rating = input("Rating (1 to 5): ")
            if rating == "return":
                return
            elif len(rating) == 0:
                print("Invalid rating, try again")
            else:
                try:
                    val = float(rating)
                    if (val >= 1) and (val <= 5):
                        print("Rating added")
                        break
                    else:
                        print("Rating must be a numerical value between 1 and 5 inclusive")
                except:
                    print("Rating must be a numerical value between 1 and 5 inclusive")

        cursor.execute("INSERT OR REPLACE into reviews VALUES (?, ?, ?, ?, datetime('now'));", 
            (user[0], email, val, review))
        connection.commit()
        print("Your review has been added")
        return

def list_user_sales(connection, cursor, email):
    #Lists all active sales of the selected user
    cursor.execute("SELECT * FROM sales where lister = ? AND edate > datetime('now') ORDER BY edate DESC;", (email,))
    active_sales = cursor.fetchall()

    col_names = [name[0] for name in cursor.description]
    print("{:<4}|{:<20}|{:<4}|{:<20}|{:<25}|{:<20}|{:<20}".format(col_names[0], col_names[1], col_names[2], col_names[3], col_names[4], col_names[5], col_names[6]))
    if not active_sales:
        print('No sales available')
        return

    for sale in active_sales:
        print("{:<4}|{:<20}|{:<4}|{:<20}|{:<25}|{:<20}|{:<20}".format(sale[0], sale[1], sale[2], sale[3], sale[4], sale[5], sale[6]))

    return

def list_user_reviews(connection, cursor, email):
    #List all reviews of the selected user
    cursor.execute("SELECT * FROM reviews WHERE reviewee = ?;", (email,))
    reviews = cursor.fetchall()
    col_names = [name[0] for name in cursor.description]
    print("{:<20}|{:<20}|{:<20}|{:<20}|{:<20}".format(col_names[0], col_names[1], col_names[2], col_names[3], col_names[4]))
    if not reviews:
        print("No reviews available")
        return

    for review in reviews:
        print("{:<20}|{:<20}|{:<20}|{:<20}|{:<20}".format(review[0], review[1], review[2], review[3], review[4]))

    return
