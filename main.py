from db_operations import connectDB, insertCoworker, getAllCoworkers, closeDB, getAllCoffee, insertCoffee,getPayingCoworker



def main():
    user_input = ""

    cursor,db = connectDB()
    print("\n")
    while user_input != "6":

        print("1. Insert a coworker.")

        print("2. Insert a coffee.")

        print("3. Get the coworker paying today.")

        print("4. List of coworkers.")

        print("5. List of coffee.")

        print("6. Exit.\n")

        user_input = input("Choose an option: ")

        match user_input:

            case "1":

                insertCoworker(cursor,db)

            case "2":

                insertCoffee(cursor,db)

            case "3":
                getPayingCoworker(cursor,db)

            case "4":

                getAllCoworkers(cursor)

            case "5":

                getAllCoffee(cursor)

            case "6":

                closeDB(db)
                exit(1)

            case _:
                print("\nInvalid option\n")


if __name__=="__main__": 
	main() 
