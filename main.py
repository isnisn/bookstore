from os import _exit
from typing import Match
import mysql.connector
from book_store import BookStore

# Instantiate new BookStore
book_store = BookStore()
user_logged_in = False
user_id = 0 

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
    print("q. Quit")


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

def print_search_menu():
    print("1. Author search") 
    print("2. Title search") 
    print("3. Go back to member menu")
 
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

def print_receipt(order_id, cart_contents, member_details):
    total_sum = 0

    print("\n\n")
    print(f"\t\t\t Invoice for order: {order_id}")
    print()
    print("\tShipping address")
    print(f"\tName: \t {member_details[0]}")
    print(f"\tAddress: {member_details[1]}")
    print(f"\t\t{member_details[2]}")
    print(f"\t\t{member_details[3]}")
    print("-"*80)

    print("ISBN\t    TITLE\t\t\t\t\t\t\t\t$\tQty\t\tTotal")
    print("-------------------------------------------------------------------------------------------------------------------")
    for row in cart_contents:
        print(f"{row[0]:<12}{row[1]:<68}${row[3]:>5}\t{row[2]:<10}\t${row[3] * row[2]:<10}")
        total_sum += (row[3] * row[2])
    print("-------------------------------------------------------------------------------------------------------------------")
    print(f"Total: ${total_sum}")
    print("-------------------------------------------------------------------------------------------------------------------") 

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
                        print(f"ISBN:\t {title[2]}")
                        print(f"Price:\t {title[3]}")
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
                
                ## Search by author or title ##
                case "2":
                    go_back = False

                    print_search_menu()
                    while(go_back is not True):

                        allowed = ["1", "2", "3"]
                        choice = get_input("Type in your option: ")
                        while(choice not in allowed):
                            choice = get_input("EPIC FAIL, Type in your option[1,2,3]: ")   

                        match(choice):
                            case "1":
                                author = get_input("Enter the exact author: ")
                                result = book_store.get_titles_by_author(author)
                                
                                print(f"Found {len(result)} books")
                                
                                i = 0
                                for title in result:
                                    print(f"Title:\t {title[0]}")
                                    print(f"Author:\t {title[1]}")
                                    print(f"ISBN:\t {title[2]}")
                                    print(f"Price:\t {title[3]}")
                                    print(f"Subject\t {title[4]}")

                                    i += 1
                                    if(i % 3 == 0):
                                        choice = get_input("Enter B to add to cart or\nN to browse 3 or\nQ for exit to menu: ")
                                        while(choice not in allowed):
                                            print(f"{choice} is not a valid option!! Please check brain-eyes relationship" )
                                            choice = get_input("Enter B to add to cart or\nN to browse 3 or\nQ for exit to menu: ")    

                                        # Get input choice for the book(s)
                                        match(choice):
                                            case "B":
                                                add_to_cart()
                                            case "N":
                                                pass# List two more
                                            case "Q":
                                                break
                                    
                            case "2":
                                allowed = ["N", "B", "Q"]
                                title = get_input("Enter part of the title: ")
                                result = book_store.get_titles_by_title(title)

                                print(f"Found {len(result)} books")
                                
                                i = 0
                                for title in result:
                                    print(f"Title:\t {title[0]}")
                                    print(f"Author:\t {title[1]}")
                                    print(f"Price:\t {title[2]}")
                                    print(f"ISBN:\t {title[3]}")
                                    print(f"Subject\t {title[4]}")
                                    print("---------------------")

                                    i += 1
                                    if(i % 3 == 0):
                                        choice = get_input("Enter B to add to cart or\nN to browse 3 or\nQ for exit to menu: ")
                                        while(choice not in allowed):
                                            print(f"{choice} is not a valid option!! Please check brain-eyes relationship" )
                                            choice = get_input("Enter B to add to cart or\nN to browse 3 or\nQ for exit to menu: ")    

                                        # Get input choice for the book(s)
                                        match(choice):
                                            case "B":
                                                add_to_cart()
                                            case "N":
                                                pass# List two more
                                            case "Q":
                                                break

                            case "3":
                                #Go back
                                go_back = True
                ## Checkout ##
                case "3":
                    order_id = 0
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
                    
                    # Do we want to checkout and pay?
                    if(get_input("Do you want to checkout? y/N").lower()) == "y":
                       #Do the checkout, we pass cart_contents so we dont have to retreive it again 
                       order_id = book_store.save_order(cart_contents, user_id)
                       print_receipt(order_id, cart_contents, book_store.get_member_details(user_id))

                    # Else just continue the program

                case "4":
                    user_logged_in = False
                    user_id = 0
                        
        else:

            # User not authenticated
            print_login_menu()
            choice = get_input()
            match (choice):
                case "1":
                   
                   # Login user 
                   member_login = get_member_login()
                   user_details = book_store.member_login(member_login)

                   while(user_details is None): 
                       print("Failed to login, try again")
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
