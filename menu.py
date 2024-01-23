from tkinter import Frame, Button, Label, font, ttk, messagebox, StringVar

class Menu:

    def __init__(self, root, database, users: list, games: list, play_game: callable, user):
        self.root = root
        self.database = database
        self.users = users
        self.games = games
        self.play_game = play_game
        self.user = user

        # Variable to track the current leaderboard mode (personal or public)
        self.leaderboard_mode = StringVar(value="Public")

    def create_menu(self):
        self.menu_frame = Frame(self.root)
        self.menu_frame.pack()

        Label(self.menu_frame, text=f"Welcome\n'{self.user}'", font=font.Font(family="Fixedsys", size=20, weight="bold")).grid(row=0, columnspan=2, padx=10, pady=10)

        if self.user.is_admin():
            Button(self.menu_frame, text="View Users", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=self.view_users).grid(row=1, columnspan=2, padx=10, pady=10)
        else:
            Button(self.menu_frame, text="Delete Account", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=self.delete_user).grid(row=1, columnspan=2, padx=10, pady=10)

        Button(self.menu_frame, text="Leaderboard", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda: [self.hide_menu(), self.leaderboard()]).grid(row=2, columnspan=2, padx=10, pady=10)
        Button(self.menu_frame, text="Play Game", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=self.play_and_add_game_to_database).grid(row=3, column=1, padx=10, pady=10)
        Button(self.menu_frame, text="Quit", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=self.root.destroy).grid(row=3, column=0, padx=10, pady=10)

    def hide_menu(self):
        self.menu_frame.destroy()

    def view_users(self):
        view_users_frame = Frame(self.root)
        view_users_frame.pack()

        for counter, user in enumerate(self.users):
            Label(view_users_frame, text=user, font=font.Font(family="Fixedsys", size=20, weight="bold")).grid(row=counter, column=0)
            Button(view_users_frame, text="View Games", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda u=user: self.view_games(u)).grid(row=counter, column=1)
            Button(view_users_frame, text="Delete User", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda u=user: self.delete_user(u)).grid(row=counter, column=2)

        Button(view_users_frame, text="Return to Menu", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda: [view_users_frame.destroy(), self.create_menu()]).grid(column=1)

    def leaderboard(self):
        self.leaderboard_frame = Frame(self.root)
        self.leaderboard_frame.pack()

        Button(self.leaderboard_frame, text="Personal Leaderboard", font=font.Font(family="Fixedsys", size=15, weight="bold"), command=lambda: self.switch_leaderboard_mode("Personal")).grid(row=0, column=2)
        Button(self.leaderboard_frame, text="Public Leaderboard", font=font.Font(family="Fixedsys", size=15, weight="bold"), command=lambda: self.switch_leaderboard_mode("Public")).grid(row=0, column=4)

        # Create Treeview
        columns_for_table=("Game ID", "Username", "Date Completed", "Time Taken", "Bomb Frequency", "Board Size", "Lives")
        tree = ttk.Treeview(self.leaderboard_frame, columns=columns_for_table)

        for column in columns_for_table:
            tree.heading(column, text=column)
            tree.column(column, width=100)

        # Insert data into the Treeview
        games_to_display = self.get_games_for_leaderboard(self.user)
        for counter, game in enumerate(games_to_display, start=1):
            tree.insert("", counter, values=(
                game.game_id, game.username, game.date_completed.split(" ")[0], game.time_taken,
                game.bomb_frequency, game.board_size, game.lives))

        # Pack the Treeview
        tree.grid(row=1, column=0, padx=10, pady=10, columnspan=7)  # Adjust columnspan to match the number of columns

        # Button to return to the main menu
        Button(self.leaderboard_frame, text="Return to Menu", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda: [self.leaderboard_frame.destroy(), self.create_menu()]).grid(row=len(games_to_display) + 2, column=3, padx=10, pady=10)

    def switch_leaderboard_mode(self, mode: str):
        self.leaderboard_mode.set(mode)
        self.leaderboard_frame.destroy()
        # Update the leaderboard based on the selected mode
        self.leaderboard()

    def get_games_for_leaderboard(self, user) -> list:
        if self.leaderboard_mode.get() == "Personal":
            return [game for game in self.games if game.username == user.username]
        else:
            return self.games  # Return all games for public leaderboard

    def delete_user(self, user = None):
        if user is None:
            user = self.user
        confirmation_message = f"Are you sure you want to delete user {user}?"
        if messagebox.askokcancel("Confirm Deletion", confirmation_message):
            self.database.delete_user(user)

    def play_and_add_game_to_database(self):
        self.hide_menu()
        game = self.play_game(self.root, self.user)

# sample usage for testing
if __name__ == "__main__":
    from database import Database
    from user_record import UserRecord
    from game_record import GameRecord
    from main import create_root, play_game

    database_instance = Database("Landmine_Labyrinth.db", UserRecord, GameRecord)
    database_instance.connect()
    users = database_instance.read_users()
    games = database_instance.read_games()
    database_instance.close_connection()
    root = create_root()
    menu_instance = Menu(root, database_instance, users, games, play_game, users[0])
    menu_instance.create_menu()
    root.mainloop()