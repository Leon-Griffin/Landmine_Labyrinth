class UserRecord():

    def __init__(self, username, passwordHash, bestGame, admin, dateJoined):
        self.username = username
        self.password_hash = passwordHash
        self.best_game = bestGame
        self.admin = admin == 1
        self.date_joined = dateJoined
        
    def is_admin(self):
        return self.admin

    def __repr__(self):
        return self.username