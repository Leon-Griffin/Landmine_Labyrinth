from tkinter import Frame, IntVar, Label, Button, Scale, font

class GameCustomisation:

    def __init__(self, root):
        self.root = root
        self.options_completed = False

        self.board_size = IntVar()
        self.bomb_frequency = IntVar()
        self.lives = IntVar()

    def get_options(self):
        self.gameCustomisationFrame = Frame(self.root)
        self.gameCustomisationFrame.pack()

        Label(self.gameCustomisationFrame, font=font.Font(family="Fixedsys", size=30, weight="bold", underline=True), text="Game Customisation").pack(anchor="n", pady=10)
        self.presetsFrame = Frame(self.gameCustomisationFrame)
        self.presetsFrame.pack()

        def easy_mode():
            self.bomb_frequency.set(10)
            self.lives.set(3)

        def medium_mode():
            self.bomb_frequency.set(20)
            self.lives.set(2)

        def hard_mode():
            self.bomb_frequency.set(25)
            self.lives.set(1)

        # easy difficulty button
        Button(self.presetsFrame, font=font.Font(family="Fixedsys", size=20, weight="bold"), text="Easy", command=easy_mode).grid(row=0, column=0)

        # medium difficulty button
        Button(self.presetsFrame, font=font.Font(family="Fixedsys", size=20, weight="bold"), text="Medium", command=medium_mode).grid(row=0, column=1)

        # hard difficulty button
        Button(self.presetsFrame, font=font.Font(family="Fixedsys", size=20, weight="bold"), text="Hard", command=hard_mode).grid(row=0, column=2)

        # frame to hold setting sliders
        self.sliderFrame = Frame(self.presetsFrame)
        self.sliderFrame.grid(row=1, columnspan=3)

        # Create sliders
        boardsize_slider = Scale(self.sliderFrame, label="Board Size", from_=9, to=21, orient="horizontal", length=250, variable=self.board_size)
        boardsize_slider.grid(row=0, padx=10, pady=5)

        bomb_frequency_slider = Scale(self.sliderFrame, label="Bomb Frequency (%)", from_=5, to=95, orient="horizontal", length=250, variable=self.bomb_frequency)
        bomb_frequency_slider.grid(row=1, padx=10, pady=5)

        lives_slider = Scale(self.sliderFrame, label="Lives", from_=1, to=5, orient="horizontal", length=250, variable=self.lives)
        lives_slider.grid(row=2, padx=10, pady=5)

        # button to continue to game
        Button(self.gameCustomisationFrame, text="Play Game", font=font.Font(family="Fixedsys", size=20, weight="bold"), command=lambda: [self.gameCustomisationFrame.destroy(), setattr(self, "options_completed", True)]).pack(padx=10, pady=10)


# Run the code if this script is the main program.
if __name__ == "__main__":
    from new_main import create_root

    root = create_root()

    game_customisation_instance = GameCustomisation(root)
    game_customisation_instance.get_options()
    game_options = game_customisation_instance.board_size.get(), game_customisation_instance.bomb_frequency.get(), game_customisation_instance.lives.get()

    while not game_customisation_instance.options_completed:
        root.update()

    board_size, bomb_frequency, lives = game_options
    print(f"Board Size: {board_size}\nBomb Frequency: {bomb_frequency}%\nLives: {lives}")
    root.mainloop()