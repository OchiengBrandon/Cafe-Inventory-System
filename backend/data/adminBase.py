import mysql.connector
from backend.dbSettings import database_name, db_host, db_password, db_user
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Database class
class adminBase:
    def __init__(self):
        # Creating Connection
        self.connection = mysql.connector.connect(
            user=db_user,
            host=db_host,
            password=db_password,
            database=database_name
        )

        self.cursor = self.connection.cursor()
        
        
    # The Show Suppliers    
    def get_suppliers(self, location1, location2, location3, location4, location5):
        self.__init__()
        self.cursor.execute(f"SELECT supplier_id,suplier_name, contact, location, KRA_PIN FROM suppliers ORDER BY created_at DESC ")
        for result in self.cursor:
            ctk.CTkLabel(location1, text=result[0]).pack()
            ctk.CTkLabel(location2, text=result[1]).pack()
            ctk.CTkLabel(location3, text=result[2]).pack()
            ctk.CTkLabel(location4, text=result[3]).pack()
            ctk.CTkLabel(location5, text=result[4]).pack()
        self.connection.close()

    def product_tree_view(self, root):
        # Editing tree view
        # Filling function
        def fill_tree_view():
            product_tree.delete(*product_tree.get_children())
            
            # Get Products from database
            self.cursor.execute("SELECT product_id, name, price, category_id, description FROM products")
            products = self.cursor.fetchall()
            
            # Inserting The data in tree view
            for product in products:
                product_tree.insert('', 'end', values=product)
                
        # The Product tree
        product_tree = ttk.Treeview(root)
        product_tree['columns'] = ("product_id", "name", "price", "category_id", "description")
        
        product_tree.column('#0', width=30)
        product_tree.column('product_id', width=30)
        product_tree.column('name', width=70)
        product_tree.column('price', width=40)
        product_tree.column('category_id', width=30)
        product_tree.column('description', width=150)
        
        product_tree.heading('#0', text='#')
        product_tree.heading('product_id', text="product_id")
        product_tree.heading('name', text="name")
        product_tree.heading('price', text="price")
        product_tree.heading('category_id', text="category_id")
        product_tree.heading('description', text="description")
        
        product_tree.pack(fill="both", expand=True)
        
        # Filling tree View
        fill_tree_view()
    # Category Tree View
    def category_tree_view(self, root):
        # Filling the tree_view
        def fill_tree_view():
            product_tree.delete(*product_tree.get_children())
            
            # Get Products from database
            self.cursor.execute("SELECT category_id, name, description FROM categories")
            products = self.cursor.fetchall()
            
            # Inserting The data in tree view
            for product in products:
                product_tree.insert('', 'end', values=product)
            
        # The Product tree
        product_tree = ttk.Treeview(root)
        product_tree['columns'] = ("category_id", "name", "description")
        
        product_tree.column('#0', width=30)
        product_tree.column('category_id', width=20)
        product_tree.column('name', width=40)
        product_tree.column('description', width=50)
        
        product_tree.heading('#0', text='#')
        product_tree.heading('category_id', text="category_id")
        product_tree.heading('name', text="name")
        product_tree.heading('description', text="description")
        
        product_tree.pack(fill="both", expand=True)
        
        fill_tree_view()
    
    def stock_information_tree_view(self, root):
        # Filling the tree_view
        def fill_tree_view():
            product_tree.delete(*product_tree.get_children())
            
            # Get Products from database
            self.cursor.execute("SELECT id, name,category_id, quantity, reorder_level from products, stock")
            products = self.cursor.fetchall()
            
            # Inserting The data in tree view
            for product in products:
                product_tree.insert('', 'end', values=product)
                
        # The Product tree
        product_tree = ttk.Treeview(root)
        product_tree['columns'] = ("id", "name", "category_id","quantity", "reorder_level")
        
        product_tree.column('#0', width=30)
        product_tree.column('id', width=30)
        product_tree.column('name', width=70)
        product_tree.column('category_id', width=40)
        product_tree.column('quantity', width=30)
        product_tree.column('reorder_level', width=30)
        
        product_tree.heading('#0', text='#')
        product_tree.heading('id', text="Stock Id")
        product_tree.heading('name', text="Product Name")
        product_tree.heading('category_id', text="Category ID")
        product_tree.heading('quantity', text="Stock_Quantity")
        product_tree.heading('reorder_level', text="Reorder Level")
        
        product_tree.pack(fill="both", expand=True)
        fill_tree_view()
        