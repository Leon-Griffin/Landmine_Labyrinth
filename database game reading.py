from database import Database
from user_record import UserRecord
from game_record import GameRecord

mydatabase = Database("Landmine_Labyrinth.db", UserRecord, GameRecord)

mydatabase.connect()

games = mydatabase.read_games()

for game in games:
    print(game)