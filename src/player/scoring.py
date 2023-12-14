
import sqlite3
import pygame
pygame.init
class ScoringHandler():

    def __init__(self):
        # DB
        self.conn = sqlite3.connect("game.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS scores (Score REAL)")
        self.conn.commit()

    # get the best scores
    def get_score(self):
        self.cursor.execute("SELECT score FROM scores ORDER BY score DESC LIMIT 3")
        best_score = self.cursor.fetchall()
        if best_score != []:
            best_score_format = f"#1: {int(best_score[0][0])}"
        else: best_score_format = f"No Score"

        return best_score_format
    
        # save the score in the db
    def save_score(self, game_score):
        # save the score in the db
        print(game_score)
        self.cursor.execute(f"INSERT INTO scores VALUES ({game_score})")
        self.conn.commit()