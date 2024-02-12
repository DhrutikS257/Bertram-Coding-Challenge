import sqlite3


# creates a connection to the database and returns the cursor and connection object
def connectDB():
    connDB = sqlite3.connect('checkout_data.db')
    cursor = connDB.cursor()
    return cursor,connDB

# closes the database connection
def closeDB(connDB:sqlite3.Connection):
    connDB.close()


# returns the list of all coworkers which includes their name, amount paid and preffered coffee, and if they have paid or not
def getAllCoworkers(cursor:sqlite3.Cursor):

    cursor.execute('''
                                SELECT *
                                FROM EMPLOYEE_LIST;
                                ''')
                
    list = cursor.fetchall()

    print('\n')

    max_length = max(len(row[1]) for row in list)

    for row in list:

        print(f"Name: {row[1].ljust(max_length + 5)}Amount Paid: {str(row[2]).ljust(max_length + 5)}\tPreffered Coffee: {row[3]}\n")
    
    print("\n")


# returns the list of all coffee and their prices
def getAllCoffee(cursor:sqlite3.Cursor):
    
    cursor.execute('''
                    SELECT *
                    FROM COFFEE_LIST;
                    ''')
    
    print('\n')

    list = cursor.fetchall()

    max_length = max(len(row[0]) for row in list)
    
    for row in list:
        print(f"Name: {row[0].ljust(max_length + 5)}Price: {row[1]}\n")
    
    print('\n')

    
# returns the name of specific coffee
def listCoffee(cursor:sqlite3.Cursor):

    cursor.execute('''
                    SELECT NAME
                    FROM COFFEE_LIST;
                    ''')
    
    coffee_list = cursor.fetchall()

    return coffee_list

# inserts a new coworker into the database with their preffered coffee
def insertCoworker(cursor:sqlite3.Cursor,db:sqlite3.Connection):
    
    name = input("\nEnter the name of coworker: ")

    coffee_list = listCoffee(cursor)
    print('\n')
    for index,coffee in enumerate(coffee_list):
        print(f"{index+1}. {coffee[0]}")

    while True:
        try:
            preffered_coffee = int(input("\nChoose the coffee from above: "))

            if 1 <= preffered_coffee <= len(coffee_list):
                break
            else:
                print("\nInvalid input. Please choose a valid number from the list.")
        except ValueError:
            print("\nInvalid input. Please enter a number.")
    
    print("\n")

    cursor.execute('''
                INSERT INTO EMPLOYEE_LIST(NAME,TOTAL_PAID,PREFERRED_COFFEE,COWORKER_PAID)
                VALUES(?,?,?,?);
                ''', (name, 0.0, coffee_list[preffered_coffee-1][0], 1))

    
    db.commit()


# inserts a new coffee into the database and the respective price
def insertCoffee(cursor:sqlite3.Cursor,db:sqlite3.Connection):

    coffee_name = input("\nEnter the coffee name: ")

    cursor.execute(f'''
                    SELECT *
                    FROM COFFEE_LIST
                    WHERE NAME LIKE ?;
                    ''',(f'{coffee_name}',))
    
    row = cursor.fetchall()

    if len(row) != 0:
        print("\nThe coffee already exists\n\n")
        return
    
    while True:
        try:
            price = float(input("\nEnter the price of coffee: "))

            cursor.execute('''
                            INSERT INTO COFFEE_LIST
                            VALUES (?,?)
                            ''',(coffee_name,price))
            
            db.commit()
            return False
        except ValueError:
            print("\nInvalid input. Please enter a number.")

# returns the coworker name who is paying today
def getPayingCoworker(cursor:sqlite3.Cursor,db:sqlite3.Connection):
    
    cursor.execute('''
                    SELECT el.NAME,el.ID
                    FROM COFFEE_LIST cl, EMPLOYEE_LIST el
                    WHERE el.PREFERRED_COFFEE = cl.NAME and el.COWORKER_PAID = 0
                    ORDER BY cl.PRICE DESC
                    LIMIT 1;
                    ''')
    
    paying_coworker = cursor.fetchall()

    if len(paying_coworker) == 0:
        resetPaidPeriod(cursor,db)
        getPayingCoworker(cursor,db)

    else:
        updatePersonPaid(cursor,db,paying_coworker[0][1])

        print(f"Coworker paying today: {paying_coworker[0][0]}\n")

# resets all coworker's paid column
def resetPaidPeriod(cursor:sqlite3.Cursor,db:sqlite3.Connection):

    cursor.execute('''
                    UPDATE EMPLOYEE_LIST
                    SET COWORKER_PAID = 0;
                    ''')

    db.commit()


def updatePersonPaid(cursor:sqlite3.Cursor,db:sqlite3.Connection,id:int):

    cursor.execute(f'''
                    UPDATE EMPLOYEE_LIST
                    SET COWORKER_PAID = 1
                    WHERE ID = {id};
                    ''')
    
    db.commit()

