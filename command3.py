# Function 3 implementation
import random
import string

def select_sale(connection, cursor, sids):
    # Show detailed information about a sale
    sid = input("Select a sale to interact with using the sid: ")
    while sid not in sids or not sids:        
        print('\nSelected sid is not in the current listing\n')
        sid = input("Select a sale to interact with using the sid: ")
        
    cursor.execute('''
                SELECT lister, COUNT(r.rating), na(AVG(r.rating)), s.descr, 
                    s.edate, s.cond, MAX(amount), s.rprice
                FROM (sales s OUTER LEFT JOIN bids USING (sid))
                OUTER LEFT JOIN reviews r ON lister = reviewee
                WHERE sid = ?
                GROUP BY lister, s.descr, s.edate, s.cond, s.rprice;''', [sid])
    sale = cursor.fetchall()

    cursor.execute('''
                SELECT p.descr, COUNT(pr.rating), na(AVG(pr.rating))
                FROM sales s OUTER LEFT JOIN products p USING (pid)
                OUTER LEFT JOIN previews pr USING (pid)
                WHERE sid = ?
                GROUP BY sid;''', [sid])
    product = cursor.fetchall()

    print('Here are the sale\'s details:')
    if not product:
        print("{:<20}|{:<10}|{:<20}|{:<25}|{:<20}|{:<10}|{:<15}".format('lister', 'rating cnt',\
            'average rating', 'description', 'expiration date', 'condition', 'current price'))
        sale = sale[0]
        if sale[0][6] == None:
            print("{:<20}|{:<10}|{:<20}|{:<25}|{:<20}|{:<10}|{:<15}".format(sale[0], sale[1],\
                sale[2], sale[3], sale[4], sale[5], sale[7]))
        else:
            print("{:<20}|{:<10}|{:<20}|{:<25}|{:<20}|{:<10}|{:<15}".format(sale[0], sale[1],\
                sale[2], sale[3], sale[4], sale[5], sale[6]))
            print(sale[:7])
    else:
        print("{:<20}|{:<10}|{:<20}|{:<25}|{:<20}|{:<10}|{:<15}|{:<20}|{:<10}|{:<15}".format(\
            'lister', 'rating cnt', 'average rating', 'sale description', \
            'expiration date', 'condition', 'current price', 'product description',\
            'prating cnt', 'average prating'))
        sale = sale[0] + product[0]
        if sale[6] == None:
            print("{:<20}|{:<10}|{:<20}|{:<25}|{:<20}|{:<10}|{:<15}|{:<20}|{:<10}|{:<15}".format(sale[0], sale[1],\
                sale[2], sale[3], sale[4], sale[5], sale[7], sale[8], sale[9], sale[10]))
        else:
            print("{:<20}|{:<10}|{:<20}|{:<25}|{:<20}|{:<10}|{:<15}|{:<20}|{:<10}|{:<15}".format(sale[0], sale[1],\
                sale[2], sale[3], sale[4], sale[5], sale[6], sale[8], sale[9], sale[10]))

    return (sid, sale[0])

def check_bids(connection, cursor, bid):
    # Returns True or False if the bid is unique
    cursor.execute('''SELECT bid FROM bids;''')
    allBIDs = cursor.fetchall()[0]
    for i in allBIDs:
        if i == bid:
            return False
    return True

def check_amount(connection, cursor, amount, sid):
    # Returns 'True' if bid amount > current max bid
    # Returns 'False' otherwise
    cursor.execute('''
                SELECT MAX(amount), rprice
                FROM sales OUTER LEFT JOIN bids using (sid)
                WHERE ? = sid
                GROUP BY sid, rprice;''', [sid])
    maxPrice = cursor.fetchall()[0]
    if not maxPrice[0]:
        return amount > maxPrice[1]
    else:
        return amount > maxPrice[0]

def create_bid():
    # Random bid ID generator
    nums = ''
    for _ in range(20):
        nums += random.choice(string.digits+string.ascii_letters)
    bid = nums 
    return bid

def place_bid(connection, cursor, sid, user):
    # Places a bid on the selected sale
    # Parameters: details on selected sale and current user
    try:
        amount = float(input('Enter a bid amount: '))
        if not check_amount(connection, cursor, amount, sid):
            print("!!!ERROR!!! Bid does not exceed current largest bid")
            return
    except:
        print('Error incorrect value inputted returning...')
        return

    bid = create_bid()
    while True:
        if check_bids(connection, cursor, bid) == False:
            bid = create_bid()
        else:
            break

    cursor.execute('INSERT INTO bids values (?,?,?, datetime("now"), ?);', \
        [bid, user[0], sid, amount])
    
    connection.commit()
    return

def list_seller_sales(connection, cursor, lister):
    # Lists all active sales of the seller

    cursor.execute('''
                SELECT *
                FROM sales
                WHERE lister = ? AND datetime(edate) > datetime('now')
                ORDER BY edate DESC;''', [lister])
    lister_sales = cursor.fetchall()
    
    if not lister_sales:
        print('No sales available')
        return
        
    print("{:<5}|{:<25}|{:<5}|{:<20}|{:<30}|{:<15}|{:<20}".format('sid', 'lister',\
        'pid', 'expiration date', 'description', 'condition', 'reserved price'))
    for sale in lister_sales:
        print("{:<5}|{:<25}|{:<5}|{:<20}|{:<30}|{:<15}|{:<20}".format(sale[0], sale[1],\
            sale[2], sale[3], sale[4], sale[5], sale[6]))

    return

def list_seller_reviews(connection, cursor, lister):
    # List all reviews of the seller

    cursor.execute('''
                SELECT *
                FROM reviews
                WHERE reviewee = ?;''', [lister])
    reviews = cursor.fetchall()
    
    if not reviews:
        print('No reviews available')
        return 

    print("{:<25}|{:<25}|{:<7}|{:<25}|{:<25}".format('reviewer', 'reviewee',\
        'rating', 'text', 'date'))
    for review in reviews:
        print("{:<25}|{:<25}|{:<7}|{:<25}|{:<25}".format(review[0], review[1],\
            review[2], review[3], review[4]))

    return

def select_main(connection, cursor, user, sids):
    # Main function for function 3
    menu = '''
=== Select an action ===
(1) Place a bid
(2) List all active sales of the seller
(3) List all reviews of the seller
(4) Select a different sale
(5) Main Menu'''

    if not sids:
        print('No listings available')
        return

    (sale_sid, lister) = select_sale(connection, cursor, sids)
    if sale_sid == False:
        return  
    num = ''
    while num != '5':
        print(menu)
        num = input('Enter an action: ')

        if num == '1':
            place_bid(connection, cursor, sale_sid, user)

        if num == '2':
            list_seller_sales(connection, cursor, lister)

        if num == '3':
            list_seller_reviews(connection, cursor, lister)
        
        if num == '4':
            sale_sid = select_sale(connection, cursor, sids)
            if sale_sid == False:
                return

    print('Returning to Main Menu...')
    return
