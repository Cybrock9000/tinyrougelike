from  CybrocksLibrary import *
import math as M
import random as R


class projectile:
    def __init__(self,scale,pos,playerpos,pangel=0,type=0):
        self.x, self.y = pos
        self.type = type
        self.angle = 90
        self.speed = 8*scale
        self.scale = scale
        self.dx = 0
        self.dy = 0
        self.remove = False
        if self.type == 0 or self.type == 5:
            self.lifespan = 60 #1 sec
        elif self.type == 1 or self.type == 3 or self.type == 4:
            self.lifespan = 120 #2 sec
        elif self.type == 2:
            self.lifespan = 260 #4 sec
        elif self.type == 6:
            self.lifespan = 6 #1/10th sec
        self.target = None
        if self.type == 0:
            self.image = BetterImage("resources/textures/projectiles/arcane.png", (self.x, self.y), scale, scale)
        elif self.type == 1:
            self.image = BetterImage("resources/textures/projectiles/flame.png", (self.x, self.y), scale, scale)
        elif self.type == 2:
            self.image = BetterImage("resources/textures/projectiles/Eshadow.png", (self.x, self.y), scale, scale)

            dx = playerpos[0] - self.x
            dy = playerpos[1] - self.y
            
            self.angle = M.degrees(M.atan2(dy, dx))
        elif self.type == 3:
            self.image = BetterImage("resources/textures/projectiles/arrow.png", (self.x, self.y), scale, scale)
            self.speed = 4*scale

            self.angle = pangel
        elif self.type == 4:
            self.image = BetterImage("resources/textures/projectiles/farrow.png", (self.x, self.y), scale, scale)
            self.speed = 4*scale
            self.angle = pangel
        elif self.type == 5:
            self.image = BetterImage("resources/textures/projectiles/rain.png", (self.x, self.y), scale, scale)
            self.speed = 2*scale
            self.angle = 145
        elif self.type == 6:
            self.image = BetterImage("resources/textures/projectiles/rsplash.png", (self.x, self.y), scale, scale)
            self.speed = 0 
            self.angle = 0


    def update(self,window,EnemyHandler,pHandler,WaveSys):
        if self.lifespan < 0:
            if self.type == 5:
                pHandler.add_projectile(projectile(self.scale,(self.x,self.y),0,0,6))
            self.remove = True
        else:
             self.lifespan -= 1
            
        self.draw(window)
        if self.type == 0 or self.type == 2 or self.type == 3 or self.type == 4 or self.type == 5:
            self.move(EnemyHandler,pHandler,WaveSys,self.type)
        elif self.type == 1:
            self.angle = R.randrange(0,360)


    def move(self, EnemyHandler, pHandler,WaveSys, type):
        if type == 0:
            if not EnemyHandler.enemy_list:
                return

            if self.target not in EnemyHandler.enemy_list:
                self.target = R.choice(EnemyHandler.enemy_list)

            '''if dist(self.x,self.y,self.target.x,self.target.y) <= 10*self.scale:
                self.target.hit(pHandler,self.scale,WaveSys)
                self.target.health -= 10'''

            dx = self.target.x - self.x
            dy = self.target.y - self.y

            self.angle = M.degrees(M.atan2(dy, dx))

            rad = M.radians(self.angle)

            self.x += M.cos(rad) * self.speed
            self.y += M.sin(rad) * self.speed

            self.image.move((self.x, self.y))
        else:
            rad = M.radians(self.angle)
            
            self.x += M.cos(rad) * self.speed
            self.y += M.sin(rad) * self.speed
            
            self.image.move((self.x, self.y))


    def draw(self,window):
        if self.type == 3 or self.type == 4:
            self.image.rotate(-self.angle-270)
        else:
            self.image.rotate(self.angle)
        self.image.draw(window)

def dist(x1,y1,x2,y2):
    return(M.sqrt(M.pow((x2-x1),2)+M.pow((y2-y1),2)))