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
        self.speed = speed*scale
        self.health = health
        self.remove = False
        
        self.maxdistance = 20*scale
        self.mindistance = 10*scale
        
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
            self.image = BetterImage("resources/textures/enemies/bosses/1.png", (self.x, self.y), scale, scale)
            self.hitS = pg.mixer.Sound('resources/sounds/enemies/FHit.wav')
        elif self.type == 4:
            self.image = BetterImage("resources/textures/enemies/rockele/1.png", (self.x, self.y), scale, scale)
            self.hitS = pg.mixer.Sound('resources/sounds/enemies/rHit.wav')
            
        self.hitS.set_volume(0.25)
        

    def update(self,window,playerpos,enemy_list,player,projectile_list,fireDamage,pHandler,waterDamage,lightDamage,shadowDamage,shadowOrbs,pet_list,shake):
        if self.health < 0:
            for r in range(shadowOrbs):
                if R.random() < 0.1:
                    pHandler.add_projectile(projectile(self.scale,(self.x,self.y),None,0,7))
                    
            self.remove = True

        self.move(playerpos,enemy_list,player,shake)
            
        self.draw(window)
        
        if self.cooldown <= 0 and self.type == 2:
            self.cooldown = 60
            pHandler.add_projectile(projectile(self.scale,(self.x,self.y),playerpos,0,2))
        elif self.type == 3 and self.cooldown <= 0:
            self.cooldown = 5
            pHandler.add_projectile(projectile(self.scale,(self.x+8*self.scale,self.y-32*self.scale),playerpos,0,8))
        else:
            self.cooldown -= 1

        for pets in pet_list:
            if dist(self.x,self.y,pets.x,pets.y) <= 25*self.scale:
                if pets.type == 0:
                    self.health -= 2+fireDamage
                    self.hitS.play()

        for proj in projectile_list:
            if dist(self.x,self.y,proj.x,proj.y) <= 10*self.scale:
                if proj.type == 0:
                    self.health -= 2+lightDamage
                    self.hitS.play()
                elif proj.type == 1:
                    if self.type != 4:
                        self.health -= 0.2+fireDamage
                        self.hitS.play()
                    else:
                        self.health -= 0.1+fireDamage
                        self.hitS.play()
                elif proj.type == 3:
                    if self.type != 4:
                        self.health -= 5
                        self.hitS.play()
                    else:
                        self.health -= 1
                        self.hitS.play()
                elif proj.type == 4:
                    if self.type != 4:
                        self.health -= 10+fireDamage
                        self.hitS.play()
                    else:
                        self.health -= 7+fireDamage
                        self.hitS.play()
                elif proj.type == 6:
                    self.health -= 7+waterDamage
                    self.hitS.play()
                elif proj.type == 7:
                    self.health -= 3+shadowDamage
                    self.hitS.play()

    def hit(self,pHandler,scale,wave):
        self.hitS.play()
        self.pHandler = pHandler
        
        if len(wave.enemy_list) <= 25:
            for i in range(R.randrange(1,7)):
                if not self.type == 3:
                    pHandler.add_partical(partical((self.x+(8*self.scale),self.y+(8*self.scale)),scale,wave,self.type))
                else:
                    pHandler.add_partical(partical((self.x+(8*self.scale),self.y+(8*self.scale)),scale,wave,self.type))
        else:
            pHandler.add_partical(partical((self.x+(8*self.scale),self.y+(8*self.scale)),scale,wave,self.type))


    def move(self,playerpos,enemy_list,player,shake):
        
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

        if not self.type == 3:
            self.image.move((self.x+shake[0],self.y+shake[1]))
        else:
            self.image.move((self.x+shake[0],self.y-(64*self.scale)+shake[1]))
        if dist(self.x,self.y,playerpos[0],playerpos[1]) <= 10*self.scale:
            player.hit(10)

    def draw(self,window):
        self.image.draw(window)





def dist(x1,y1,x2,y2):
    return(M.sqrt(M.pow((x2-x1),2)+M.pow((y2-y1),2)))