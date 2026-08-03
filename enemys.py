import pygame as pg
from CybrocksLibrary import *
import math as M
import random as R
from particals import *
from projectiles import *

class enemy:
    def __init__(self, pos, scale, speed, health,type=0):
        self.x, self.y = pos
        self.type = type
        self.scale = scale
        self.cooldown = R.randrange(10,60)
        
        if self.type == 0:
            self.image = BetterImage("resources/textures/enemies/slimes/slimes.png", (self.x, self.y), scale, scale)
            self.hitS = pg.mixer.Sound('resources/sounds/enemies/sHit.wav')
        elif self.type == 1:
            self.image = BetterImage("resources/textures/enemies/frostSpider/frostSpider.png", (self.x, self.y), scale, scale)
            self.hitS = pg.mixer.Sound('resources/sounds/enemies/FShit.wav')
        elif self.type == 2:
            self.image = BetterImage("resources/textures/enemies/forgotten/forgotten.png", (self.x, self.y), scale, scale)
            self.hitS = pg.mixer.Sound('resources/sounds/enemies/FHit.wav')
        elif self.type == 3:
            self.image = BetterImage("resources/textures/enemies/forgotten/forgotten.png", (self.x, self.y), 2*scale, 2*scale)
            self.hitS = pg.mixer.Sound('resources/sounds/enemies/FHit.wav')
            
        
        self.speed = speed*scale
        self.health = health
        self.remove = False

        self.maxdistance = 20*scale
        self.mindistance = 10*scale
        

    def update(self,window,playerpos,enemy_list,player,projectile_list,fireDamage,pHandler,waterDamage,lightDamage,shadowDamage,shadowOrbs):
        if self.health < 0:
            for r in range(shadowOrbs):
                if R.random() < 0.1:
                    pHandler.add_projectile(projectile(self.scale,(self.x,self.y),None,0,7))
                    
            self.remove = True

        if not self.type == 2:
            self.move(playerpos,enemy_list,player)
            
        self.draw(window)
        
        if self.cooldown <= 0 and self.type == 2:
            self.cooldown = 60
            pHandler.add_projectile(projectile(self.scale,(self.x,self.y),playerpos,0,2))
        elif self.cooldown <= 0 and self.type == 3:
            self.cooldown = 20
            pHandler.add_projectile(projectile(self.scale,(self.x,self.y),(R.randrange(0,400*self.scale),R.randrange(0,400*self.scale)),0,2))
        else:
            self.cooldown -= 1
            
        for proj in projectile_list:
            if dist(self.x,self.y,proj.x,proj.y) <= 10*self.scale:
                if proj.type == 0:
                    self.health -= 2+lightDamage
                    self.hitS.play()
                elif proj.type == 1:
                    self.health -= 0.1+fireDamage
                    self.hitS.play()
                elif proj.type == 3:
                    self.health -= 5
                    self.hitS.play()
                elif proj.type == 4:
                    self.health -= 7+fireDamage
                    self.hitS.play()
                elif proj.type == 6:
                    self.health -= 7+waterDamage
                    self.hitS.play()
                elif proj.type == 7:
                    self.health -= 7+shadowDamage
                    self.hitS.play()

    def hit(self,pHandler,scale,wave):
        self.hitS.play()
        self.pHandler = pHandler
        if len(wave.enemy_list) <= 25:
            for i in range(R.randrange(1,7)):
                pHandler.add_partical(partical((self.x,self.y),scale,wave,self.type))
        else:
            pHandler.add_partical(partical((self.x,self.y),scale,wave,self.type))


    def move(self,playerpos,enemy_list,player):
        
        for enemy in enemy_list:
            if enemy is None:
                continue
            if enemy != self:
                if enemy.type != 2:
                    if dist(self.x,self.y,enemy.x,enemy.y) <= self.maxdistance:
                        if dist(self.x,self.y,enemy.x,enemy.y) <= self.mindistance:
                            if self.x >= enemy.x:
                                self.x += self.speed
                            elif self.x <= enemy.x:
                                self.x -= self.speed
                                                                    
                            if self.y >= enemy.y:
                                self.y += self.speed
                            elif self.y <= enemy.y:
                                self.y -= self.speed
                            
        if self.x >= playerpos[0]:
            self.x -= self.speed
        if self.x <= playerpos[0]:
            self.x += self.speed
                                
        if self.y >= playerpos[1]:
            self.y -= self.speed
        if self.y <= playerpos[1]:
            self.y += self.speed
        self.image.move((self.x,self.y))
        if dist(self.x,self.y,playerpos[0],playerpos[1]) <= 10*self.scale:
            player.hit(10)

    def draw(self,window):
        self.image.draw(window)





def dist(x1,y1,x2,y2):
    return(M.sqrt(M.pow((x2-x1),2)+M.pow((y2-y1),2)))