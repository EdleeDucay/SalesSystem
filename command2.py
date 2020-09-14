# Function 2 implementation
from command3 import *

def get_key_count(connection, cursor, sid, key):
    # Returns the count of keyword in either
    # Product or sale description
    cursor.execute('''
                SELECT s.descr, p.descr
                FROM sales s OUTER LEFT JOIN products p using (pid)
                WHERE s.sid = ?''', [sid])
    descrs = cursor.fetchall()[0]
    num = descrs[0].lower().count(key) + descrs[1].lower().count(key)
    return num

def convert_time(time):
    # Converts the time in seconds to Days/Hours/Minutes
    days = int(time / 86400)
    time = time % 86400
    hours = int(time / 3600)
    time = time % 3600
    minutes = int(time / 60)

    time = "{}D|{}H|{}M".format(days,hours,minutes)
    return time

def search_sales(connection, cursor, user):
    # Function 2 Entering one or more keywords the user can retrieve all sales
    # With at least one keyword in the sales/product description

    keywords = input("Enter one or more keywords using space as a separator: ")
    keys_split = keywords.split()
    total_sales = []
    sids = set()

    # Iterate through each inputted key
    for key in keys_split:
        key = key.lower()
        pkey = '%' + key + '%'
        cursor.execute('''
                    SELECT s.sid, s.descr, s.rprice, MAX(amount), 
                        (strftime('%s', edate) - strftime('%s', 'now'))
                    FROM (products p, sales s) OUTER LEFT JOIN bids b USING (sid)
                    WHERE s.pid = p.pid AND strftime(edate) >= datetime('now')
                    AND (s.descr like ? OR  p.descr like ?)
                    GROUP BY s.sid, s.descr, s.rprice;''', [pkey, pkey])   
        
        # Place each sale into a list with a corresponding key count
        sales = cursor.fetchall()
        for sale in sales:
            key_count = get_key_count(connection, cursor, sale[0], key)
            sale = sale + (key_count,)            
            total_sales.append(sale)
            sids.add(sale[0])
    # Sort by total no. of keywords
    total_sales.sort(key=lambda x: x[5], reverse=True)
    print("{:<5}|{:<25}|{:<15}|{:<15}|{:<5}".format('sid',\
        'description', 'current price', 'time remaining', 'key count'))
    for sale in total_sales:
        if sale[3] is None:
            print("{:<5}|{:<25}|{:<15}|{:<15}|{:<5}".format\
                (sale[0], sale[1], sale[2], convert_time(int(sale[4])), sale[5]))
        else:
            print("{:<5}|{:<25}|{:<15}|{:<15}|{:<5}".format\
                (sale[0], sale[1], sale[3], convert_time(int(sale[4])), sale[5]))

    select_main(connection, cursor, user, sids)
    return
