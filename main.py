from os import _exit
from typing import Match
import mysql.connector
from book_store import BookStore

# Instantiate new BookStore
book_store = BookStore()
user_logged_in = False

# Get the subjects
subjects = book_store.get_subjects()

# Method for printing the subjects on the screen with options
def print_subjects(subjects):
    index = 0

    for subject in subjects:
        index += 1
        print(f"{index}. {subject[0]}")


def print_menu() -> None:
    print("******************************************") 
    print("***  Welcome to the online Book Store  ***")
    print("******************************************") 
    print()
    print("1. Member login")
    print("2. New member Registration") 
    print("q. Member login")

def get_input() -> str:
    return str(input("Enter your choice: "))

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


def main():

    print_menu()
    
    choice = get_input()

    match (choice):
        case "1":
            # Login user 
           member_login = get_member_login()
           print(member_login)
           login_status = book_store.member_login(member_login)

           # Login the user if the authentication was successful
           if login_status == False:
               print("Not logged in")
           elif login_status == True:
               print("Logged in!")
               user_logged_in = True

        case "2":
            # Collect member data
            member_data = collect_member_data()

            # Create the member 
            book_store.create_member(member_data) 
            
        case "q":
            exit()

    #print_subjects(subjects)


if __name__ == "__main__":
    main()
