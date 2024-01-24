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

    # def __del__(self):
    #     self.cursor.close()
    #     self.mydb.close()
