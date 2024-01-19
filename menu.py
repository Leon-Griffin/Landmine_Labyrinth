from tkinter import Frame, Button, Label, font, ttk, messagebox
    
class Menu:

    def __init__(self, root, database, users, games, PlayGame, user):
        self.root = root
        self.database = database
        self.users = users
        self.games = games
        self.PlayGame = PlayGame
        self.user = user

    def create_menu(self):
        menu_frame = Frame(self.root)
        menu_frame.pack()
        Label(menu_frame, text="Welcome\n'"+str(self.user)+"'", font=font.Font(family="Fixedsys", size=20, weight="bold")).pack(padx=10, pady=10)

        if self.user.admin:
            Button(menu_frame, text="View Users", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda:[menu_frame.destroy(), self.view_users()]).pack(padx=10, pady=10)

        else:
            Button(menu_frame, text="Delete account", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=self.delete_user).pack(padx=10, pady=10)

        Button(menu_frame, text="Personal Leaderboard", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda:[menu_frame.destroy(), self.view_games]).pack(padx=10, pady=10)

        Button(menu_frame, text="Play Game", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda:[menu_frame.destroy(), self.PlayGame(self.root)]).pack(padx=10, pady=10)

    def view_users(self):
        view_users_frame = Frame(self.root)
        view_users_frame.pack()

        for counter, user in enumerate(self.users):
            Label(view_users_frame, text=user, font=font.Font(family="Fixedsys", size=20, weight="bold")).grid(row=counter, column=0)
            Button(view_users_frame, text="view games", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda:[view_users_frame.destroy(), self.view_games(user)]).grid(row=counter, column=1)
            Button(view_users_frame, text="delete user", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda:[view_users_frame.destroy(), self.delete_user(user)]).grid(row=counter, column=2)

        Button(view_users_frame, text="Return to menu", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda:[view_users_frame.destroy(), self.create_menu()]).grid(column=1)

    def view_games(self, user=None):
        if user is None:
            user = self.user

        userGames = [game for game in self.games if game.username == user.username]

        view_games_frame = Frame(self.root)
        view_games_frame.pack()

        # Create Treeview
        tree = ttk.Treeview(view_games_frame, columns=("GameID", "Date Completed", "Time Taken", "Bomb Frequency", "Board Size", "Lives"))
        tree.heading("GameID", text="Game ID")
        tree.heading("Date Completed", text="Date Completed")
        tree.heading("Time Taken", text="Time Taken")
        tree.heading("Bomb Frequency", text="Bomb Frequency")
        tree.heading("Board Size", text="Board Size")
        tree.heading("Lives", text="Lives")

        # Insert data into the Treeview
        for counter, game in enumerate(userGames, start=1):
            tree.insert("", counter, text=f"Game {counter}", values=(game.GameID, game.dateCompleted, game.timeTaken, game.bombFrequency, game.boardSize, game.lives))

        # Pack the Treeview
        tree.grid(row=0, column=0, padx=10, pady=10, columnspan=7)

        # Button to return to the main menu
        Button(view_games_frame, text="Return to menu", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda: [view_games_frame.destroy(), self.create_menu()]).grid(row=len(userGames) + 1, column=3, columnspan=3, padx=10, pady=10)

    def delete_user(self, user=None):
        if user is None:
            user = self.user
        if messagebox.askokcancel("Confirm Deletion", f"Are you sure you want to delete user {user}?"):
            self.database.delete_user(user)
        self.create_menu()