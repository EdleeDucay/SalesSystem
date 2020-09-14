import re
from command2 import *
from command3 import *

def make_rid(connection, cursor):
    
    cursor.execute("SELECT rid FROM previews ORDER BY rid DESC")
    rid = cursor.fetchone()[0]
    connection.commit()
    if rid is None:
         return 1
    return rid+1

def rate(connection, cursor, user, product):

    print("To review the selected product, enter the review and rating as prompted and it will be saved to the database")
    print("To return to the product selection, enter 'return' at any point")
    while True:
        review = input("Enter review (<=20 characters): ")
        if review == "return":
            return
        elif not review:
            print("Review is empty, please enter something for the reivew. Try again")
        elif len(review) > 20:
            print("Review is to long, make it at most 20 characters. Try again")
        else:
            break       
    while True:
        rating = input("Enter rating (Single digit, 1-5): ")
        if rating == "return":
            return
        elif rating:
            try: 
                val = float(rating)
                if val >= 1 and val <=5:
                    break
            except:
                print("Invalid rating. Try again")
    data = (make_rid(connection, cursor), product, user[0], val, review)
    cursor.execute("INSERT INTO previews VALUES(?,?,?,?,?, datetime('now'));", data)
    connection.commit()
    print("Review added")
    return

def reviews(connection, cursor, product):
    print("The reviews for " + product + " are:") 
    cursor.execute("SELECT * FROM previews WHERE pid = ?;", (product,))
    col_names = [name[0] for name in cursor.description]
    print("{:<10}|{:<5}|{:<25}|{:<8}|{:<25}|{:<20}".format(col_names[0], col_names[1], col_names[2], col_names[3], col_names[4], col_names[5]))
    for review in cursor.fetchall():
        print("{:<10}|{:<5}|{:<25}|{:<8}|{:<25}|{:<20}".format(review[0], review[1], review[2], review[3], review[4], review[5]))
    connection.commit()
    return

def product_sales(connection, cursor, user, product):
    sids = []
    print("The sales for " + product + " are:")
    cursor.execute('''
                    SELECT s.sid, s.descr, s.rprice, MAX(amount) AS rprice_or_max_bid, (strftime('%s', edate) - strftime('%s', 'now')) AS time_left
                    FROM (products p, sales s) OUTER LEFT JOIN bids b USING(sid)
                    WHERE p.pid = s.pid AND datetime(edate) >= datetime('now') AND p.pid = ?
                    GROUP BY s.sid, s.descr, s.rprice
                    ORDER BY (JulianDay(edate) - JulianDay("now"));''', (product,))
    col_names = [name[0] for name in cursor.description]
    print("{:<5}|{:<30}|{:<20}|{:<15}".format(col_names[0], col_names[1], col_names[3], col_names[4]))
    for sale in cursor.fetchall():
        sids.append(sale[0])
        if sale[3] is None:
            print("{:<5}|{:<30}|{:<20}|{:<15}".format(sale[0], sale[1], sale[2], convert_time(int(sale[4]))))
        else:
            print("{:<5}|{:<30}|{:<20}|{:<15}".format(sale[0], sale[1], sale[3], convert_time(int(sale[4]))))
    connection.commit()
    select_main(connection, cursor, user, sids)
    return 

def products(connection, cursor, user):
    while True:
        pids = []
        print("The products with active sales are: ")
        cursor.execute('''
                    SELECT p.pid, p.descr, COUNT(DISTINCT rid) AS total_reviews, na(AVG(rating)) AS avg_rating, COUNT(DISTINCT sid) AS total_sales 
                    FROM products p OUTER LEFT JOIN previews r USING (pid), sales s
                    WHERE p.pid = s.pid AND datetime(edate) >= datetime('now')
                    GROUP BY p.pid, p.descr
                    ORDER BY COUNT(sid) DESC;''')
        col_names = [name[0] for name in cursor.description]
        print("{:<5}|{:<25}|{:<15}|{:<20}|{:<15}".format(col_names[0], col_names[1], col_names[2], col_names[3], col_names[4]))
        for product in cursor.fetchall():
            pids.append(product[0])
            print("{:<5}|{:<25}|{:<15}|{:<20}|{:<15}".format(product[0], product[1], product[2], product[3], product[4]))
        connection.commit()
        print('''You may: 
 Enter the pid of a product to perform actions with it
 or 'return' to main menu''')
        while True:
            product = input("Enter pid: ")
            found = False
            for p in pids:
                if p.lower() == product.lower():
                    found = True
                    product = p
                    break
            if found:
                print("Product selected: ")
                print("Pid: " + product)
                break
            elif product == "return":
                return
            elif product:
                print("Invalid pid provided. Try again.")

        menu = '''With the selected product, you may:
(1) Rate the product
(2) View the product's reviews
(3) View the product's sales
(4) Reselect product
(5) Return to main menu '''
        while True:
            print(menu)
            i = input("Enter action: ")
            if i == "1":
                rate(connection, cursor, user, product)
            elif i == "2":
                reviews(connection, cursor, product)
            elif i == "3":
                product_sales(connection, cursor, user, product)
                return
            elif i == "4":
                break
            elif i == "5":
                return
            elif i:
                print("Invalid command. Try again")
