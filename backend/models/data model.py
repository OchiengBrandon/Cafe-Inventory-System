import mysql.connector
from backend.dbSettings import database_name, db_host, db_password, db_user,db_port

class db_init:
    def __init__(self):
        # Creating Connection
        self.connection = mysql.connector.connect(
            host="sql.freedb.tech",
            port = db_port,
            user=db_user,
            password = db_password,
            database=database_name
        )
        
        self.cursor = self.connection.cursor()
        
        
        # Creating tables
        self.admin_table()
        self.suppliers_table()
        self.categories_table()
        self.products_table()
        self.stock_table()
        self.stock_entries_table()
        self.orders_table()
        self.orders_items()
        
    def stock_entries_table(self):
        query = """CREATE TABLE IF NOT EXISTS stock_entries(
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_id VARCHAR(10) NOT NULL,
            quantity INT NOT NULL,
            operation VARCHAR(10) NOT NULL,
            location VARCHAR(100) NOT NULL,
            entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
            
        )"""
        
        self.cursor.execute(query)
        self.connection.commit()
    
    def categories_table(self):
        query = """CREATE TABLE IF NOT EXISTS categories(
            category_id VARCHAR(10) PRIMARY KEY NOT NULL,
            name VARCHAR(50) NOT NULL,
            description TEXT
            
            
        )"""
        
        self.cursor.execute(query)
        self.connection.commit()
    def products_table(self):
        query = """CREATE TABLE IF NOT EXISTS  products(
            product_id VARCHAR(10) PRIMARY KEY NOT NULL,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            description TEXT,
            category_id VARCHAR(10) NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
            
        )"""
        
        self.cursor.execute(query)
        self.connection.commit()
    def stock_table(self):
        query = """CREATE TABLE IF NOT EXISTS  stock(
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_id VARCHAR(10) NOT NULL,
            quantity INT NOT NULL DEFAULT 0,
            location VARCHAR(100) NOT NULL,
            reorder_level INT NOT NULL, 
            out_of_stock BOOLEAN NOT NULL DEFAULT FALSE,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
            
        )"""
        
        self.cursor.execute(query)
        self.connection.commit()
    def suppliers_table(self):
        query = """CREATE TABLE IF NOT EXISTS suppliers(
            supplier_id VARCHAR(10)  NOT NULL,
            suplier_name VARCHAR(255) NOT NULL,
            contact VARCHAR(12) NOT NULL,
            suplier_email VARCHAR(255) UNIQUE NOT NULL,
            address VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            KRA_PIN VARCHAR(50) NOT NULL,
            notes VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (supplier_id)
     
        )"""
        
        self.cursor.execute(query)
        self.connection.commit()
        
    def admin_table(self):
        query = """CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
     
        )"""
        
        self.cursor.execute(query)
        self.connection.commit()
    
    def orders_table(self):
        query = """CREATE TABLE orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            supplier_id VARCHAR(10)  NOT NULL,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_amount DECIMAL(10,2),
            FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)   
        )"""
        
        self.cursor.execute(query)
        self.connection.commit()
        
    def orders_items(self):
        query = """CREATE TABLE order_items (
            order_item_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            product_id VARCHAR(10) NOT NULL,
            quantity INT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )"""
        
        self.cursor.execute(query)
        self.connection.commit()

if __name__ == "__main__":
    db_init()