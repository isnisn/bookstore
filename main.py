import mysql.connector
from book_store import BookStore

# Instantiate new BookStore
book_store = BookStore()

# Get the subjects
subjects = book_store.get_subjects()

# Method for printing the subjects on the screen with options
def print_subjects(subjects):
    index = 0

    for subject in subjects:
        index += 1
        print(f"{index}. {subject[0]}")


def print_menu():
    pass

def main():
    print_subjects(subjects)


if __name__ == "__main__":
    main()
