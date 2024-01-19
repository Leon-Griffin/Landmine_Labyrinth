from tkinter import Frame, Label, Button, font, StringVar, Entry, messagebox, Tk
import bcrypt
import datetime

class UserAuthentication:

    def __init__(self, root, database=None, users=None):
        self.root = root
        self.users = users or []
        self.database = database
        self.current_user = None
        self.authentication_over = False
        self.UserRecord = UserRecord

    def destroy_window(self, window):
        window.destroy()
        self.root.update()

    def authenticate_user(self):
        welcome_window = Frame(self.root)
        welcome_window.pack()

        Label(welcome_window, text="Welcome!\n", font=font.Font(family="Fixedsys", size=30, weight="bold")).grid(row=0, column=0, columnspan=3)
        Button(welcome_window, text="Sign Up\n   (new user)   ", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda: (self.destroy_window(welcome_window), self.sign_up())).grid(row=1, column=0, padx=15, pady=15)
        Label(welcome_window, text="  or  ", font=font.Font(family="Fixedsys", size=20, weight="bold")).grid(row=1, column=1, padx=15, pady=15)
        Button(welcome_window, text="Log In\n(returning user)", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda: (self.destroy_window(welcome_window), self.log_in())).grid(row=1, column=2, padx=15, pady=15)
        Button(welcome_window, text="Skip To Game", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda: (self.destroy_window(welcome_window), setattr(self, "authentication_over", True))).grid(row=2, columnspan=3, padx=15, pady=15)

    def sign_up(self):
        signup_window = Frame(self.root)
        signup_window.pack()

        username_var = StringVar()
        password1_var = StringVar()
        password2_var = StringVar()

        Label(signup_window, text="Username:", font=font.Font(family="Fixedsys", size=20, weight="bold")).grid(row=0, column=0, padx=10, pady=10)
        username_entry = Entry(signup_window, textvariable=username_var, font=font.Font(family="Fixedsys", size=20, weight="bold"))
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(signup_window, text="Password:", font=font.Font(family="Fixedsys", size=20, weight="bold")).grid(row=1, column=0, padx=10, pady=10)
        password_entry1 = Entry(signup_window, show="*", textvariable=password1_var, font=font.Font(family="Fixedsys", size=20, weight="bold"))
        password_entry1.grid(row=1, column=1, padx=10, pady=10)

        Label(signup_window, text="Confirm Password:", font=font.Font(family="Fixedsys", size=20, weight="bold")).grid(row=2, column=0, padx=10, pady=10)
        password_entry2 = Entry(signup_window, show="*", textvariable=password2_var, font=font.Font(family="Fixedsys", size=20, weight="bold"))
        password_entry2.grid(row=2, column=1, padx=10, pady=10)

        Button(signup_window, text="Back", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda: (self.destroy_window(signup_window), self.authenticate_user())).grid(row=3, column=0)
        submit_button = Button(signup_window, text="Submit", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda: self.destroy_window(signup_window))
        submit_button.grid(row=3, column=1, columnspan=2, pady=15)
        submit_button.config(state='disabled')

        check_entries = lambda *args: submit_button.config(state='active') if all((username_var.get(), password1_var.get(), password2_var.get())) else submit_button.config(state='disabled')

        username_var.trace_add('write', check_entries)
        password1_var.trace_add('write', check_entries)
        password2_var.trace_add('write', check_entries)

    def log_in(self):
        login_window = Frame(self.root)
        login_window.pack()

        username_var = StringVar()
        password_var = StringVar()

        Label(login_window, text="Username:", font=font.Font(family="Fixedsys", size=20, weight="bold")).grid(row=0, column=0, padx=10, pady=10)
        username_entry = Entry(login_window, textvariable=username_var, font=font.Font(family="Fixedsys", size=20, weight="bold"))
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(login_window, text="Password:", font=font.Font(family="Fixedsys", size=20, weight="bold")).grid(row=1, column=0, padx=10, pady=10)
        password_entry = Entry(login_window, show="*", textvariable=password_var, font=font.Font(family="Fixedsys", size=20, weight="bold"))
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        Button(login_window, text="Back", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda: (self.destroy_window(login_window), self.authenticate_user())).grid(row=3, column=0)
        submit_button = Button(login_window, text="Submit", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda: self.destroy_window(login_window))
        submit_button.grid(row=3, column=0, columnspan=2, pady=15)
        submit_button.config(state='disabled')

        check_entries = lambda *args: submit_button.config(state='active') if all((username_var.get(), password_var.get())) else submit_button.config(state='disabled')

        username_var.trace_add('write', check_entries)
        password_var.trace_add('write', check_entries)

    def submit_signup(self, username, password1, password2):
        if password1 != password2:
            messagebox.showerror("Error", "Passwords do not match!")
            
        elif self.binary_search_users(username) is not None:
            messagebox.showerror("Error", "Username already in use!")
            
        elif len(password1) < 5:
            messagebox.showerror("Error", "Password should be 5 characters or more!")
            
        elif password1 == username:
            messagebox.showerror("Error", "Username should not be the same as the password!")
            
        else:
            try:
                current_user = self.UserRecord(username, bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt()), 0, False, datetime.datetime(2020, 1, 1))
                self.users.append(current_user)

                if self.database is not None:
                    self.database.add_user(current_user)

                messagebox.showinfo("Success", "Sign up was successful")
                self.current_user = current_user
                self.authentication_over = True

            except Exception as e:
                messagebox.showerror("Error", f"Sign up unsuccessful: {str(e)}")

    def submit_login(self, username, password):
        user_index = self.binary_search_users(username)
        if user_index is None:
            messagebox.showinfo("ERROR", "User does not exist!")
        elif not bcrypt.checkpw(password.encode('utf-8'), self.users[user_index].passwordHash):
            messagebox.showinfo("ERROR", "Incorrect password!")
        else:
            messagebox.showinfo("Success", "Log in was successful")
            self.current_user = self.users[user_index]
            self.authentication_over = True

    def binary_search_users(self, username):
        low, high = 0, len(self.users) - 1
        while low <= high:
            mid = (low + high) // 2
            mid_username = self.users[mid].username
            if mid_username == username:
                return mid
            elif mid_username < username:
                low = mid + 1
            else:
                high = mid - 1
        return None

if __name__ == "__main__":
    from new_main import create_root
    from user_record import UserRecord
    root = create_root()

    authentication_instance = UserAuthentication(root, UserRecord)
    authentication_instance.authenticate_user()

    while (not authentication_instance.completed_authentication) and (not authentication_instance.skipped_authentication):
        root.update()

    if authentication_instance.current_user is None:
        print("Authentication skipped")
    else:
        print("User authenticated:", authentication_instance.current_user)

    root.mainloop()