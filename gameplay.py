from tkinter import Frame
from datetime import datetime
from game_button import GameButton

# defining the minesweeper game object, for when a game is played
class Gameplay:
    
    # creating board with no passed options
    def __init__(self, root, game_options):
        self.root = root
        self.game_over_flag = False

        # button counters - for win condition and stats screen
        self.revealed_buttons = 0
        self.clicked_buttons = 0
        self.flagged_buttons = 0
        self.number_of_bombs = 0

        # game settings
        self.board_size, self.bomb_frequency, self.lives = game_options

        self.lives_lost = 0

    def play_game(self):

        # creating the board within a frame
        try:
            self.game_frame = Frame(self.root)
            self.buttons = []
            self.create_board()

        except Exception as e:
            print(e)

    # logic to create board and fill it with GameButton objects
    def create_board(self):
        self.game_frame.pack()

        # loop for creating and displaying the buttons for this game
        for row in range(self.board_size):
            button_row = []
            for col in range(self.board_size):
                button = GameButton(self, row, col)
                button.button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    # method to count the number of bombs surrounding the current button
    def count_bombs(self, button):
        bomb_count = 0
        
        for r in range(max(0, button.row - 1), min(button.game.board_size, button.row + 2)):
            for c in range(max(0, button.col - 1), min(button.game.board_size, button.col + 2)):
                if self.buttons[r][c].bomb:
                    bomb_count += 1

        return bomb_count
   
    # reveal all neighbours of a button
    def reveal_neighbours(self, button):
        for row in range(max(0, button.row - 1), min(self.board_size, button.row + 2)):
            for col in range(max(0, button.col - 1), min(self.board_size, button.col + 2)):
                self.buttons[row][col].handle_click(False)

    # handle the first click of the game
    def first_click(self, button):
        self.start_time = datetime.now()
        
        for row in range(max(0, button.row - 1), min(self.board_size, button.row + 2)):
            for col in range(max(0, button.col - 1), min(self.board_size, button.col + 2)):
                if self.buttons[row][col].bomb:
                    self.buttons[row][col].bomb = False
                    self.number_of_bombs -= 1

        for row in range(max(0, button.row - 1), min(self.board_size, button.row + 2)):
            for col in range(max(0, button.col - 1), min(self.board_size, button.col + 2)):
                self.buttons[row][col].handle_click(False)

    # for when end of game condition is met
    def game_over(self, end_condition):

        self.end_condition = end_condition
                        
        # record time taken
        try:
            self.time_taken = str(datetime.now() - self.start_time).split('.')[0]
            
        except TypeError:
            self.time_taken = str(datetime.now() - datetime.strptime(self.time_taken, "%Y-%m-%d %H:%M:%S.%f")).split('.')[0]

        # freeze all buttons
        [button.button.config(state='disabled') for row in range(self.board_size) for button in self.buttons[row]]
        
        self.game_over_flag = True
    
if __name__ == "__main__":
    from new_main import create_root
    from game_options import GameCustomisation
    from game_over import GameOver

    def play_game(root, game_options=None):

        if game_options is None:

            game_customisation_instance = GameCustomisation(root)
            game_customisation_instance.get_options()

            while not game_customisation_instance.options_completed:
                root.update()
                
            game_options = game_customisation_instance.board_size.get(), game_customisation_instance.bomb_frequency.get(), game_customisation_instance.lives.get()

        game = Gameplay(root, game_options)
        game.play_game()
        
        while not game.game_over_flag:
            root.update()
        
        GameOver(game, play_game).end_game("toplevel")

    root = create_root()
    play_game(root)
    
    root.mainloop()