import customtkinter as ctk
from frontend.adminDashboard import adminDash
from backend.data.adminDatabase import admindb
from tkinter import messagebox


class admin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Admin")
        self.resizable(False, False)
        self.minsize(width=800, height=400)
        self.maxsize(width=800, height=400)

        # Local variable
        self.db = admindb()
        self.frame_bg = "transparent"
        self.entry_width = 200
        self.label_font = ctk.CTkFont(size=14)

        # putting login Screen
        self.admin_login()

    # Login Function
    def loginf(self):
        dash = adminDash(self.admin_login_email.get(), self.admin_login_password.get())
        if self.admin_login_email.get():
            if self.admin_login_password.get():
                if self.db.login_authenticationA(self.admin_login_email.get(), self.admin_login_password.get()) == 1:
                    self.withdraw()
                    dash.mainloop()
                else:
                    messagebox.showerror("Authentication Error", "Authentication failed")

            else:
                messagebox.showerror("Blank password", "Please enter password")
        else:
            messagebox.showerror("Blank email", "Please enter email")

    # Admin Account Login
    def admin_login(self):
        self.admin_login_frame = ctk.CTkFrame(self, bg_color=self.frame_bg)
        self.admin_login_frame.pack(anchor="center", pady=20)

        ctk.CTkLabel(
            master=self.admin_login_frame,
            text="Admin Login",
            font=ctk.CTkFont(family="Roboto", weight="bold", size=20)
        ).pack(pady=4)

        # Widget_frame
        widget_frame = ctk.CTkFrame(self.admin_login_frame, bg_color=self.frame_bg)
        widget_frame.pack()

        # Widgets
        self.admin_login_email = ctk.CTkEntry(widget_frame, placeholder_text="Email", width=self.entry_width)
        self.admin_login_password = ctk.CTkEntry(widget_frame, placeholder_text="Password", width=self.entry_width, show="*")

        # The frame
        ctk.CTkLabel(widget_frame, text="Email", font=self.label_font).grid(row=0, column=0, pady=8)
        self.admin_login_email.grid(row=0, column=1, padx=8)
        ctk.CTkLabel(widget_frame, text="Password", font=self.label_font).grid(row=1, column=0)
        self.admin_login_password.grid(row=1, column=1)

        ctk.CTkButton(self.admin_login_frame, text="Login", width=120, font=ctk.CTkFont(
            weight="bold"

        ), command=self.loginf).pack(pady=8)
        
    

        footer_frame = ctk.CTkFrame(self.admin_login_frame, width=400)
        footer_frame.pack()
        footer_frame.pack_configure(pady=8)

        # Redirect Method to account creation
        def redirect():
            self.admin_login_frame.destroy()
            self.admin_create_account()

        # Items in the Create frame
        direct_text = ctk.CTkLabel(footer_frame, text="New user? ", font=self.label_font)
        direct_text.grid(row=0, column=0)
        create_account_redirect_button = ctk.CTkButton(
            footer_frame,
            text="create admin account",
            width=50,
            command=redirect,
            fg_color="white",
            text_color="blue",
            font=ctk.CTkFont(weight="bold"),
            corner_radius=4,
        )
        create_account_redirect_button.grid(row=0, column=1)
        create_account_redirect_button.grid_configure(padx=3)

    # Create Account Backend
    def create_accountf(self):
        if self.createAccount_name.get():
            if self.createAccount_email.get():
                if self.createAccount_password.get():
                    if self.createAccount_confirm_password.get():
                        
                        # Checking if passwords match
                        if self.createAccount_password.get()==self.createAccount_confirm_password.get():  
                            # Validation
                            try:
                                if self.db.accountCreationA(
                                    self.createAccount_email.get(),
                                    self.createAccount_password.get(),
                                    self.createAccount_name.get()
                                    
                                    ) == 1:
                                    dash = adminDash(self.createAccount_email.get(),self.createAccount_email.get())
                                    messagebox.showinfo("Success", "Account Created Successfully")
                                    # Destroying Account Creation frame
                                    self.account_creation_frame.destroy()
                                    
                                    self.admin_login()
                                    
                                else:
                                    messagebox.showerror("Failed", "Account Not Created, Try Again")           
                            except:
                                messagebox.showerror("Error", "Failed")
                        else:
                            messagebox.showerror("Password Error", "Passwords do not Match")
                    else:
                        messagebox.showerror("Empty Fields", "Confirm password")
                else:
                    messagebox.showerror("Empty Fields", "Enter Password")
            else:
                messagebox.showerror("Empty Fields", "Enter Email")
            
        else:
            messagebox.showerror("Empty Fields", "Enter Name")
        
    # Admin Account Creation
    def admin_create_account(self):
        self.account_creation_frame = ctk.CTkFrame(self, bg_color=self.frame_bg)
        self.account_creation_frame.pack(anchor="center", pady=20)

        ctk.CTkLabel(
            master=self.account_creation_frame,
            text="Admin Create Account",
            font=ctk.CTkFont(family="Roboto", weight="bold", size=20)
        ).pack()
        
        # Settings
        entry_width = 200
        # Carries create account widgets
        content_frame = ctk.CTkFrame(self.account_creation_frame)
        content_frame.pack(ipadx=12)
        
        
        self.createAccount_name = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Name")
        self.createAccount_email = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Email")
        self.createAccount_password = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Password", show="*")
        self.createAccount_confirm_password = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Reenter Password", show="*")
        
        ctk.CTkLabel(content_frame, text="Name").grid(row=0, column=0, padx=5, pady=8)
        self.createAccount_name.grid(row=0, column=1)
        
        ctk.CTkLabel(content_frame, text="Email").grid(row=1, column=0, padx=5, pady=8)
        self.createAccount_email.grid(row=1, column=1)
        
        ctk.CTkLabel(content_frame, text="Password").grid(row=2, column=0, padx=5, pady=8)
        self.createAccount_password.grid(row=2, column=1)
        
        ctk.CTkLabel(content_frame, text="Confirm Password").grid(row=3, column=0, padx=5, pady=8)
        self.createAccount_confirm_password.grid(row=3, column=1)
        
        # Create Account Button
        ctk.CTkButton(self.account_creation_frame, text="Create Account", command=self.create_accountf).pack(pady=12)
        
        
    
        
        

if __name__ == "__main__":
    admin = admin()
    admin.mainloop()