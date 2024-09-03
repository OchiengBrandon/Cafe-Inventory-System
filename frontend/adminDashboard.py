import customtkinter as ctk
import datetime as dt
import time as tm
from backend.data.adminDatabase import admindb
from backend.data.reportGenerator import MySQLPDFReport
from backend.data.adminBase import adminBase
from frontend.frames.inventory import inventory_frame
from frontend.create_order import SupplierOrderCreator
from tkinter import messagebox



class adminDash(ctk.CTk):
    def __init__(self, email, password):
        super().__init__()
        self.title("Admin Dashboard")
        self.theme = "dark"
        ctk.set_appearance_mode("dark")
        self.email = email
        self.password = password
        self.date = dt.datetime.now()
       
        
        # Frames for Navigation place config
        self.relx = 0
        self.rely = 0
        self.relwidth = 1
        self.relheight = 1
        self.time = tm.strftime('%H:%M:%S')
        self.minsize(width=1250, height=700)
        self.maxsize(width=1250, height=7000)
        self.resizable(False, False)
        self.db = admindb()
        self.dbBase = adminBase()

        # Adding widgets
        self.top_bar()
        self.navigation()

        # Initialising Content
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.place(relx=0.17, rely=0.1, relwidth=0.825, relheight=0.85)
        # Inventroy frame Variable
        self.inventory_frame = None
        
        

        # Initially putting Dashboard
        self.the_dashboard()
        

    # The top Bar
    def top_bar(self):
        self.top_bar_frame = ctk.CTkFrame(self, height=80)
        self.top_bar_frame.place(relx=0.02, y=0, relwidth=0.96, bordermode="inside")

        # The left Top container
        left_container = ctk.CTkFrame(self.top_bar_frame, height=50)
        left_container.pack(side="left", pady=5, padx=5)
        self.welome_text = ctk.CTkLabel(
            left_container,
            text=f"Welcome {self.db.getNameA(self.email, self.password)}  ",
            font=ctk.CTkFont(
                size=16,
            )
        )
        self.welome_text.pack(side="left")

        ctk.CTkLabel(left_container, text="Status:", corner_radius=10, font=ctk.CTkFont(
            size=16,
            weight="bold",
        ), text_color="blue").pack(side="left")

        ctk.CTkLabel(left_container, text="..Online..", text_color="green", corner_radius=10, font=ctk.CTkFont(
            size=16,
        )).pack(side="right")

        # The Right Top Container
        right_container = ctk.CTkFrame(self.top_bar_frame, height=50)
        right_container.pack(side="right", pady=5, padx=5)
        ctk.CTkLabel(right_container, text=f"{self.date:%B, %d %Y}", font=ctk.CTkFont(size=16, weight="bold")).pack(
            side="left")

    # Frame Changeover
    def menu_switch(self):
        self.content_frame.forget()
        # Creating new Content Frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.place(relx=0.17, rely=0.1, relwidth=0.825, relheight=0.85)

    def navigation(self):
        side_bar = ctk.CTkFrame(self, corner_radius=10, fg_color="purple", border_width=4)
        side_bar.place(relx=0.01, rely=0.1, relheight=0.85, relwidth=0.15)

        # Title
        ctk.CTkLabel(side_bar, text="UEAB\nCafeteria", font=ctk.CTkFont(
            weight="bold",
            size=16

        )).pack(pady=5)

        # Separator
        ctk.CTkLabel(side_bar, text="________________________", text_color="Blue").pack()

        # Nav items Styling
        nav_items_bg = "purple"
        nav_items_padding = 8

        # Navigation Menu Items
        self.dashboard_button = ctk.CTkButton(side_bar, text="Dashboard", text_color="white", fg_color=nav_items_bg,
                                              command=self.the_dashboard)
        self.inventory_button = ctk.CTkButton(side_bar, text="Inventory", text_color="white", fg_color=nav_items_bg,
                                              command=self.inventory)
        self.Suppliers_button = ctk.CTkButton(side_bar, text="Suppliers", text_color="white", fg_color=nav_items_bg,
                                              command=self.suppliers)
        self.reports_button = ctk.CTkButton(side_bar, text="Reports", text_color="white", fg_color=nav_items_bg,
         
                                              command=self.reports)

        # Removed module
        # self.delivery_button = ctk.CTkButton(side_bar, text="Delivery", text_color="white", fg_color=nav_items_bg,
        #                                     command=self.delivery)
        self.settings_button = ctk.CTkButton(side_bar, text="Settings", text_color="white", fg_color=nav_items_bg,
                                             command=self.settings)

        # Adding them to the side bar
        self.dashboard_button.pack(pady=nav_items_padding)
        self.inventory_button.pack(pady=nav_items_padding)
        self.Suppliers_button.pack(pady=nav_items_padding)
        self.reports_button.pack(pady=nav_items_padding)
        # self.delivery_button.pack(pady=nav_items_padding)
        self.settings_button.pack(pady=nav_items_padding)

    # Dashboard Page
    def the_dashboard(self):
        self.menu_switch()
        dash_frame = ctk.CTkFrame(self.content_frame)
        dash_frame.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=self.relheight)
        # Title
        ctk.CTkLabel(dash_frame, text="Dashboard", text_color="white", font=ctk.CTkFont(size=16)).pack(pady=10)

        # contents
        self.dash_items_frame = ctk.CTkFrame(dash_frame, width=900, height=100)
        self.dash_items_frame.pack()
        # Fonts
        dash_items_font = ctk.CTkFont(weight="bold", size=14)
        dash_title_font = ctk.CTkFont(weight="bold", size=16)

        # Total Orders
        total_orders = ctk.CTkFrame(self.dash_items_frame, fg_color="orange")
        total_orders.place(relx=0, rely=0, relwidth=0.3)
        ctk.CTkLabel(total_orders, text=self.db.count_suppliersA(), font=dash_items_font).pack()
        ctk.CTkLabel(total_orders, text="Total Items", font=dash_items_font).pack()
        ctk.CTkLabel(total_orders, text="Total Suppliers", font=dash_title_font).pack()

        # Total Unpaid Orders
        unpaid_orders = ctk.CTkFrame(self.dash_items_frame, fg_color="Blue")
        unpaid_orders.place(relx=0.32, rely=0, relwidth=0.3)
        ctk.CTkLabel(unpaid_orders, text=self.db.count_productsA(), font=dash_items_font).pack()
        ctk.CTkLabel(unpaid_orders, text="Total Items", font=dash_items_font).pack()
        ctk.CTkLabel(unpaid_orders, text="Total Products", font=dash_title_font).pack()

        # Pending Delivery
        pending_delivery = ctk.CTkFrame(self.dash_items_frame, fg_color="grey", corner_radius=4)
        pending_delivery.place(relx=0.64, rely=0, relwidth=0.3)
        ctk.CTkLabel(pending_delivery, text=self.db.count_categoriesA(), font=dash_items_font).pack()
        ctk.CTkLabel(pending_delivery, text="Total Items", font=dash_items_font).pack()
        ctk.CTkLabel(pending_delivery, text="Total Categories", font=dash_title_font).pack()

        #*****************T***********

    # Create Supplier Backend_driver
    def create_supplier_driver(self):
        if self.create_supplier_id.get():
            if self.create_supplier_name.get():
                if self.create_supplier_Contact.get():
                    if self.create_supplier_Email.get():
                        if self.create_supplier_Address.get():
                            if self.create_supplier_Location.get():
                                if self.create_supplier_Kra_pin.get():
                                    # Running the Backend Config
                                    
                                    if self.db.createSupplierA(self.create_supplier_id.get(),
                                                                self.create_supplier_name.get(),
                                                                self.create_supplier_Contact.get(),
                                                                self.create_supplier_Email.get(),
                                                                self.create_supplier_Address.get(),
                                                                self.create_supplier_Location.get(),
                                                                self.create_supplier_Kra_pin.get(),
                                                                self.create_supplier_notes.get()) == 1:
                                        messagebox.showinfo("Success", "Supplier Created Successfully")
                                        self.create_supplier_window.withdraw()
                                    else:
                                        messagebox.showerror("Failed", "Failed To create Supplier")
                                    
                                else:
                                    messagebox.showerror("Empty Field", "Enter Supplier KRA PIN")
                            else:
                                messagebox.showerror("Empty Field", "Enter Supplier Location")
                        else:
                            messagebox.showerror("Empty Field", "Enter Supplier Address")
                    else:
                        messagebox.showerror("Empty Field", "Enter Supplier Email")
                else:
                    messagebox.showerror("Empty Field", "Enter Supplier Contact")
            else:
                messagebox.showerror("Empty Field", "Enter Name")
        else:
            messagebox.showerror("Empty Field", "Enter Supplier Id")

    # Open Inventory
    def inventory(self):
        self.menu_switch()
        self.inventory_frame = inventory_frame(self.content_frame)
        self.inventory_frame.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=self.relheight)
        
    # Create Supplier
    def create_supplier(self):
        self.create_supplier_window = ctk.CTkToplevel(self)
        self.create_supplier_window.title("Create Supplier")
        self.create_supplier_window.minsize(width=650, height=500)
        self.create_supplier_window.minsize(width=650, height=500)
        
        # Description
        ctk.CTkLabel(self.create_supplier_window, text="Fill in the form to Create a Supplier").pack(pady=10)

        # Supplier Frame
        create_frame = ctk.CTkFrame(self.create_supplier_window)
        create_frame.pack(pady=10, ipadx=5)
        # Items
        self.create_supplier_id = ctk.CTkEntry(create_frame, placeholder_text="Supplier ID")
        self.create_supplier_name = ctk.CTkEntry(create_frame, placeholder_text="Supplier Name")
        self.create_supplier_Kra_pin = ctk.CTkEntry(create_frame, placeholder_text="KRA Pin")
        self.create_supplier_Location = ctk.CTkEntry(create_frame, placeholder_text="Location")
        self.create_supplier_Contact = ctk.CTkEntry(create_frame, placeholder_text="Tel Number")
        self.create_supplier_Address = ctk.CTkEntry(create_frame, placeholder_text="Physical Address")
        self.create_supplier_Email = ctk.CTkEntry(create_frame, placeholder_text="Email")
        self.create_supplier_notes = ctk.CTkEntry(create_frame, width=200, height=80, placeholder_text="notes")

        # Adding Items
        # Basic Info
        ctk.CTkLabel(create_frame, text="Basic Information", text_color="blue",
                     font=ctk.CTkFont(weight="bold", size=14)).grid(row=0, column=0)
        ctk.CTkLabel(create_frame, text="Supplier Id").grid(row=1, column=0)
        self.create_supplier_id.grid(row=1, column=1, padx=8, pady=5)

        ctk.CTkLabel(create_frame, text="Supplier Name").grid(row=1, column=2)
        self.create_supplier_name.grid(row=1, column=3, padx=8, pady=5)

        # Contact
        ctk.CTkLabel(create_frame, text="Contact Information", text_color="blue",
                     font=ctk.CTkFont(weight="bold", size=14)).grid(row=2, column=0)
        ctk.CTkLabel(create_frame, text="Contact").grid(row=3, column=0)
        self.create_supplier_Contact.grid(row=3, column=1, padx=8, pady=5)

        ctk.CTkLabel(create_frame, text="Email").grid(row=3, column=2)
        self.create_supplier_Email.grid(row=3, column=3, padx=8, pady=5)

        ctk.CTkLabel(create_frame, text="Adress").grid(row=4, column=0)
        self.create_supplier_Address.grid(row=4, column=1, padx=8, pady=5)

        ctk.CTkLabel(create_frame, text="Location").grid(row=4, column=2)
        self.create_supplier_Location.grid(row=4, column=3, padx=8, pady=5)

        ctk.CTkLabel(create_frame, text="KRA PIN").grid(row=5, column=0)
        self.create_supplier_Kra_pin.grid(row=5, column=1, padx=8, pady=5)

        ctk.CTkLabel(create_frame, text="Notes").grid(row=6, column=0)
        self.create_supplier_notes.grid(row=6, column=1, padx=8, pady=5)

        # The Button
        ctk.CTkButton(self.create_supplier_window, text="Create", corner_radius=4, command=self.create_supplier_driver).pack(
            pady=10)


    def Show_Supplier_widgets(self):
        self.show_supplier_frame = ctk.CTkFrame(self.suppliers_frame, height=320)
        self.show_supplier_frame.pack(expand=True, fill="both")
        
        # SupplierId
        self.supplier_id_header = ctk.CTkFrame(self.show_supplier_frame)
        self.supplier_id_header.place(relx=0.1, rely=0.3)
        ctk.CTkLabel(self.supplier_id_header, text="Supplier ID", font=ctk.CTkFont(weight="bold", underline=True), text_color="brown").pack()
        
        # Supplier name
        self.supplier_name_header = ctk.CTkFrame(self.show_supplier_frame)
        self.supplier_name_header.place(relx=0.2, rely=0.3, relwidth=0.2)
        ctk.CTkLabel(self.supplier_name_header, text="Supplier Name", font=ctk.CTkFont(weight="bold", underline=True), text_color="brown").pack()
        
        # Supplier Contact
        self.supplier_Contact_header = ctk.CTkFrame(self.show_supplier_frame)
        self.supplier_Contact_header.place(relx=0.5, rely=0.3)
        ctk.CTkLabel(self.supplier_Contact_header, text="Contact", font=ctk.CTkFont(weight="bold", underline=True), text_color="brown").pack()
        
        # Location
        self.supplier_location_header = ctk.CTkFrame(self.show_supplier_frame)
        self.supplier_location_header.place(relx=0.7, rely=0.3)
        ctk.CTkLabel(self.supplier_location_header, text="LOCATION ID", font=ctk.CTkFont(weight="bold", underline=True), text_color="brown").pack()
        
        # Supplier kra pin
        self.supplier_KRA_header = ctk.CTkFrame(self.show_supplier_frame)
        self.supplier_KRA_header.place(relx=0.9, rely=0.3)
        ctk.CTkLabel(self.supplier_KRA_header, text="KRA PIN", font=ctk.CTkFont(weight="bold", underline=True), text_color="brown").pack()
        
        # Getting Suppliers
        self.dbBase.get_suppliers(self.supplier_id_header, self.supplier_name_header, self.supplier_Contact_header, self.supplier_location_header, self.supplier_KRA_header)

    # Update Supplier
    def update_supplier(self):
        update_supplier = ctk.CTkToplevel(self)
        update_supplier.title("Update Supplier")
        update_supplier.minsize(width=700, height=500)
        update_supplier.minsize(width=700, height=500)
        # Description
        ctk.CTkLabel(update_supplier, text="Enter Supplier Id to Update Existing Supplier").pack(pady=10)

        frame = ctk.CTkFrame(update_supplier, width=600, height=60)
        frame.pack()

        self.update_search_entry = ctk.CTkEntry(frame, placeholder_text="Supplier ID", width=370, corner_radius=2)
        self.update_search_entry.place(relx=0.1, rely=0.1)
        ctk.CTkButton(frame, text="Search", width=100, text_color="black", fg_color="light blue", font=ctk.CTkFont(
            weight="bold"
        )).place(relx=0.8, rely=0.1)

        # Supplier Frame
        create_frame = ctk.CTkFrame(update_supplier)
        create_frame.pack(pady=10, ipadx=5)
        # Items
        self.update_supplier_id = ctk.CTkEntry(create_frame, placeholder_text="Supplier ID")
        self.update_supplier_name = ctk.CTkEntry(create_frame, placeholder_text="Supplier Name")
        self.update_supplier_Kra_pin = ctk.CTkEntry(create_frame, placeholder_text="KRA Pin")
        self.update_supplier_Location = ctk.CTkEntry(create_frame, placeholder_text="Location")
        self.update_supplier_Contact = ctk.CTkEntry(create_frame, placeholder_text="Tel Number")
        self.update_supplier_Address = ctk.CTkEntry(create_frame, placeholder_text="Physical Address")
        self.update_supplier_Email = ctk.CTkEntry(create_frame, placeholder_text="Email")
        self.update_supplier_notes = ctk.CTkTextbox(create_frame, width=200, height=80)

        # Adding Items
        # Basic Info
        ctk.CTkLabel(create_frame, text="Basic Information", text_color="blue",
                     font=ctk.CTkFont(weight="bold", size=14)).grid(row=0, column=0)
        ctk.CTkLabel(create_frame, text="Supplier Id").grid(row=1, column=0)
        self.update_supplier_id.grid(row=1, column=1, padx=8, pady=5)

        ctk.CTkLabel(create_frame, text="Supplier Name").grid(row=1, column=2)
        self.update_supplier_name.grid(row=1, column=3, padx=8, pady=5)

        # Contact
        ctk.CTkLabel(create_frame, text="Contact Information", text_color="blue",
                     font=ctk.CTkFont(weight="bold", size=14)).grid(row=2, column=0)
        ctk.CTkLabel(create_frame, text="Contact").grid(row=3, column=0)
        self.update_supplier_Contact.grid(row=3, column=1, padx=8, pady=5)

        ctk.CTkLabel(create_frame, text="Email").grid(row=3, column=2)
        self.update_supplier_Email.grid(row=3, column=3, padx=8, pady=5)

        ctk.CTkLabel(create_frame, text="Adress").grid(row=4, column=0)
        self.update_supplier_Address.grid(row=4, column=1, padx=8, pady=5)

        ctk.CTkLabel(create_frame, text="Location").grid(row=4, column=2)
        self.update_supplier_Location.grid(row=4, column=3, padx=8, pady=5)

        ctk.CTkLabel(create_frame, text="KRA PIN").grid(row=5, column=0)
        self.update_supplier_Kra_pin.grid(row=5, column=1, padx=8, pady=5)

        ctk.CTkLabel(create_frame, text="Notes").grid(row=6, column=0)
        self.update_supplier_notes.grid(row=6, column=1, padx=8, pady=5)

        # The Button
        ctk.CTkButton(update_supplier, text="Update", corner_radius=4).pack(pady=10)

    # Suppliers Page
    
    # Open orders Window
    def open_orders(self):
        orders_window = SupplierOrderCreator(self)
        orders_window.mainloop()
        
    def suppliers(self):
        self.menu_switch()
        self.suppliers_frame = ctk.CTkFrame(self.content_frame)
        self.suppliers_frame.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=self.relheight)
        # Title
        ctk.CTkLabel(self.suppliers_frame, text="Suppliers", font=ctk.CTkFont(
            weight="bold",
            size=20
        ), text_color="white").pack(pady=10)

        menu = ctk.CTkFrame(self.suppliers_frame, width=900, height=60)
        menu.pack(pady=12)
        height = 40

        # Menu Items
        create_supplier_buton = ctk.CTkButton(menu, text="Create new Supplier", fg_color="Purple", height=height,
                                              command=self.create_supplier)
        update_supplier_buton = ctk.CTkButton(menu, text="Update Existing Supplier", fg_color="green", height=height,
                                              command=self.update_supplier)
        create_order_buton = ctk.CTkButton(menu, text="Create Order", fg_color="Orange", height=height, command=self.open_orders)

        # Putting menu items
        create_supplier_buton.place(relx=0.1, rely=0)
        update_supplier_buton.place(relx=0.4, rely=0)
        create_order_buton.place(relx=0.7, rely=0)

        # Search frame
        search_frame = ctk.CTkFrame(self.suppliers_frame, width=800, height=40)
        search_frame.pack(pady=12)

        # Search Items
        self.search_supplier_entry = ctk.CTkEntry(search_frame, width=370, corner_radius=2,
                                                  placeholder_text="Enter supplier id, name, email, location")
        self.search_supplier_entry.place(relx=0.01, rely=0.1)

        self.search_supplier_button = ctk.CTkButton(search_frame, text="Search", width=100, text_color="black",
                                                    fg_color="light blue", font=ctk.CTkFont(
                weight="bold"
            ))
        self.search_supplier_button.place(relx=0.865, rely=0.1)
        
        # Refresh
        self.refresh_supplier_button = ctk.CTkButton(self.suppliers_frame, text="Refresh", width=100, text_color="black",
                                                    fg_color="light blue", font=ctk.CTkFont(weight="bold"), command=self.refresh_suppliers)
        self.refresh_supplier_button.pack()
        
        self.Show_Supplier_widgets()
    # Refresh Suppliers Window
    def refresh_suppliers(self):
        self.show_supplier_frame.forget()
        self.Show_Supplier_widgets()
    # Orders Page
    def reports(self):
        self.menu_switch()
        reports_frame = ctk.CTkFrame(self.content_frame)
        reports_frame.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=self.relheight)
       
        
        content_frame = ctk.CTkFrame(reports_frame, height=40)
        content_frame.place(relx=0.1, rely=0.2, relwidth=0.8)
        
        ctk.CTkButton(content_frame, text="All product", height=30, command=MySQLPDFReport("products", "all products.pdf").generate_report()).grid(row=0, column=0,padx=12)
        ctk.CTkButton(content_frame, text="Stock Information", height=30, command=MySQLPDFReport("stock", "stock report.pdf").generate_report()).grid(row=0, column=1,padx=12)
        ctk.CTkButton(content_frame, text="All Categories", height=30, command=MySQLPDFReport("categories", "all categories.pdf").generate_report()).grid(row=0, column=2, padx=12)
        ctk.CTkButton(content_frame, text="All Orders", height=30,command=MySQLPDFReport("orders", "all orders.pdf").generate_report()).grid(row=0, column=3,padx=12)

    def report_middle(self, table, filename, desc):
        MySQLPDFReport("products", "all products.pdf").generate_report()
        messagebox.showinfo("Success",f"{desc} Report Created Successfully")
 
            
    # Delivery Page
    def delivery(self):
        self.menu_switch()
        delivery_frame = ctk.CTkFrame(self.content_frame)
        delivery_frame.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=self.relheight)
        ctk.CTkLabel(delivery_frame, text="Welcome to Delivery").pack()

    # Log Out Function
    def log_out(self):
        self.destroy()
    
    # Change theme
    def change_theme(self):
        if self._get_appearance_mode() == "light":
            ctk.set_appearance_mode("dark")
        elif self._get_appearance_mode() == "dark":
            ctk.set_appearance_mode("light")
            
            
    # Settings Page
    def settings(self):
        self.menu_switch()
        self.settings_frame = ctk.CTkFrame(self.content_frame)
        self.settings_frame.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=self.relheight)
        ctk.CTkLabel(self.settings_frame, text="Welcome to Settings", font=ctk.CTkFont(
            size=20, 
            weight="bold"
            )).pack()
        inner_settings_frame = ctk.CTkFrame(self.settings_frame)
        inner_settings_frame.pack(ipady=5, fill="x", pady=10)
        
        
        # Profile Information
        ctk.CTkLabel(inner_settings_frame, text="Name", font = ctk.CTkFont(weight="bold", size=14)).pack(pady=8)
        name_info = ctk.CTkEntry(inner_settings_frame, width=150)
        name_info.pack()
        name_info.insert(0, f"{self.db.getNameA(self.email, self.password)}")
        name_info.configure(state = "readonly")
        
        ctk.CTkLabel(inner_settings_frame,text="Email", font = ctk.CTkFont(weight="bold", size=14)).pack()
        profile_info = ctk.CTkEntry(inner_settings_frame, width=150)
        profile_info.pack()
        profile_info.insert(0, f"{self.email}")
        profile_info.configure(state = "readonly")
        # Change theme
        ctk.CTkButton(inner_settings_frame, text="Change theme",command=self.change_theme).pack(pady=10)
        
        # Log out Button
        ctk.CTkButton(inner_settings_frame, text="Log Out", command=self.log_out).pack(pady=10)
        
        # Info
        ctk.CTkLabel(self.settings_frame, text="To change the user profile details, consult the databsase adminstrator\nor the cafetreia manager", font=ctk.CTkFont(
            size=14,
            family="roboto"
            ),text_color="red").pack(pady=5)
        
        
    


if __name__ == "__main__":
    adminDash("p","ww").mainloop()
