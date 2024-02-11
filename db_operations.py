import sqlite3

def connectDB():
    connDB = sqlite3.connect('checkout_data.db')
    cursor = connDB.cursor()
    return cursor,connDB


def closeDB(connDB:sqlite3.Connection):
    connDB.close()


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

def listCoffee(cursor:sqlite3.Cursor):

    cursor.execute('''
                    SELECT NAME
                    FROM COFFEE_LIST;
                    ''')
    
    coffee_list = cursor.fetchall()

    return coffee_list


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


    cursor.execute('''
                INSERT INTO EMPLOYEE_LIST(NAME,TOTAL_PAID,PREFERRED_COFFEE,EMPLOYEE_PROBABILITY)
                VALUES(?,?,?,?);
                ''', (name, 0.0, coffee_list[preffered_coffee-1][0], 1))

    
    db.commit()



