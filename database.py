import sqlite3
import os

class Database:

    # Initialisation of the database, requires a file path as a string, for example: "database_file.db"
    # Also takes arguments UserRecord and GameRecord which are the structures I'm using to represent records from the Users and Games tables respectively
    def __init__(self, filePath, UserRecord, GameRecord):

        self.filePath = filePath
        self.UserRecord = UserRecord
        self.GameRecord = GameRecord
        self.connected = False
        self.conn = None
        self.cursor = None

    # Establish a connection to the SQLite database.
    def connect(self):
        if os.path.exists(self.filePath):
            self.conn = sqlite3.connect(self.filePath)
            self.cursor = self.conn.cursor()
            self.connected = True

    # Close the connection to the database
    def close_connection(self):
        if self.connected:
            self.conn.close()
            self.connected = False

    # Reads contents of the Users table into an array of 'UserRecords'
    def read_users(self) -> list:
        self.cursor.execute("SELECT * FROM Users")
        userDetails = self.cursor.fetchall()

        users = []
        for details in userDetails:
            username, passwordHash, bestGame, admin, dateJoined = details
            users.append(self.UserRecord(username, passwordHash, bestGame, admin, dateJoined))

        # Sort users by username using insertion sort method
        self.insertion_sort(users, "username")

        return users

    # Reads contents of the Games table into an array of 'GameRecords'
    def read_games(self) -> list:
        self.cursor.execute("SELECT * FROM Games")
        gameDetails = self.cursor.fetchall()

        games = []
        for details in gameDetails:
            GameID, username, dateCompleted, timeTaken, bombFrequency, boardSize, lives = details
            games.append(self.GameRecord(username, dateCompleted, timeTaken, bombFrequency, boardSize, lives, GameID))

        # Sort games by GameID using insertion sort method
        self.insertion_sort(games, "game_id")

        return games

    # Sort an array of objects based on a specified property, intended to sort the arrays from read_users and read_games before they are returned
    def insertion_sort(self, array: list, property: str):
        for i in range(1, len(array)):
            key = array[i]
            j = i - 1

            # Extract the property value for sorting
            key_property = getattr(key, property)

            while j >= 0 and getattr(array[j], property) > key_property:
                array[j + 1] = array[j]
                j -= 1

            array[j + 1] = key

    # Deletes the user provided from the 'Users' table, 'user' below is an instance of the 'UserRecord' class
    def delete_user(self, user):
        query = "DELETE FROM Users WHERE Username = ?"
        self.cursor.execute(query, (user.username,))
        self.conn.commit()

    # Adds one user to the 'Users' table, 'user' below is an instance of the 'UserRecord' class
    def add_user(self, user):
        query = "INSERT INTO Users (Username, PasswordHash, BestGame, Admin, DateJoined) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (user.username, user.password_hash, user.best_game, user.admin, user.date_joined))
        self.conn.commit()

    # Adds one game to the 'Games' table, 'game' below is an instance of the 'GameRecord' class
    def add_game(self, user, game):
        query = "INSERT INTO Games (Username, DateCompleted, TimeTaken, BombFrequency, BoardSize, Lives) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (user.username, game.date_completed, game.time_taken, game.bomb_frequency, game.board_size, game.lives))
        self.conn.commit()

# This if statement is true when this code is run directly, if this is the case the database will be entirely reset, adding only the default admin user
if __name__ == "__main__":
    try:
        import bcrypt
        from datetime import date

    except Exception as e:
        print(f"Imports unsuccessful, error: {e}")
        quit()

    # get todays date
    currentDate = date.today()
    print("Today's date:", currentDate)

    # define database file
    database_file_path = 'Landmine_Labyrinth.db'

    # Create/connect to Landmine_Labyrinth file
    conn = sqlite3.connect(database_file_path)
    print(f"\nConnection to '{database_file_path}' file successful.")

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    if not input(f"\nThis code will drop the tables in the '{database_file_path}' file if they exist and reset them with the default admin as the only user.\nDo you want to continue? y/n: ").lower() == "y":
        exit()

    # Reset the database file
    try:
        cursor.execute('''
            DROP TABLE Users;
            ''')
        cursor.execute('''
            DROP TABLE Games
            ''')

        print(f"\nTables 'Users' and 'Games' have been deleted.")
    except sqlite3.OperationalError:
        print("\nTables 'Users' and 'Games' do not exist")

    # Create users table
    cursor.execute('''
        CREATE TABLE Users (
            Username VARCHAR(15) PRIMARY KEY,
            PasswordHash VARCHAR(64) NOT NULL,
            BestGame INTEGER REFERENCES Games(GameID),
            Admin BOOLEAN DEFAULT FALSE,
            DateJoined DATE NOT NULL
        )
    ''')

    # Create Games table
    cursor.execute('''
        CREATE TABLE Games (
            GameID INTEGER PRIMARY KEY,
            Username VARCHAR(15) REFERENCES Users(Username),
            DateCompleted DATE,
            TimeTaken TIME,
            BombFrequency INTEGER CHECK (BombFrequency >= 1 AND BombFrequency <= 99),
            BoardSize INTEGER,
            Lives INTEGER
        )
    ''')

    print("\nEmpty tables 'Users' and 'Games' have been added")

    # Hash the password
    hashed_password = bcrypt.hashpw("admin1".encode('utf-8'), bcrypt.gensalt())

    # Add one admin account
    cursor.execute("INSERT INTO Users (Username, PasswordHash, Admin, DateJoined) VALUES (?, ?, ?, ?)", ('admin', hashed_password, True, currentDate))
    print("\nDefault admin user has been added\n")

    # Commit changes to the database
    conn.commit()