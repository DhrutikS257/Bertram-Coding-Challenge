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

    for row in list:

        print(row,'\n')
    
    print("\n")


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



def main():
    user_input = ""

    cursor,db = connectDB()

    while user_input != "q":

        print("Press 1 to insert a coworker.")

        print("Press 2 to get the coworker paying today.")

        print("Press 3 to get the list of coworkers.")

        print("Press q to exit.\n")

        user_input = input("Choose an option: ")

        match user_input:

            case "1":

                insertCoworker(cursor,db)

            case "2":
                
                pass

            case "3":

                getAllCoworkers(cursor)

            case "q":

                closeDB(db)
                exit(1)

            case _:

                print("\nInvalid option\n")


if __name__=="__main__": 
	main() 
