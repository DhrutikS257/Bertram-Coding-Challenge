from db_operations import connectDB, insertCoworker, getAllCoworkers, closeDB, getAllCoffee



def main():
    user_input = ""

    cursor,db = connectDB()

    while user_input != "q":

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

                pass

            case "3":
                
                pass

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
