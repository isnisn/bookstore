import mysql.connector
class BookStore:
    
    database = "book_store"
    
    def __init__(self) -> None:
    
        ### Create a file ´config´ in the root folder with 
        ### user:password:host
        ### For example -> banana:bread:localhost

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


    # Get all titles by current subject
    def get_titles_by_subject(self, str_subject) -> list:
        q = "(select title, author, price, isbn, price from books where subject = %s)"
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
            q = ("insert into cart(userid, isbn, qty) values(%s, %s, %s)")
            self.cursor.execute(q, data)
            self.mydb.commit()

            return True
    
        except mysql.connector.Error as err:
            # print(err.errno)
            return False

    def get_cart(self, userid):
        q = "(select b.isbn, b.title, c.qty, b.price from cart c join books b on b.isbn = c.isbn where c.userid = %s)"

        self.cursor.execute(q, (userid,))
        data = self.cursor.fetchall()
        return data

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




    # def __del__(self):
    #     self.cursor.close()
    #     self.mydb.close()
