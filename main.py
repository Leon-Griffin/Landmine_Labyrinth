"""
Main entry point for Landmine Labyrinth game
Leon Griffin
"""

# Tkinter imports
try:
    # Importing necessary classes from tkinter
    from tkinter import Tk, Label, font, messagebox
    # importing error from tkinter
    from tkinter import TclError 
except Exception as e:
    print(f"An error occured importing display: {e}")
    quit()

# importing datetime to store date completed for games
try: 
    from datetime import datetime
    datetime_imported = True
except: datetime_imported = False

# Importing classes to represent the records from the 'Users' and 'Games' tables respectively
try:
    from user_record import UserRecord
    from game_record import GameRecord
    synchronised = True
except: synchronised = False

# Importing the database class file
try: from database import Database
except Exception as e:
    print(f"An error occured importing database: {e}")
    synchronised = False

# Importing user authentication class file
try: from user_authentication import UserAuthentication
except Exception as e:
    print(f"An error occured importing user authentication: {e}")
    synchronised = False

# Importing main menu class file
try: from menu import Menu
except Exception as e:
    print(f"An error occured importing main menu: {e}")
    synchronised = False

# Importing game component class files
try:
    from game_options import GameCustomisation
    from gameplay import Gameplay
    from game_over import GameOver 
except Exception as e:
    print(f"An error occured importing game components: {e}")
    quit()


# Main structure of the code
def main():
    root = create_root()
    
    if synchronised:
        database, users, games = open_and_read_database()
        
        if database.connected:
            current_user = authenticate_user(root, database, users)
            
            if current_user is not None:
                menu_instance = Menu(root, database, users, games, play_game, current_user)
                menu_instance.create_menu()
                while window_exists(root):
                    root.update()
                
            else:
                play_game(root, current_user=current_user)
                
        else:
            play_game(root, current_user=current_user)
            
        database.close_connection()
        
    else:
        play_game(root)
    
    root.mainloop()
        
    
# Connecting to database and reading tables
def open_and_read_database() -> tuple[Database, list[UserRecord], list[GameRecord]]:
    database_instance = Database("Landmine_Labyrinth.db", UserRecord, GameRecord)
    database_instance.connect()
    
    if database_instance.connected:
        print("Connection to 'Landmine_Labyrinth.db' successful.")
        users = database_instance.read_users()
        games = database_instance.read_games()
        
    else:
        print("Connection to 'Landmine_Labyrinth.db' failed, file does not exist.")
        users, games = None, None
        
    return database_instance, users, games
      

# Authenticating the user, can be skipped
def authenticate_user(root:Tk, database:Database, users:list[UserRecord]) -> UserRecord:
    authentication_instance = UserAuthentication(root, UserRecord, database, users)
    authentication_instance.authenticate_user()
    
    while not authentication_instance.authentication_over and window_exists(root):
        root.update()
        
    return authentication_instance.current_user


# Creating the default window
def create_root() -> Tk:
    root = Tk()
    root.title("Landmine Labyrinth")
    root.config(bg="gray")

    # Display the title
    Label(root, text="Landmine Labyrinth", font=font.Font(family="Fixedsys", size=40, weight="bold"), bg="gray").pack(anchor="n", padx=25, pady=20)
    return root


# Function to play the game, allows for repeated playing as it passes itself as an argument
def play_game(root:Tk, database: Database = None, current_user: UserRecord = None, game_options: tuple[int] = None) -> GameRecord:

    # function to save a game to the database
    def save_game(database: Database, game: GameRecord, user: UserRecord) -> None:
        if game is not None:
            database.add_game(user, game)

    if window_exists(root):

        if game_options is None:

            game_customisation_instance = GameCustomisation(root)
            game_customisation_instance.get_options()

            while not game_customisation_instance.options_completed and window_exists(root):
                root.update()
                
            game_options = game_customisation_instance.board_size.get(), game_customisation_instance.bomb_frequency.get(), game_customisation_instance.lives.get()

        game = Gameplay(root, game_options)
        game.play_game()

        if datetime_imported and current_user is not None and game.end_condition == "win":
            game = GameRecord(current_user.username, datetime.today(), game.time_taken, game.bomb_frequency, game.board_size, game.lives)
            save_game(database, game, current_user)
        
        while not game.game_over_flag and window_exists(root):
            root.update()
        
        if game.end_condition is not None:
            GameOver(game, play_game, current_user).end_game()


# Try-except function to check if the window exists
def window_exists(window: Tk) -> bool:
    try: window.winfo_exists(); return True
    except TclError: return False


# Calls the main code structure
if __name__ == "__main__": main()