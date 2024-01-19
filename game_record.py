class GameRecord():
    
    def __init__(self, GameID, username, dateCompleted, timeTaken, bombFrequency, boardSize, lives):
        self.GameID = GameID
        self.username = username

        self.date_completed = dateCompleted
        self.timeTaken = timeTaken
        
        self.bomb_frequency = bombFrequency
        self.board_size = boardSize
        self.lives = lives

    def __repr__(self):
        return f"Game {self.GameID}, completed on the date {self.date_completed}"