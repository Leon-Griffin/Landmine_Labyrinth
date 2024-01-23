class GameRecord():
    
    def __init__(self, username, dateCompleted, timeTaken, bombFrequency, boardSize, lives, GameID=None):
        self.game_id = GameID
        self.username = username

        self.date_completed = dateCompleted
        self.time_taken = timeTaken
        
        self.bomb_frequency = bombFrequency
        self.board_size = boardSize
        self.lives = lives

    # represent method for testing
    def __repr__(self):
        return f"Game {self.game_id}, completed on the date {self.date_completed} by user: {self.username}"