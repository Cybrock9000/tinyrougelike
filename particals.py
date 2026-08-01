from CybrocksLibrary import *
import random as R


class partical:
    def __init__(self,pos,scale,enemys,type=0):
        self.x, self.y = pos
        
        self.yv = R.randrange(0,15)
        self.xv = R.randrange(0,25)
        self.vdir = R.randrange(-1,1)
        self.axv = 0
        self.ayv = 0
        self.aayv = 0
        self.remove = False

        if type == 0:
            if len(enemys.enemy_list) >= 25:
                self.image = BetterImage("resources/textures/particals/slimebits2.png", (self.x, self.y), scale, scale)
            else:
                self.image = BetterImage("resources/textures/particals/slimebits.png", (self.x, self.y), scale, scale)
        if type == 1:
            if len(enemys.enemy_list) >= 25:
                self.image = BetterImage("resources/textures/particals/FSblood2.png", (self.x, self.y), scale, scale)
            else:
                self.image = BetterImage("resources/textures/particals/FSblood.png", (self.x, self.y), scale, scale)
        if type == 2:
            if len(enemys.enemy_list) >= 25:
                self.image = BetterImage("resources/textures/particals/shadowbits2.png", (self.x, self.y), scale, scale)
            else:
                self.image = BetterImage("resources/textures/particals/shadowbits.png", (self.x, self.y), scale, scale)



    def update(self,window,scale):
        self.draw(window)
        self.move(scale)



    def draw(self,window):
        self.image.draw(window)



    def move(self,scale):

        if self.axv != self.xv:
            self.x += self.vdir
            self.axv += 1

        if self.ayv != self.yv:
            self.y -= 1
            self.ayv += 1

        if self.axv == self.xv and self.ayv == self.yv:
            if self.aayv != 10:
                self.y += 1
                self.aayv += 1
            else:
                self.remove = True
        self.image.move((self.x,self.y))