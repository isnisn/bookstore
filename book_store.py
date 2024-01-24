import mysql.connector
class BookStore:
    
    cursor = 0
    mydb = 0
    database = "book_store"

    user = "root"
    password = "EKDXc5aP"
    host = "localhost"
    
    def __init__(self) -> None:
    
        ### CREATE A file ´config´ in the root folder with 
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


    def get_subjects(self) -> tuple:
        q = "(SELECT subject FROM books GROUP BY subject)"
        self.cursor.execute(q)
        return [subject for subject in self.cursor.fetchall()] 


    def create_member(self, member_data):
        q = ("INSERT INTO members(fname, lname, address, city, zip, phone, email, `password`) "
        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)")

        self.cursor.execute(q, member_data)
        self.mydb.commit() 
        

    def member_login(self, member_login) -> bool:

        q = "(SELECT password FROM members WHERE email = %s)"
        self.cursor.execute(q, (member_login[0],))

        _data = self.cursor.fetchone()

        if _data is not None:
            if _data[0] == member_login[1]:
                return True

        return False




    # def __del__(self):
    #     self.cursor.close()
    #     self.mydb.close()
