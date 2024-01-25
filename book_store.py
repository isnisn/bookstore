############################################
# BookStore, author an224qi@student.lnu.se #
############################################
import mysql.connector
class BookStore:
    
    database = "book_store"
    
    def __init__(self) -> None:
    
        ### Create a file ´config´ in the root folder with 
        ### user:password:host
        ### For example -> dbuser:dbpassword:localhost

        with open("config", "r") as file:
            values = file.readline().split(":")
            self.user = values[0]
            self.password = values[1]
            self.host = values[2]
            
        self.mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password
        )
        
        self.cursor = self.mydb.cursor()
        self.cursor.execute(f"USE {self.database}") 


    # Get all titles by author
    def get_titles_by_author(self, author):
        q = "(SELECT title, author, price, isbn, subject FROM books WHERE author = %s)"
        self.cursor.execute(q, (author,))
        lst = self.cursor.fetchall()
        return lst

    
    # Get all titles by title
    def get_titles_by_title(self, title):
        q = "(SELECT title, author, price, isbn, subject FROM books WHERE title LIKE CONCAT('%', %s, '%'))"
        self.cursor.execute(q, (title,))
        lst = self.cursor.fetchall()
        return lst
    

    # Get all titles by current subject
    def get_titles_by_subject(self, str_subject):
        q = "(SELECT title, author, isbn, price, subject FROM books WHERE subject = %s)"
        self.cursor.execute(q, (str_subject,))
        lst = self.cursor.fetchall()
        return lst


    # Get all subjects available
    def get_subjects(self):
        q = "(SELECT subject FROM books GROUP BY subject ORDER BY subject)"
        self.cursor.execute(q)
        return [x for x in self.cursor.fetchall()]


    # Add item to cart
    def add_to_cart(self, data):
        try:
            q = ("INSERT INTO cart(userid, isbn, qty) VALUES(%s, %s, %s)")
            self.cursor.execute(q, data)
            self.mydb.commit()

            return True
    
        except mysql.connector.Error as err:
            return False


    # Save the order to the database
    def save_order(self, cart_data, userid):
        # First we create the order and save the order_id
        q = ("INSERT INTO orders(userid, created, shipAddress, shipCity, shipZip)" 
              + " SELECT 1, CURDATE(), address, city, zip FROM members WHERE userid = %s")
        self.cursor.execute(q, (userid,))  
        self.mydb.commit()
        orderid = self.cursor._last_insert_id

        # Now we insert the individual rows from cart_data 
        for row in cart_data:
            q = ("INSERT INTO odetails(ono, isbn, qty, amount) "
                 + "VALUES(%s, %s, %s, %s)")
            self.cursor.execute(q, (orderid, row[0], row[2], row[3])) 
        self.mydb.commit()
        
        # All went well return data for receipt.
        return orderid


    def clear_cart(self, userid):
        q = ("DELETE FROM cart WHERE userid = %s")
        self.cursor.execute(q, (userid,))
        self.mydb.commit()


    # Get the entire cart for one user
    def get_cart(self, userid):
        q = "(SELECT b.isbn, b.title, c.qty, b.price FROM cart c JOIN books b ON b.isbn = c.isbn WHERE c.userid = %s)"

        self.cursor.execute(q, (userid,))
        data = self.cursor.fetchall()
        return data


    # Get all memberdetails for a specific user(without password)
    def get_member_details(self, userid):
        q = "(SELECT concat(fname, ' ', lname), address, city, zip FROM members WHERE userid = %s)"
        self.cursor.execute(q, (userid,))
        return [x for x in self.cursor.fetchone()]


    # Creates a member in database
    def create_member(self, member_data):
        q = ("INSERT INTO members(fname, lname, address, city, zip, phone, email, `password`) "
        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)")

        self.cursor.execute(q, member_data)
        self.mydb.commit() 
        

    # Returns member login data
    def member_login(self, member_login):

        q = "(SELECT password, userid FROM members WHERE email = %s)"
        self.cursor.execute(q, (member_login[0],))
        return self.cursor.fetchone()


