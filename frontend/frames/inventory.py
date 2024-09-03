import customtkinter as ctk
import tkinter as tk
from backend.data.adminBase import adminBase
from backend.data.adminDatabase import admindb
from tkinter import messagebox

class inventory_frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.adminBase = adminBase()
        self.db = admindb()
        # Frames for Navigation place config
        self.relx = 0.01
        self.rely = 0.01
        self.relwidth = 0.98
        self.relheight = 0.98
        
        # Adding widgets
        self.side_bar()
        self.stock_content_frame = ctk.CTkFrame(self)
        self.stock_content_frame.place(relx=0.22,rely=0.01, relwidth=0.77, relheight=0.92)
        # Default frame
        self.stock_information()
        
    # Side Frame
    def side_bar(self):
        side_frame = ctk.CTkFrame(self)
        side_frame.place(relx=0.01, rely=0.01, relwidth=0.2, relheight=0.6)
        
        # Title
        ctk.CTkLabel(side_frame, text="Inventory Options", font=ctk.CTkFont(
            family="ROBOTO",
            size=14,
            weight="bold" 
        )).pack()
        
        # Options
        # Stock info Button
        stock_information_button = ctk.CTkButton(side_frame,text="Stock Information", command=self.stock_information)
        create_product_button = ctk.CTkButton(side_frame,text="Create new Product", command=self.create_new_product)
        update_product_button = ctk.CTkButton(side_frame,text="Update Product", command=self.update_product)
        update_stock_button = ctk.CTkButton(side_frame,text="Update Stock", command=self.update_stock)
        create_category_button = ctk.CTkButton(side_frame,text="Categories", command=self.categories)
        
        # Packing options
        stock_information_button.pack(pady=5)
        create_product_button.pack(pady=5)
        update_product_button.pack(pady=5)
        update_stock_button.pack(pady=5)
        create_category_button.pack(pady=5)
        
    
    # Frame Switch
    def change_stock_content(self):
        self.stock_content_frame.destroy()
        # Creating new frame
        self.stock_content_frame = ctk.CTkFrame(self)
        self.stock_content_frame.place(relx=0.22,rely=0.01, relwidth=0.77, relheight=0.92)
    
    def categories(self):
        # Clearing frame
        self.change_stock_content()
        categories_frame = ctk.CTkFrame(self.stock_content_frame)
        categories_frame.place(relx=self.relx, rely=self.rely, relwidth = self.relwidth, relheight = self.relheight)
        
        ctk.CTkLabel(categories_frame, text="Create New Category").pack()
        
        # Widgets
        widget_frame = ctk.CTkFrame(categories_frame)
        widget_frame.pack()
        
        self.category_id = ctk.CTkEntry(widget_frame, placeholder_text="Category_id", width=180)
        self.category_name = ctk.CTkEntry(widget_frame, placeholder_text="Name", width=180)
        self.category_description = ctk.CTkEntry(widget_frame, placeholder_text="Description", width=180, height=60)
        
        # Adding widgets
        ctk.CTkLabel(widget_frame, text="ID").grid(row=0, column=0)
        self.category_id.grid(row=0, column=1, pady=6, padx=8)
        
        ctk.CTkLabel(widget_frame, text="Name").grid(row=1, column=0)
        self.category_name.grid(row=1, column=1, pady=6, padx=8)
        
        ctk.CTkLabel(widget_frame, text="Description").grid(row=2, column=0)
        self.category_description.grid(row=2, column=1, pady=6, padx=8)
        
        # Button
        ctk.CTkButton(categories_frame, text="Create", command=self.create_category_driver).pack(pady=10)
        
        # Treeview frame
        tree_view_frame = ctk.CTkFrame(categories_frame)
        tree_view_frame.pack(fill="x", padx=10, pady=20)
        self.adminBase.category_tree_view(tree_view_frame)  
        
    # Create category back end
    def create_category_driver(self):
        try:
            # Checking for inputs
            if self.category_id.get():
                if self.category_name.get():
                    if self.db.create_product_categoryA(
                        self.category_id.get(),
                        self.category_name.get(),
                        self.category_description.get()
                    ) == 1:
                        messagebox.showinfo("Successfull", "Category created successfully")
                        self.category_id.delete(0, "end")
                        self.category_name.delete(0, "end")
                        self.category_description.delete(0, "end")
                    else:
                        messagebox.showerror("Error", "Failed to Create Product")
                else:
                    messagebox.showerror("Empty Fields", "Name")
            else:
                messagebox.showerror("Empty Fields", "Input ID")
        except:
            messagebox.showerror("Error", "Failed to Create Product")
            
    # Show Products Backend
    def show_products(self):
        # Clearing the fields
        self.update_product_name.delete(0, "end")
        self.update_product_price.delete(0, "end")
        self.update_product_description.delete(0, "end")
        self.update_product_category_id.delete(0, "end")
        # Inserting data in fields
        try:
            self.update_product_name.insert(0, self.db.search_product(self.update_product_id.get())[0])
            self.update_product_price.insert(0, self.db.search_product(self.update_product_id.get())[1])
            self.update_product_description.insert(0, self.db.search_product(self.update_product_id.get())[2])
            self.update_product_category_id.insert(0, self.db.search_product(self.update_product_id.get())[3])
            
        except:
            messagebox.showerror("Error", "Product Does not Exists")
    # Update Product Backend
    def update_product_driver(self):
        try:
            if self.db.update_productA(
                self.update_product_id.get(),
                self.update_product_name.get(),
                self.update_product_price.get(),
                self.update_product_description.get(),
                self.update_product_category_id.get()
            )!= 0:
                messagebox.showinfo("Done", "Update Successful")
            else:
                messagebox.showerror("Failed", "Update Unsuccesfull")
            
        except:
            messagebox.showerror("Failed", "Update Unsuccesfull")
    # Update Product Frame
    
    # Delete Backend
    def deleteProduct_driver(self):
        try:
            if self.db.delete_products(self.update_product_id.get()) !=0:
                messagebox.showinfo("Successful", "Product Deleted Successfully")
            else:
                messagebox.showerror("Error", "Delete Failed")
                
        except:
            messagebox.showerror("Error", "Delete Failed")
            
    # Update Product    
    def update_product(self):
        self.change_stock_content()
        # The frame
        self.update_product_frame = ctk.CTkFrame(self.stock_content_frame)
        self.update_product_frame.place(relx=self.relx, rely=self.rely, relwidth = self.relwidth, relheight = self.relheight)
        
        ctk.CTkLabel(self.update_product_frame,text="Update Product Details", font=ctk.CTkFont(
            weight="bold",
            size=16
            )).pack(pady=5)
        # Create product frame
        update_frame = ctk.CTkFrame(self.update_product_frame)
        update_frame.pack()
        
        # Variables
        entry_width = 210
        # Frame widgets
        self.update_product_id = ctk.CTkEntry(update_frame, width=entry_width)
        self.update_product_name = ctk.CTkEntry(update_frame, width=entry_width)
        self.update_product_price = ctk.CTkEntry(update_frame, width=entry_width)
        self.update_product_category_id = ctk.CTkEntry(update_frame, width=entry_width)
        self.update_product_description = ctk.CTkEntry(update_frame, width=entry_width)
        
        
        # Constructing frame
        ctk.CTkLabel(update_frame, text="Product Id").grid(row=0, column=0)
        self.update_product_id.grid(row=0, column=1, padx=8, pady=5)
        ctk.CTkButton(update_frame, text="Show", command=self.show_products).grid(row=0, column=2, padx=5, pady=5)
      
        
        ctk.CTkLabel(update_frame, text="Poduct Name").grid(row=1, column=0)
        self.update_product_name.grid(row=1, column=1, padx=8, pady=5)
        
        ctk.CTkLabel(update_frame, text="Product Price").grid(row=2, column=0)
        self.update_product_price.grid(row=2,column=1, padx=8, pady=5)
        
        ctk.CTkLabel(update_frame, text="Category_ID").grid(row=4, column=0)
        self.update_product_category_id.grid(row=4, column=1, padx=8, pady=5)
        
        ctk.CTkLabel(update_frame, text="Description").grid(row=3, column=0)
        self.update_product_description.grid(row=3, column=1, padx=8, pady=5)
        
        # Adding Button
        ctk.CTkButton(self.update_product_frame, text="Update", width=150, command=self.update_product_driver).pack(pady=12, padx=2)
        ctk.CTkButton(self.update_product_frame, text="Delete", width=150, command=self.deleteProduct_driver).pack(pady=12, padx=2)
    
    
        
    # Show Inventory
    def stock_information(self):
        self.change_stock_content()
        self.stock_info_frame = ctk.CTkFrame(self.stock_content_frame)
        self.stock_info_frame.place(relx=self.relx, rely=self.rely, relwidth = self.relwidth, relheight = self.relheight)
        ctk.CTkLabel(self.stock_info_frame, text="Stock Information").pack()
        
        # Treeview frame
        tree_view_frame = ctk.CTkFrame(self.stock_info_frame)
        tree_view_frame.pack(fill="x", padx=10, pady=20)
        self.adminBase.stock_information_tree_view(tree_view_frame)  
        
    # New Product driver
    def create_new_product_driver(self):
        # Checking if they are not null
        if self.create_product_id.get():
            if self.create_product_name.get():
                if self.create_product_price.get():
                    if self.create_product_category_id.get():
                        if self.create_product_description.get():
                            # Back end logic
                            if self.db.createProductA(
                                self.create_product_id.get(),
                                self.create_product_name.get(),
                                self.create_product_price.get(),
                                self.create_product_description.get(),
                                self.create_product_category_id.get()) ==1:
                                messagebox.showinfo("Success", "Product Created Successfully")
                                # Clearing the entries
                                self.create_product_id.delete(0, "end")
                                self.create_product_name.delete(0, "end")
                                self.create_product_price.delete(0, "end")
                                self.create_product_category_id.delete(0, "end")
                                self.create_product_description.delete(0, "end")
                            else:
                                messagebox.showerror("Failed", "Failed to Create Product")

                        else:
                            messagebox.showerror("Empty Fields", "Enter Description, or type none")
                    else:
                        messagebox.showerror("Empty Fields", "Enter Category ID")
                else:
                    messagebox.showerror("Empty Fields", "Enter Product Price")
            else:
                messagebox.showerror("Empty Fields", "Enter Product Name")
                
        else:
            messagebox.showerror("Empty Fields", "Enter Product_id")
        
        
    # Show Inventory
    def create_new_product(self):
        self.change_stock_content()
        self.create_new_product = ctk.CTkFrame(self.stock_content_frame)
        self.create_new_product.place(relx=self.relx, rely=self.rely, relwidth = self.relwidth, relheight = self.relheight)
        ctk.CTkLabel(self.create_new_product, text="Create new Product").pack()
        
        # Create product frame
        create_product_frame = ctk.CTkFrame(self.create_new_product)
        create_product_frame.pack()
        
        # Variables
        entry_width = 210
        # Frame widgets
        self.create_product_id = ctk.CTkEntry(create_product_frame, width=entry_width)
        self.create_product_name = ctk.CTkEntry(create_product_frame, width=entry_width)
        self.create_product_price = ctk.CTkEntry(create_product_frame, width=entry_width)
        self.create_product_category_id = ctk.CTkEntry(create_product_frame, width=entry_width)
        self.create_product_description = ctk.CTkEntry(create_product_frame, width=entry_width)
        
        
        # Constructing frame
        ctk.CTkLabel(create_product_frame, text="Product Id").grid(row=0, column=0)
        self.create_product_id.grid(row=0, column=1, padx=8, pady=5)
        
        ctk.CTkLabel(create_product_frame, text="Poduct Name").grid(row=1, column=0)
        self.create_product_name.grid(row=1, column=1, padx=8, pady=5)
        
        ctk.CTkLabel(create_product_frame, text="Product Price").grid(row=2, column=0)
        self.create_product_price.grid(row=2,column=1, padx=8, pady=5)
        
        ctk.CTkLabel(create_product_frame, text="Category_ID").grid(row=4, column=0)
        self.create_product_category_id.grid(row=4, column=1, padx=8, pady=5)
        
        ctk.CTkLabel(create_product_frame, text="Description").grid(row=3, column=0)
        self.create_product_description.grid(row=3, column=1, padx=8, pady=5)
        
        # Adding Button
        ctk.CTkButton(self.create_new_product, text="Create", width=150, command=self.create_new_product_driver).pack(pady=12, padx=2)
        
        # Treeview frame
        self.tree_view_frame = ctk.CTkFrame(self.create_new_product)
        self.tree_view_frame.pack(fill="x", padx=10, pady=20)
        self.adminBase.product_tree_view(self.tree_view_frame)      

        
    # Update Stock
    def update_stock(self):
        self.change_stock_content()
        self.update_stock_frame = ctk.CTkFrame(self.stock_content_frame)
        self.update_stock_frame.place(relx=self.relx, rely=self.rely, relwidth = self.relwidth, relheight = self.relheight)
        ctk.CTkLabel(self.update_stock_frame, text="Update Stock").pack()
        
        # Search Frame
        self.search_frame = ctk.CTkFrame(self.update_stock_frame, width=600, height=40)
        self.search_frame.pack()
        
        # Search Items
        self.update_stock_search = ctk.CTkEntry(self.search_frame, width=370, corner_radius=2,
                                                  placeholder_text="Enter Product Id to Update stock")
        self.update_stock_search.place(relx=0.01, rely=0.1)

        self.update_stock_search_button = ctk.CTkButton(self.search_frame, text="Show", width=100, text_color="black",fg_color="light blue", font=ctk.CTkFont(
            weight="bold"
            ), command=self.update_stock_popup   
        )
        self.update_stock_search_button.place(relx=0.7, rely=0.1)
        # Serch _value
        self.update_stock_search_value = self.update_stock_search.get()

    # Search Product Display
    def product_display(self, product_id):
        try:
            if self.db.search_product(product_id) !=0:
                val =  self.db.search_product(product_id)[0]
                return val
            else:
                error = "No result!"
                return error
        except:
            error = "No result!"
            return error

        # Update Stock Frame
    def update_stock_popup(self):    
        self.update_stock_search_button.destroy()
        # Checking if Product data is available
        self.search_result = ctk.CTkLabel(self.search_frame, text=self.product_display(self.update_stock_search.get()), font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                ))
        self.search_result.place(relx=0.7, rely=0.1)
        # Entry width
        entry_width = 210
        self.update_stock_popup_frame = ctk.CTkFrame(self.update_stock_frame,width=700)
        self.update_stock_popup_frame.pack(pady=20, ipadx=50, ipady=10)
        
        # Widgets
        self.update_stock_product_id = ctk.CTkEntry(self.update_stock_popup_frame, width=entry_width)
        self.update_stock_quantity = ctk.CTkEntry(self.update_stock_popup_frame, width=entry_width)
        self.update_stock_location = ctk.CTkEntry(self.update_stock_popup_frame, width=entry_width)
        self.update_stock_reorderLevel = ctk.CTkEntry(self.update_stock_popup_frame, width=entry_width)
        self.update_stock_Out_of_stock = ctk.CTkEntry(self.update_stock_popup_frame, width=entry_width )
        
        # Packing Items
        ctk.CTkLabel(self.update_stock_popup_frame, text="Product Id").grid(row=0, column=0, padx=8, pady=5)
        self.update_stock_product_id.grid(row=0, column=1)
        
        
        ctk.CTkLabel(self.update_stock_popup_frame, text="Quantity").grid(row=1, column=0, padx=8, pady=5)
        self.update_stock_quantity.grid(row=1, column=1)
        
        
        ctk.CTkLabel(self.update_stock_popup_frame, text="Location").grid(row=2, column=0, padx=8, pady=5)
        self.update_stock_location.grid(row=2, column=1)
        
        ctk.CTkLabel(self.update_stock_popup_frame, text="Reorder Level").grid(row=3, column=0, padx=8, pady=5)
        self.update_stock_reorderLevel.grid(row=3, column=1)
        
        ctk.CTkLabel(self.update_stock_popup_frame, text="Out of Stock").grid(row=4, column=0, padx=8, pady=5)
        self.update_stock_Out_of_stock.grid(row=4, column=1)
        
        self.update_stock_product_id.insert(0, str(self.update_stock_search.get()))
        # Checking if stock is available
        if self.db.check_stockA(self.update_stock_product_id.get()) == 1:
            # Inserting Stock Data
            self.insert_stock_data()
            

        self.update_create_button = ctk.CTkButton(self.update_stock_frame, text="Submit", command=self.update_stock_driver)
        self.update_create_button.pack(pady=10)
        ctk.CTkButton(self.update_stock_frame, text="Search Again", command=self.search_again).pack(pady=10)
    
    def search_again(self):
        # Destroy Main Frame
        self.update_stock_frame.destroy()
        # Refreshing
        self.update_stock()
    
    # Insert stock data
    def insert_stock_data(self):
        self.update_stock_quantity.delete(0, "end")
        self.update_stock_location.delete(0,"end")
        self.update_stock_reorderLevel.delete(0, "end")
        self.update_stock_Out_of_stock.delete(0, "end")
        try:
            self.update_stock_quantity.insert(0, self.db.search_stockA(self.update_stock_product_id.get())[0])
            self.update_stock_location.insert(0, self.db.search_stockA(self.update_stock_product_id.get())[1])
            self.update_stock_reorderLevel.insert(0, self.db.search_stockA(self.update_stock_product_id.get())[2])
            self.update_stock_Out_of_stock.insert(0, self.db.search_stockA(self.update_stock_product_id.get())[3])
        except:
            print("Failed")
    # Update stock Driver
    def update_stock_driver(self):
        # Choosing between update and Create
        # Update Logic
        if self.db.check_stockA(self.update_stock_product_id.get()) ==1:
            try:
                if self.db.update_stockA(
                    self.update_stock_product_id.get(),
                    self.update_stock_quantity.get(),
                    self.update_stock_location.get(),
                    self.update_stock_reorderLevel.get(),
                    self.update_stock_Out_of_stock.get()
                    ) !=0:
                    messagebox.showinfo("Success", "Stock Updated successfully")
                    self.update_stock_frame.destroy()
                    self.update_stock()
                else:
                    messagebox.showerror("Failed", "Update Unsuccessful")
            except:
                messagebox.showerror("Failed", "Update Unsuccessful")
                
        # Create new Product
        else:
            try:
                if self.db.createStockA(
                    self.update_stock_product_id.get(),
                    self.update_stock_quantity.get(),
                    self.update_stock_location.get(),
                    self.update_stock_reorderLevel.get(),
                    self.update_stock_Out_of_stock.get()
                ) ==1:
                    messagebox.showinfo("Success", "Stock Created successfully")
                    self.update_stock_frame.destroy()
                    self.update_stock()
                    
                else:
                    messagebox.showerror("Failed", "Failed To create Stock")
            except:
                messagebox.showerror("Failed", "Failed To create Stock")
                
                    
            
                
        
        
        
        

        
        