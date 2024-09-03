import mysql.connector
from backend.dbSettings import database_name, db_host, db_password, db_user


# Database class
class admindb:
    def __init__(self):
        # Creating Connection
        self.connection = mysql.connector.connect(
            user=db_user,
            host=db_host,
            password=db_password,
            database=database_name
        )

        self.cursor = self.connection.cursor()

    # Login Check
    def login_authenticationA(self, admin_email, admin_password):
        self.__init__()
        role = "Admin"
        query = """
            SELECT * FROM users
            WHERE email = %s AND password = %s AND role = %s
        """
        values = (admin_email, admin_password, role)
        try:
            self.cursor.execute(query, values)
            user = self.cursor.fetchone()
            if user:
                return 1
            else:
                return 0
        except:
            return 0

    # Create Account
    def accountCreationA(self, email, password, name):
        self.__init__()
        role = "Admin"
        query = "INSERT INTO users(email,password, name, role) VALUES(%s, %s, %s, %s)"
        values = (email, password, name, role)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            self.connection.close()
            return 1
        except:
            return 0

    # Get Name
    def getNameA(self, admin_email, admin_password):
        self.__init__()
        role = "Admin"
        query = """
            SELECT name FROM users
            WHERE email = %s AND password = %s AND role = %s
        """
        values = (admin_email, admin_password, role)
        try:
            self.cursor.execute(query, values)
            user = self.cursor.fetchone()
            if user:
                self.connection.close()
                return user[0]
            else:
                return 0
        except:
            return 0

    # Create supplier
    def createSupplierA(self, supplier_id, supplier_name, contact, suplier_email, address, location, KRA_PIN, notes):
        self.__init__()
        query = ("INSERT INTO suppliers(supplier_id, suplier_name, contact, suplier_email, address, location, "
                 "KRA_PIN, notes) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)")
        values = (supplier_id, supplier_name, contact, suplier_email, address, location, KRA_PIN, notes)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            self.connection.close()
            return 1
        except:
            return 0
    
    # Create Product
    def createProductA(self, product_id, name, price, description, category_id):
        self.__init__()
        query = ("INSERT INTO products(product_id, name, price,  description, category_id ) VALUES(%s, %s, %s, %s, %s)")
        values = (product_id, name, price, description, category_id)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            self.connection.close()
            return 1
        except:
            return 0
    
    # Create category
    def create_product_categoryA(self, category_id, name, description):
        self.__init__()
        query = ("INSERT INTO categories(category_id, name, description) VALUES(%s, %s, %s)")
        values = (category_id, name, description)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            self.connection.close()
            return 1
        except:
            return 0
    
    # Stock Entry
    def stockEntryA(self, product_id, quantity, operation, location):
        self.__init__()
        query = ("INSERT INTO stock_entries(product_id, quantity, operation, location) VALUES(%s, %s, %s, %s)")
        values = (product_id, quantity, operation, location)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            self.connection.close()
            return 1
        except:
            return 0
        
    # Stock update/ create
    def createStockA(self, product_id, quantity, location, reorder_level, out_of_stock):
        self.__init__()
        query = ("INSERT INTO stock(product_id, quantity, location, reorder_level, out_of_stock) VALUES(%s, %s, %s, %s, %s)")
        values = (product_id, quantity, location, reorder_level, out_of_stock)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            self.connection.close()
            return 1
        except:
            return 0
    
    def getProductName(self, product_id):
        self.__init__()

        query = """
            SELECT name FROM products 
            WHERE product_id = %s 
        """
        values = (product_id)
        try:
            self.cursor.execute(query, values)
            user = self.cursor.fetchone()
            if user:
                return user[0]
            else:
                return 0
        except:
            return 0
    
    def update_productA(self, product_id, name, price, description, category_id):
        query = """
        UPDATE products
        SET  name = %s,
        price=%s,
        description=%s,
        category_id=%s
        
        WHERE product_id = %s
        """
        values = (name, price, description, category_id, product_id)
        
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            self.connection.close()
        except:
            return 0
            
    # Product Search
    def search_product(self, product_id):
        self.__init__()
        query = """
        SELECT name, price, description, category_id FROM products WHERE product_id = %s
        """
        values = (product_id,)
        try:
            self.cursor.execute(query, values)
            row= self.cursor.fetchone()
            while row is not None:
                return row
            self.connection.close()
        except:
            print("Failed")
    def search_stockA(self, product_id):
        query = """
        SELECT quantity, location, reorder_level, out_of_stock FROM stock WHERE product_id = %s
        """
        values = (product_id,)
        # Search
        try:
            self.cursor.execute(query, values)
            row= self.cursor.fetchone()
            while row is not None:
                return row
            self.connection.close()
        except:
            print("Failed")
        
    def delete_products(self, product_id):
        self.__init__()
        query = """
        DELETE FROM products WHERE product_id = %s
        """
        values = (product_id, )
        
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            self.connection.close()
        except:
            return 0
    
    # Check function 
    def check_stockA(self, product_id):
        self.__init__()
        query = """SELECT * FROM stock WHERE product_id = %s"""
        values = (product_id,)
        try:
            self.cursor.execute(query, values)
            row = self.cursor.fetchone()
            if row is not None:
                return 1
            else:
                return 0
        except:
            return 0
        
    # Update Stock
    def update_stockA(self, product_id, quantity, location, reorder_level, out_of_stock):
        query = """
        UPDATE stock 
        SET quantity = %s,
        location = %s,
        reorder_level = %s,
        out_of_stock = %s
        WHERE product_id = %s
        """
        values = (quantity,location, reorder_level, out_of_stock, product_id)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            self.connection.close()
        except:
            return 0
            
    # Count number of suppliers
    def count_suppliersA(self):   
        self.__init__() 
        query = """SELECT COUNT(*) FROM suppliers"""
        self.cursor.execute(query)
        
        value = self.cursor.fetchone()[0]
        return value
    
    # Count number of categories
    def count_categoriesA(self):   
        self.__init__() 
        query = """SELECT COUNT(*) FROM categories"""
        self.cursor.execute(query)
        
        value = self.cursor.fetchone()[0]
        return value
    
    # Count number of products
    def count_productsA(self):   
        self.__init__() 
        query = """SELECT COUNT(*) FROM products"""
        self.cursor.execute(query)
        
        value = self.cursor.fetchone()[0]
        return value
  
# me = admindb()
# me.create_product_categoryA("C001", "BEVERAGE", "Coffe, tea etc")
# me.createProductA("P002", "Yoghurt ", "100", "Drink ready", "C001")
# me.createStockA("P001", 10, "Main Store", 5, False)
# me.stockEntryA("P001", 5, "PLUS", "Main Store")

# print(me.getProductName("C001"))
# value = me.search_product("P001")[1]
#print(value)
    

            



