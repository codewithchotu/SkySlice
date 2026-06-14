import json
import os

class Score:

    def __init__(self):
        self.value = 0
        self.high_score = 0
        self.load_high_score()

    def add(self, points=1):
        self.value += points
        if self.value > self.high_score:
            self.high_score = self.value
            self.save_high_score()
            
    def load_high_score(self):
        if os.path.exists("highscore.json"):
            try:
                with open("highscore.json", "r") as f:
                    self.high_score = json.load(f).get("high_score", 0)
            except:
                pass
                
    def save_high_score(self):
        try:
            with open("highscore.json", "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except:
            pass