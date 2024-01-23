from tkinter import Toplevel, Label, Frame, font, Button, ttk, messagebox

class GameOver:

    def __init__(self, game, play_game, current_user=None):
        self.game = game
        self.end_condition = game.end_condition
        self.play_game = play_game
        self.current_user = current_user

    # display the game over menu (play again, view stats, quit game, and back to options)
    def end_game(self, platform=None):
        
        if platform is None:
            # creating a Toplevel widget to display game over
            end_message = Toplevel(self.game.root)
            end_message.title("Game Over")
        
        else:
            # creating a frame to display game over
            end_message = Frame(self.game.root)
            end_message.pack()

        # display loss message
        if self.end_condition == "lose":
            Label(end_message, text="You Lost", font=font.Font(family="Fixedsys", size=30, weight="bold", underline=True)).grid(row=0, columnspan=2, padx=15, pady=15)

        # display win message
        elif self.end_condition == "win":
            Label(end_message, text="You Won!", font=font.Font(family="Fixedsys", size=30, weight="bold", underline=True)).grid(row=0, columnspan=2, padx=15, pady=15)

        # Display a button to view the stats of the game
        Button(end_message, font=font.Font(family="Fixedsys", size=20, weight="bold"), text="View Stats", command=lambda: [end_message.destroy(), self.view_stats()]).grid(row=1, column = 0, padx=25, pady=10)

        # display a button to retry the same settings
        Button(end_message, font=font.Font(family="Fixedsys", size=20, weight="bold"), text="New Game", command=lambda: [end_message.destroy(), self.game.game_frame.destroy(), self.play_game(self.game.root, self.current_user, (self.game.board_size, self.game.bomb_frequency, self.game.lives))]).grid(row=1, column = 1, padx=25, pady=10)

        # display a button to quit the game
        Button(end_message, font=font.Font(family="Fixedsys", size=20, weight="bold"), text="Quit Game", command=lambda:[messagebox.showinfo("Landmine Labyrinth", "Thank you for playing!"), self.game.root.destroy()]).grid(row=2, column = 0, padx=25, pady=10)

        # display a button to return to game settings
        Button(end_message, font=font.Font(family="Fixedsys", size=20, weight="bold"), text="Return to options", command=lambda: [end_message.destroy(), self.game.game_frame.destroy(), self.play_game(self.game.root, self.current_user)]).grid(row=2, column = 1, padx=25, pady=10)

    # window to view stats such as time taken and buttons clicked etc
    def view_stats(self):
        self.game.game_frame.destroy()
        total_buttons = self.game.board_size*self.game.board_size
    
        # Create statsFrame
        statsFrame = Frame(self.game.root)
        statsFrame.pack()

        # Label for the heading
        Label(statsFrame, text="Your Statistics", font=font.Font(family="Fixedsys", size=30, weight="bold", underline=True)).pack()

        # statistics to show
        game_stats = {
            "Time taken":str(self.game.time_taken),
            " ":" ",
            "Buttons clicked": self.game.clicked_buttons,
            "Buttons Revealed": self.game.revealed_buttons,
            "Buttons flagged": self.game.flagged_buttons,
            "Buttons left": (total_buttons-(self.game.revealed_buttons+self.game.flagged_buttons)),
            "Completed": str(int((((self.game.revealed_buttons+self.game.flagged_buttons)/total_buttons)*100))) + "%",
            "  ":"  ",
            "Board size": str(self.game.board_size)+" x "+str(self.game.board_size),
            "Bomb Frequency (%)": self.game.bomb_frequency,
            "Lives": self.game.lives
        }

        # Create a Treeview widget inside statsFrame
        tree = ttk.Treeview(statsFrame, columns=("Statistic", "Value"), show="headings")

        # Define column headings
        tree.heading("Statistic", text="STATISTIC")
        tree.heading("Value", text="VALUE")

        # Set column widths
        tree.column("Statistic", width=150, anchor="center")
        tree.column("Value", width=150, anchor="center")

        # Pack the Treeview widget
        tree.pack(fill='both', expand=True)

        # Insert data into the Treeview
        for stat, value in game_stats.items():
            tree.insert("", "end", values=(stat, value))
            
        # create a back button
        Button(statsFrame, text="Back", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda:[statsFrame.destroy(), self.end_game("root")]).pack(pady=10)