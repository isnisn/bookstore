from os import _exit
from typing import Match
import mysql.connector
from book_store import BookStore

# Instantiate new BookStore
book_store = BookStore()
user_logged_in = True#False
user_id = 1 

# Get the subjects
subjects = book_store.get_subjects()

# Method for printing the subjects on the screen with options
def print_subjects(subjects):
    index = 0

    for subject in subjects:
        index += 1
        print(f"{index}. {subject[0]}")


def print_login_menu() -> None:
    print("\n" * 5)
    print("******************************************") 
    print("***  Welcome to the online Book Store  ***")
    print("***          Please log in             ***") 
    print("******************************************") 
    print()
    print("1. Member login")
    print("2. New member Registration") 
    print("q. Member login")


def print_main_menu() -> None:
    print("\n" * 5)
    print("******************************************") 
    print("***  Welcome to the online Book Store  ***")
    print("******************************************") 
    print()
    print("1. Browse by subject")
    print("2. Search by Author/Title") 
    print("3. Check out")
    print("4. Logout")

def get_input(text = "Enter your choice: ") -> str:
    return str(input(text))

def get_member_login():
    member_login = []
    member_login.append(input("Enter username: "))
    member_login.append(input("Enter password: "))

    return member_login


def collect_member_data():
    member_data = []
    member_data.append(input("Enter first name: "))
    member_data.append(input("Enter last name: "))
    member_data.append(input("Enter streetaddress: "))
    member_data.append(input("Enter city: "))
    member_data.append(input("Enter zip: "))
    member_data.append(input("Enter phone: "))
    member_data.append(input("Enter email address: "))
    member_data.append(input("Password: "))

    return member_data

def add_to_cart():

    isbn = get_input("Enter ISBN: ")
    qty = get_input("Enter qty: ")
    data = (user_id, isbn, int(qty))

    if book_store.add_to_cart(data):
        print(f"\n{isbn} was successfully added to cart\n")
    else:
        print("\nSomething went horrible wrong, please check your input")

def main():

    global user_logged_in, user_id
    wanna_quit = False

    while wanna_quit is not True:
 

        # User is authenticated
        if user_logged_in:
            
            print_main_menu()
            choice = get_input()
 
            match (choice):
                # Browse by subject
                case "1":
                    index = 0;
                    subjects = book_store.get_subjects()
                    for subject in subjects: 
                        index += 1
                        print(f"{index}. {subject[0]}")
                    str_subject = subjects[int(get_input("Choice: "))-1]
                    
                    ############

                    titles = book_store.get_titles_by_subject(str_subject[0]) 
                        
                    print(f"{len(titles)} available on this subject!")

                    i = 0 
                    for title in titles:
                        print(f"Title:\t {title[0]}")
                        print(f"Author:\t {title[1]}")
                        print(f"Price:\t {title[2]}")
                        print(f"ISBN:\t {title[3]}")
                        print(f"Price:\t {title[4]}")
                        print(f"Subject\t {str_subject[0]}")
                        print("\n")
                        
                        # List two at a time
                        i += 1
                        if(i % 2 == 0):
                            choice = get_input("Enter B to add to cart or\nN to browse 2 more or\nQ for exit to menu: ")

                            # Get input choice for the book(s)
                            match(choice):
                                case "B":
                                    add_to_cart()

                                case "N":
                                    pass# List two more
                                case "Q":
                                    break
                    # print("No more books in the list, going to main menu")
                
                    ## Checkout ##
                case "3":
                    # Retrieve contents for current logged in user
                    cart_contents = book_store.get_cart(user_id)
                    total_sum = 0 
                    print("ISBN\t    TITLE\t\t\t\t\t\t\t\t$\tQty\t\tTotal")
                    print("-------------------------------------------------------------------------------------------------------------------")
                    for row in cart_contents:
                        print(f"{row[0]:<12}{row[1]:<68}${row[3]:>5}\t{row[2]:<10}\t${row[3] * row[2]:<10}")
                        total_sum += (row[3] * row[2])
                    print("-------------------------------------------------------------------------------------------------------------------")
                    print(f"Total: ${total_sum}")
                    print("-------------------------------------------------------------------------------------------------------------------") 
        else:

            # User not authenticated
            print_login_menu()
            choice = get_input()
            match (choice):
                case "1":
                    # Login user 
                   member_login = get_member_login()
                   
                   user_details = book_store.member_login(member_login)

                   # Login the user if the authentication was successful
                   if user_details[0] == member_login[1]:
                       print("Logged in!")
                       user_logged_in = True
                       user_id = user_details[1]
                   else:
                       print("Failed to login")
                    

                case "2":
                    # Collect member data
                    member_data = collect_member_data()

                    # Create the member 
                    book_store.create_member(member_data) 
                    
                case "q":
                    wanna_quit = True

        


if __name__ == "__main__":
    main()
