from tkinter import Button, font, DISABLED
import random

# defining the buttons class, for the buttons on the gameboard
class GameButton:

    # initialising the button, with all the related info to do with this specific button (clicked, flag, bomb etc...)
    def __init__(self, game, row, col):
        self.game = game
        
        self.unclicked_colour = "gray"
        self.zero_bomb_colour = "systembuttonface"
        self.clicked_colour = "systembuttonface"

        self.button = Button(game.game_frame, width=2, height=1, command=lambda: self.handle_click(True), font=font.Font(family="Fixedsys", size=20, weight="bold"), bg=self.unclicked_colour)
        self.button.bind("<Button-3>", lambda event: self.handle_right_click())

        self.clicked = False
        self.flagged = False
        self.row = row
        self.col = col

        self.bomb = random.randint(1, 100) <= self.game.bomb_frequency
        if self.bomb:
            self.game.number_of_bombs += 1

    # handle the user clicking the button
    def handle_click(self, manuallyClicked: bool) -> None:
        if manuallyClicked:
            self.game.clicked_buttons += 1

        # making sure that the current button is not flagged or clicked already
        if not self.clicked and not self.flagged:
            self.game.revealed_buttons += 1
            
            self.clicked = True

            # handling the first click
            if self.game.revealed_buttons == 1:
                self.game.first_click(self)

            # handling a zero bomb square
            if self.game.count_bombs(self) == 0:
                self.game.reveal_neighbours(self)

            # handling a non bomb button
            if not self.bomb:
                
                bombcount = self.game.count_bombs(self)
                if bombcount == 0:
                    self.button.config(relief="sunken", state=DISABLED, text="", bg=self.zero_bomb_colour)
                else:
                    self.button.config(relief="sunken", state=DISABLED, text=str(bombcount), bg=self.clicked_colour)
           
            # handling a bomb button
            else:
                self.button.config(relief="sunken", state=DISABLED, text="B", bg="red", fg="white")
                self.game.lives_lost += 1
                if self.game.lives_lost == self.game.lives:
                    self.game.game_over("lose")
               
            # handle win condition
            if self.game.revealed_buttons == (self.game.board_size*self.game.board_size) - self.game.number_of_bombs + self.game.lives_lost:

                self.game.game_over("win")

    # handle the user flagging a button
    def handle_right_click(self) -> None:
        if not self.clicked and not str(self.button['state']) == 'disabled':
            self.flagged = not self.flagged
            if self.flagged:
                self.game.flagged_buttons += 1
                self.button.config(text="F", bg="black", fg="white")
            else:
                self.game.flagged_buttons -= 1
                self.button.config(text="", bg=self.unclicked_colour, fg="black")