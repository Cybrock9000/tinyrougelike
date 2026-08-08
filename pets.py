import pygame as pg
from CybrocksLibrary import *
import math as M
import random as R
from particals import *
from projectiles import *

class pet:
    def __init__(self, pos, scale, speed, health,type=0):
        self.song = pg.mixer.Sound('resources/music/pets/requiem.wav')
        self.song.set_volume(1)
        self.song.play(-1)
        self.x, self.y = pos
        self.type = type
        self.scale = scale
        self.cooldown = R.randrange(10,60)
        self.speed = speed*scale
        self.health = health
        self.remove = False
        self.dir = 'R'
        
        self.target = None
        
        if self.type == 0:
            self.image = BetterImage("resources/textures/pets/requiem/1.png", (self.x, self.y), scale, scale)
            self.hitS = pg.mixer.Sound('resources/sounds/enemies/sHit.wav')
        elif self.type == 1:
            self.image = BetterImage("resources/textures/enemies/frostSpider/frostSpider.png", (self.x, self.y), scale, scale)
            self.hitS = pg.mixer.Sound('resources/sounds/enemies/FShit.wav')
        

    def update(self,window,playerpos,enemy_list,player,projectile_list,fireDamage,pHandler,waterDamage,lightDamage,shadowDamage,shadowOrbs,shake):
        if self.dir == 'R':
            self.image.draw(window)
        else:
            self.image.draw(window,'L')
            
        
        if self.target not in enemy_list:
            self.target = R.choice(enemy_list)
        
        
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        
        self.angle = M.degrees(M.atan2(dy, dx))
        
        rad = M.radians(self.angle)

        if (M.cos(rad) * self.speed) <= 0:
            self.dir = 'L'
        else:
            self.dir = 'R'

        if dist(self.x,self.y,self.target.x,self.target.y) >= 100*self.scale and self.type == 0:
            self.speed = 4*self.scale
        elif self.type == 0:
            self.speed = 0.5*self.scale

        self.x += M.cos(rad) * self.speed
        self.y += M.sin(rad) * self.speed
        
        self.image.centermove((self.x+shake[0], self.y+shake[1]))







def dist(x1,y1,x2,y2):
    return(M.sqrt(M.pow((x2-x1),2)+M.pow((y2-y1),2)))