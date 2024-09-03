import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from backend.dbSettings import db_user, db_host, db_password, database_name
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib import colors, styles

class SupplierOrderCreator(tk.Toplevel):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.minsize(width=600, height=700)
        self.maxsize(width=600, height=700)
        self.title("Supplier Order Creator")

        # Connect to MySQL database
        self.db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=database_name
        )
        self.cursor = self.db.cursor()

        # Create a style for the application
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("TLabel", font=("Times New Roman", 10))
        self.style.configure("TCombobox", font=("Times New Roman", 10))
        self.style.configure("TButton", font=("Times New Roman", 10))
        self.style.configure("TEntry", font=("Times New Roman", 10))

        # Create a frame for the order details
        self.order_frame = ttk.Frame(self)
        self.order_frame.pack(pady=20)


        # Create labels and entry fields for order details
        self.order_label = ttk.Label(self.order_frame, text="Order Details:")
        self.order_label.grid(row=0, column=0, sticky="w")

        self.supplier_label = ttk.Label(self.order_frame, text="Supplier:")
        self.supplier_label.grid(row=1, column=0, sticky="w")
        self.supplier_var = tk.StringVar()
        self.supplier_dropdown = ttk.Combobox(self.order_frame, textvariable=self.supplier_var, state="readonly")
        self.supplier_dropdown.grid(row=1, column=1)

        # Create a frame for the product selections
        self.product_frame = ttk.Frame(self)
        self.product_frame.pack(pady=20)

        self.product_label = ttk.Label(self.product_frame, text="Products:")
        self.product_label.grid(row=0, column=0, sticky="w")

        self.product_dropdowns = []
        self.quantity_entries = []

        self.add_product_button = ttk.Button(self.product_frame, text="+", command=self.add_product)
        self.add_product_button.grid(row=len(self.product_dropdowns)+40, column=0)


        # Create a button to generate the report
        self.report_button = ttk.Button(self, text="Generate Report", command=self.generate_report)
        self.report_button.pack(pady=20)

        self.populate_dropdowns()
        
    def add_product(self):
        product_dropdown = ttk.Combobox(self.product_frame, state="readonly")
        product_dropdown.grid(row=len(self.product_dropdowns)+1, column=0, pady=5)
        quantity_entry = ttk.Entry(self.product_frame)
        quantity_entry.grid(row=len(self.quantity_entries)+1, column=1, padx=5)
        self.product_dropdowns.append(product_dropdown)
        self.quantity_entries.append(quantity_entry)
        self.populate_dropdowns()

    def populate_dropdowns(self):
        # Populate the supplier dropdown
        self.cursor.execute("SELECT supplier_id, suplier_name FROM suppliers")
        self.suppliers = [(row[0], row[1]) for row in self.cursor.fetchall()]
        self.supplier_dropdown["values"] = [supplier[1] for supplier in self.suppliers]
        self.supplier_var.set(self.suppliers[0][1])

        # Populate the product dropdown
        self.cursor.execute("SELECT product_id, name FROM products")
        self.products = [(row[0], row[1]) for row in self.cursor.fetchall()]
        for product_dropdown in self.product_dropdowns:
            product_dropdown["values"] = [product[1] for product in self.products]
            product_dropdown.current(0)  # Set the first product as the current selection

    def generate_report(self):
        try:
            # Get the selected supplier
            try:
                selected_supplier_id = next(supplier[0] for supplier in self.suppliers if supplier[1] == self.supplier_var.get())
            except StopIteration:
                messagebox.showerror("Null Fields", "Products not selected")
                return

            # Get the selected products and quantities
            selected_products = []
            for product_dropdown, quantity_entry in zip(self.product_dropdowns, self.quantity_entries):
                try:
                    selected_product_id = next(product[0] for product in self.products if product[1] == product_dropdown.get())
                    quantity = int(quantity_entry.get())
                    selected_products.append((selected_product_id, quantity))
                except (StopIteration, ValueError):
                    print(f"Selected product '{product_dropdown.get()}' not found in the list or invalid quantity.")
                    continue

            # Validate if at least one product is selected
            if not selected_products:
                messagebox.showerror("No Products Selected", "Please select at least one product to generate the report.")
                return

            # Insert the order into the database
            self.cursor.execute("INSERT INTO orders (supplier_id) VALUES (%s)", (selected_supplier_id,))
            order_id = self.cursor.lastrowid
            for product_id, quantity in selected_products:
                self.cursor.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)", (order_id, product_id, quantity))
            self.db.commit()

            # Create the PDF report
            doc = SimpleDocTemplate("order_report.pdf", pagesize=letter)
            elements = []

            # Get the sample stylesheets
            styles = getSampleStyleSheet()
            # Add the order details to the report
            report_text = Paragraph("Order placed:\n", styles["Heading1"])
            elements.append(report_text)

            for product_dropdown, quantity_entry in zip(self.product_dropdowns, self.quantity_entries):
                product_name = product_dropdown.get()
                quantity = int(quantity_entry.get())
                report_text = Paragraph(f"- {quantity} units of {product_name}", styles["BodyText"])
                elements.append(report_text)

            report_text = Paragraph(f"from {self.supplier_var.get()}", styles["BodyText"])
            elements.append(report_text)
            
            report_text = Paragraph("*************************************************************",styles["BodyText"])
            elements.append(report_text)

            # Create a table for the order items
            data = [["Product", "Quantity", "Total"]]
            total = 0
            for product_dropdown, quantity_entry in zip(self.product_dropdowns, self.quantity_entries):
                product_name = product_dropdown.get()
                quantity = int(quantity_entry.get())
                product_total = quantity
                data.append([product_name, quantity, product_total])
                total += product_total
            data.append(["", "Total", total])

            table = Table(data)
            table_style = TableStyle([
                ("BACKGROUND", (0,0), (-1,0), colors.grey),
                ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
                ("ALIGN", (0,0), (-1,-1), "CENTER"),
                ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
                ("FONTSIZE", (0,0), (-1,0), 14),
                ("BOTTOMPADDING", (0,0), (-1,0), 12),
                ("BACKGROUND", (0,1), (-1,-1), colors.beige),
                ("GRID", (0,0), (-1,-1), 1, colors.black)
            ])
            table.setStyle(table_style)
            elements.append(table)

            # Build the PDF report
            doc.build(elements)

            print(f"PDF report generated: order_report.pdf{selected_supplier_id}")
            messagebox.showinfo("Success", "Order created Successfully")
        except:
            messagebox.showerror("Failed", "Failed to create Order")
                

if __name__ == "__main__":
    app = SupplierOrderCreator()
    app.mainloop()