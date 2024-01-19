class UserRecord():

    def __init__(self, username, passwordHash, bestGame, admin, dateJoined):
        self._username = username
        self._password_hash = passwordHash
        self._best_game = bestGame
        self._admin = admin == 1
        self._date_joined = dateJoined
        
    def is_admin(self):
        return self._admin

    def __repr__(self):
        return self.username