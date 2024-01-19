"""
Main entry point for Landmine Labyrinth game
Leon Griffin
"""

# Importing necessary classes from tkinter
from tkinter import Tk, Label, font

# importing error from tkinter to be caught (line something)
from tkinter import TclError

# Importing classes to represent the records from the 'Users' and 'Games' tables respectively
from user_record import UserRecord
from game_record import GameRecord

# Importing the files that make up the code
try:
    from database import Database
    from user_authentication import UserAuthentication
    from menu import Menu
except:
    pass
from gameplay import PlayGame


# function to create the default window used throughout the code
def create_root():
    root = Tk()
    root.title("Landmine Labyrinth")
    root.config(bg="gray")

    # Display the title
    Label(root, text="Landmine Labyrinth", font=font.Font(family="Fixedsys", size=40, weight="bold"), bg="gray").pack(anchor="n", padx=25, pady=20)
    return root

def connect_to_database():
    try:
        database = Database("Landmine_Labyrinth.db", UserRecord, GameRecord)
        connected = database.connect()

        if connected:
            print("Connection to 'Landmine_Labyrinth.db' successful.")
            users = database.read_users()
            games = database.read_games()
            return database, users, games
        
        else:
            print("Connection to 'Landmine_Labyrinth.db' failed, file does not exist.")
            return None, None, None

    except Exception as e:
        print(f"Error during database connection: {e}")
        return None, None, None

def authenticate_user(root, users, database):
    signed_in = False
    user_quit_authentication = False

    while not signed_in and not user_quit_authentication:
        try:
            user_index, users = UserAuthentication(root, users, database).authenticate_user()
            signed_in = True

        except TypeError:
            pass

        except TclError:
            user_quit_authentication = True
            user_index = None
            root = create_root()

    return signed_in, users[user_index], users, root

def main():
    root = create_root()

    # Connect to the database
    database, users, games = connect_to_database()
    
    if database is None:
        game = PlayGame(root)

    else:
        signed_in, user, users, root = authenticate_user(root, users, database)

        if not signed_in:
            PlayGame(root)

        else:
            Menu(root, database, users, games, PlayGame, user)

    root.mainloop()

if __name__ == "__main__":
    main()