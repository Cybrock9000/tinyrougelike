import random as R

class Player:
    def __init__(self):
        self.health = 100
        self.imunityFrames = 20 #1/2 sec
        self.i = 0
        self.dead = False
        self.waterbubblechance = 0

    def update(self):
        self.i += 1
        if self.health <= 0:
            self.dead = True

    def hit(self,amount):
        if self.imunityFrames < self.i:
            self.i = 0
            if R.random() > self.waterbubblechance:
                self.health -= amount