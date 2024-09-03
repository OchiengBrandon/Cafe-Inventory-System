import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from backend.dbSettings import db_host,db_password, db_user, database_name

class MySQLPDFReport:
    def __init__(self, table_name, pdf_file_name):
        self.host = db_host
        self.user = db_user
        self.password = db_password
        self.database = database_name
        self.table_name = table_name
        self.pdf_file_name = pdf_file_name

    def generate_report(self):
        # Connect to the MySQL database
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        # Get a cursor object to execute SQL queries
        cursor = db.cursor()

        # Execute a SQL query to get the database report
        cursor.execute(f"SELECT * FROM {self.table_name}")
        report_data = cursor.fetchall()

        # Create a PDF document
        doc = SimpleDocTemplate(self.pdf_file_name, pagesize=letter)
        elements = []

        # Create a table from the report data
        table_data = [[col[0] for col in cursor.description]]  # Add column headers
        table_data.extend(report_data)
        table = Table(table_data)

        # Apply table style
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

        # Add the table to the PDF document
        elements.append(table)

        # Build the PDF document
        doc.build(elements)

        # Close the database connection
        db.close()

        print(f"PDF report saved as {self.pdf_file_name}")