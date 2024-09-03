import mysql.connector
from backend.dbSettings import database_name, db_host, db_password, db_user


# Database class
class supplierdb:
    def __init__(self):
        # Creating Connection
        self.connection = mysql.connector.connect(
            user=db_user,
            host=db_host,
            password = db_password,
            database=database_name
        )
        
        self.cursor = self.connection.cursor()
        
    # Login Check
    def login_authenticationSu(self,admin_email, admin_password):
        role = "Supplier"
        query = """
            SELECT * FROM users
            WHERE email = %s AND password = %s AND role = %s
        """
        values = (admin_email, admin_password, role)
        try:
            self.cursor.execute(query, values)
            self.connection.close()
            return 1
        except:
            return 0
        
        
    # Create Account
    def accountCreationSu(self, email, password, name):
        role = "Supplier"
        query = "INSERT INTO users(email,password, name, role) VALUES(%s, %s, %s, %s)"
        values = (email, password, name, role)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            self.connection.close()
            return 1
        except:
            return 0

me = supplierdb()
me.accountCreationSu("james254@gmail.com", "123456", "james Munyasia")
