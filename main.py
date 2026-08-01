# 2026 Cy 



#  --------------------------------------== BEWARE ==------------------------------------------------------
#  the code for this game is a spiderweb of interconnecting functions that might make no sense but it works



import pygame as pg
from CybrocksLibrary import *
import time
import math as M
from enemy_handeler import *
from enemys import *
from waves import *
import os
from partical_handeler import *
from particals import *
from player import Player
import random as R
from projectiles import *


def menu():
    
    pg.init()
    pg.font.init()
    

    click = pg.mixer.Sound('resources/sounds/ui/click.wav')
    
    scale = 2 #yes its pixel accurate, games with pixel art that isnt pixel accurate anoy me
    window = pg.display.set_mode((400*scale, 400*scale+50), pg.NOFRAME)

    start = Button("resources/textures/ui/start.png", (168*scale, 284*scale), 2*scale, 2*scale)

    font = pg.font.SysFont('Arial', 10*scale)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if pg.key.name(event.key) == "escape":
                    pg.quit()
                    
        window.fill((25,25,50))
        
        
        start.draw(window)
        fpsT = font.render(f'Game, Music and Art by Cy',False,(255,255,255))
        window.blit(fpsT,(150*scale,410*scale))

        if start.is_pressed():
            click.play()
            running = False
        
        pg.display.flip()
        
    racemenu(scale,window)


def racemenu(scale,window):
    click = pg.mixer.Sound('resources/sounds/ui/click.wav')

    humanB = Button("resources/textures/ui/humanB.png", (5*scale, 5*scale), 2*scale, 2*scale)
    werewolfB = Button("resources/textures/ui/werewolfB.png", (40*scale, 5*scale), 2*scale, 2*scale)
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if pg.key.name(event.key) == "escape":
                    pg.quit()
                    
        window.fill((25,25,50))
        
        humanB.draw(window)
        werewolfB.draw(window)

        if humanB.is_pressed():
            click.play()
            running = False
        
        pg.display.flip()
        
    weaponmenu(scale,window)

def weaponmenu(scale,window):
    font = pg.font.SysFont('Arial', 10*scale)
    click = pg.mixer.Sound('resources/sounds/ui/click.wav')

    weapons =   ['sword',       'rapier',       'greatsword',               'cysfang',          'kaen',            'arcanestaff',       'crossbow']
    itemdesc1 = ['The Classic', 'The Rapier,',  'Greatsword',               'Cy`s Fang,',       'Phoenix Katana,', 'Arcane Staff,',     'Crossbow']
    itemdesc2 = ['Shortsword,', 'Far range',    'Small range, Wide area',   'Legendary Scythe', 'BURN BABY BURN',  'Cast homing bolts', 'Pew']
    itemdesc3 = ['Melee',       'Persice Melee','Melee',                    'Lifesteal Melee',  'Fire Melee',      'Arcane Magic',      'Ranged']
    weaponweights=(25, 25, 25, 1, 25, 25, 25)
    button1 = shopButton(weapons,weaponweights, 1*scale, (100*scale,200*scale),True)
    button2 = shopButton(weapons,weaponweights, 1*scale, (200*scale,200*scale),True)
    button3 = shopButton(weapons,weaponweights, 1*scale, (300*scale,200*scale),True)
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if pg.key.name(event.key) == "escape":
                    pg.quit()
                    
        window.fill((25,25,50))
        
        button1.draw(window,font,itemdesc1,itemdesc2,itemdesc3)
        button2.draw(window,font,itemdesc1,itemdesc2,itemdesc3)
        button3.draw(window,font,itemdesc1,itemdesc2,itemdesc3)

        if button1.is_pressed('1'):
            click.play()
            running = False
            weaponType = button1.item
        if button2.is_pressed('2'):
            click.play()
            running = False
            weaponType = button2.item
        if button3.is_pressed('3'):
            click.play()
            running = False
            weaponType = button3.item
        
        pg.display.flip()
        
    main(scale,window,weaponType)


def main(scale, window, weaponType):
    click = pg.mixer.Sound('resources/sounds/ui/click.wav')
    font = pg.font.SysFont('Arial', 10*scale)

    # --------------== Inits ==-----------------------------------------------------------

    bgm = pg.mixer.Sound(os.curdir +'/resources/music/Lost.wav')
    channel = bgm.play(-1)
    
    EnemyHandler = enemyHandler()
    pHandler = particalHandler()
    playerH = Player()

    clock = pg.time.Clock()

    WaveSys = Wavesystem(scale)


    delay = False
    s = 0
    attacked = False
    arcaneDelay = 0
    attackCount = 0

    specialInventory = []
    arcaneBolts = 0
    extraenemys = 0
    attackDist = 0
    fireDamage = 0
    waterDamage = 0
    illusionistsCloak = False
    torch = 0
    rain = 0


    justopenedshop = False

    direction = 'L'
    dashdir = 'U'
    d = 0
    dashcooldownmax = 60
    dashcooldown = 0
    moving = False
    slash = False
    speed = 50
    maxhealth = 100
    px, py = 200*scale, 200*scale


    # --------------== Images ==-----------------------------------------------------------
    playerframes = []
    pFrame = 0
    panimtimer = 0
    for i in range(10):
        playerframes.append(BetterImage(f"resources/textures/races/human/base{i}.png", (0, 0), scale, scale))
    arm = BetterImage("resources/textures/races/human/arm.png", (0, 0), scale, scale)

    sword = BetterImage(f"resources/textures/weapons/{weaponType}.png", (0, 0), scale, scale)

    mapI = R.choice((1,2))
    #print(mapI)
    mapP = BetterImage(f"resources/textures/maps/map{mapI}.png", (0, 0), scale, scale)
    
    
    slashframes = []

    for i in range(3):
        if weaponType == 'sword':
            slashframes.append(BetterImage(f"resources/textures/particals/slash/slash{i}.png",(0,0),scale,scale))
        elif weaponType == 'rapier':
            slashframes.append(BetterImage(f"resources/textures/particals/poke/poke{i}.png",(0,0),scale,scale))
        elif weaponType == 'greatsword':
            slashframes.append(BetterImage(f"resources/textures/particals/gsslash/slash{i}.png",(0,0),1.5*scale,1.5*scale))
        elif weaponType == 'kaen':
            slashframes.append(BetterImage(f"resources/textures/particals/kslash/slash{i}.png",(0,0),scale,scale))
        
    # --------------== Main loop ==-----------------------------------------------------------
    
    WaveSys.newWave(EnemyHandler,extraenemys)


    items =     ['requiem',                'gring',              'rring',      'bring',        'coin',  'arcaneB',                   'firestone',      'illusionistsCloak',        'torch',                            'waterbubble',               'waterbottle']
    itemweights=(1,                         50,                   50,           50,             5,       10,                          10,               1,                          7,                                  7,                           3)
    itemdesc1 = ['Summons The Mechanical', 'Emerald Ring',       'Ruby Ring',  'Saphire Ring', '',      'Arcane book',               'Firestone',      'Illusionists Cloak',       'Torch',                            'Water Bubble',              'Water Bottle']
    itemdesc2 = ['Requem',                 '+1 Attack distance', '+5 Health',  '+5 speed',     '',      'Summons a arcane bolt',     '+10 Fire magic', '90% to block projectiles', 'Every attack has 25% chance',      '+1% to block Melee',        '+1 rain (1+Water dmg)']
    itemdesc3 = ['Fire & Mech',            'on melee',           '',           '',             '',      'every 4 seconds (2+light)', '-33% health',    '10% to do double dmg',     'to summon fire bolt (7+Fire dmg)', '-2 Fire dmg, +2 water dmg', '-2 Fire dmg']
    button1 = shopButton(items,itemweights, 1*scale, (100*scale,200*scale))
    button2 = shopButton(items,itemweights, 1*scale, (200*scale,200*scale))
    button3 = shopButton(items,itemweights, 1*scale, (300*scale,200*scale))

    
    running = True
    while running:

        if WaveSys.inshop:
            
            window.fill((10,10,15))

            if justopenedshop == False:
                justopenedshop = True
                button1.newstock(items,itemweights, 1*scale, (100*scale,200*scale))
                button2.newstock(items,itemweights, 1*scale, (200*scale,200*scale))
                button3.newstock(items,itemweights, 1*scale, (300*scale,200*scale))


            button1.update(window, font,itemdesc1,itemdesc2,itemdesc3)
            button2.update(window, font,itemdesc1,itemdesc2,itemdesc3)
            button3.update(window, font,itemdesc1,itemdesc2,itemdesc3)


            if button1.is_pressed('1') == True: 
                
                if button1.item == 'rring':
                    maxhealth += 5
                elif button1.item == 'bring':
                    speed += 5
                elif button1.item == 'gring':
                    attackDist += 1
                elif button1.item == 'coin':
                    pass
                elif button1.item == 'arcaneB':
                    arcaneBolts += 1
                elif button1.item == 'firestone':
                    maxhealth = round(maxhealth-(maxhealth/3))
                    fireDamage +=10
                elif button1.item == 'illusionistsCloak':
                    illusionistsCloak = True
                elif button1.item == 'torch':
                    torch += 1
                    fireDamage += 2
                elif button1.item == 'waterbubble':
                    playerH.waterbubblechance += 0.01 #1%
                    fireDamage -= 2
                    waterDamage += 2
                    if fireDamage <= 0:
                        fireDamage = 0
                elif button1.item == 'waterbottle':
                    rain += 1
                    fireDamage -= 2
                    
                #specialInventory.append(button1.item)
                #print(specialInventory)
                WaveSys.inshop = False
                justopenedshop = False
                click.play()
                
                px, py = 200*scale, 200*scale
                playerH.health = maxhealth
                WaveSys.newWave(EnemyHandler,extraenemys)

            elif button2.is_pressed('2') == True:

                if button2.item == 'rring':
                    maxhealth += 5
                elif button2.item == 'bring':
                    speed += 5
                elif button2.item == 'gring':
                    attackDist += 1
                elif button2.item == 'arcaneB':
                    arcaneBolts += 1
                elif button2.item == 'firestone':
                    maxhealth = round(maxhealth-(maxhealth/3))
                    fireDamage += 10
                elif button2.item == 'illusionistsCloak':
                    illusionistsCloak = True
                elif button2.item == 'torch':
                    torch += 1
                    fireDamage += 2
                elif button2.item == 'waterbubble':
                    playerH.waterbubblechance += 0.01 
                    fireDamage -= 2
                    waterDamage += 2
                    if fireDamage <= 0:
                        fireDamage = 0
                    
                #specialInventory.append(button2.item)
                WaveSys.inshop = False
                justopenedshop = False
                playerH.health = maxhealth
                click.play()
                px, py = 200*scale, 200*scale
                WaveSys.newWave(EnemyHandler,extraenemys)

            elif button3.is_pressed('3') == True:

                if button3.item == 'rring':
                    maxhealth += 5
                elif button3.item == 'bring':
                    speed += 5
                elif button3.item == 'gring':
                    attackDist += 1
                elif button3.item == 'arcaneB':
                    arcaneBolts += 1
                elif button3.item == 'firestone':
                    maxhealth = round(maxhealth-(maxhealth/3))
                    fireDamage +=10
                elif button3.item == 'illusionistsCloak':
                    illusionistsCloak = True
                elif button3.item == 'torch':
                    torch += 1
                    fireDamage += 2
                elif button3.item == 'waterbubble':
                    playerH.waterbubblechance += 0.01 
                    fireDamage -= 2
                    waterDamage += 2
                    if fireDamage <= 0:
                        fireDamage = 0

                #specialInventory.append(button3.item)
                WaveSys.inshop = False
                justopenedshop = False
                playerH.health = maxhealth
                click.play()
                px, py = 200*scale, 200*scale
                WaveSys.newWave(EnemyHandler,extraenemys)
            

        dt = clock.tick(60) / 1000

        WaveSys.update(EnemyHandler)
        #print(EnemyHandler.enemy_list)

        if delay >= 1:
            delay -= 1


        # --------------== Controls ==-----------------------------------------------------------
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if pg.key.name(event.key) == "escape":
                    running = False

        keys = pg.key.get_pressed()
        if not WaveSys.inshop:
            
            if keys[pg.K_w]:
                if py >= 10:
                    dashdir = 'U'
                    py -= speed*scale*dt
            if keys[pg.K_s]:
                dashdir = 'D'
                if py <= 400*scale:
                    py += speed*scale*dt
                
            if keys[pg.K_a]:
                dashdir = 'L'
                direction = 'L'
                if px >= 10:
                    px -= speed*scale*dt
            if keys[pg.K_d]:
                dashdir = 'R'
                direction = 'R'
                if px <= 400*scale:
                    px += speed*scale*dt

            if keys[pg.K_w] or keys[pg.K_s] or keys[pg.K_a] or keys[pg.K_d]:
                moving = True
            else:
                moving = False

            if keys[pg.K_LSHIFT]:
                if dashcooldown <= 0:
                    dashcooldown = dashcooldownmax
                    d = 10

            if d >= 0:
                d -= 1
                if dashdir == 'U':
                    if py >= 10:
                        py -= (speed*2)*scale*dt
                elif dashdir == 'D':
                    if py <= 400*scale:
                        py += (speed*2)*scale*dt
                elif dashdir == 'L':
                    if px >= 10:
                        px -= (speed*2)*scale*dt
                elif dashdir == 'R':
                    if px <= 400*scale:
                        px += (speed*2)*scale*dt
            else:
                dashcooldown -= 1

            if pg.mouse.get_pressed()[0] and delay == 0:
                delay = 45
                slash = True

        # --------------== Drawing and other Calculation (things are not organized) ==-----------------------------------------------------------
        if not WaveSys.inshop:
            window.fill((25,25,50))
            mapP.draw(window)

            for r in range(rain):
                if R.random() < 0.1:
                    pHandler.add_projectile(projectile(scale,(R.randrange(100,500)*scale,R.randrange(-100,350)*scale),None,0,5))

            if arcaneDelay <= 0:
                arcaneDelay = 240
                for bolts in range(arcaneBolts):
                    pHandler.add_projectile(projectile(scale,(px,py),None,0,0))
            else:
                arcaneDelay -= 1

            playerframes[pFrame].centermove((px,py))
            playerframes[pFrame].draw(window,direction)

            if moving:
                if panimtimer >= speed/20:
                    panimtimer = 0
                    pFrame += 1
                    if pFrame >= 10:
                        pFrame = 0
                else:
                    panimtimer += 1
            else:
                pFrame = 0


            ax, ay = px,py-(3*scale)
            arm.centermove((ax,ay))
            
            mx, my = pg.mouse.get_pos()
            dx = (px-(5*scale)) - mx
            dy = (py-(4*scale)) - my

            anglerad = M.atan2(dy, dx)
            angledeg = M.degrees(anglerad)
            
            arm.rotate(-angledeg-90)
            arm.draw(window)

            armlength = -11 * scale
            angle = M.radians(angledeg)
            handx = ax + M.cos(angle) * armlength
            handy = ay + M.sin(angle) * armlength
            
            sword.centermove((handx, handy))
            sword.rotate(-angledeg + 90)
            sword.draw(window)
            
            EnemyHandler.update(window,(px,py),playerH,pHandler.projectile_list,fireDamage,pHandler,waterDamage)


            for proj in pHandler.projectile_list:
                if proj.type == 2:
                    if dist(px,py,proj.x,proj.y) <= 10:
                        if illusionistsCloak == True:
                            if R.random() <= 0.10:
                                playerH.health -= 8
                        else:
                            playerH.health -= 4

            if slash:
                if not attacked:
                    attacked = True
                    attack(window, ax, ay, -angledeg-90, EnemyHandler,scale,pHandler,EnemyHandler,weaponType,attackDist,maxhealth,playerH,fireDamage,attackCount,torch)

                frame = int(s)

                if frame < len(slashframes):
                    slashI = slashframes[frame]

                    if weaponType == 'sword' or weaponType == 'kaen':
                        slength = -35 * scale
                    elif weaponType == 'rapier':
                        slength = -55 * scale
                    elif weaponType == 'greatsword':
                        slength = -0 * scale
                    angle = M.radians(angledeg)

                    sx = ax + M.cos(angle) * slength
                    sy = ay + M.sin(angle) * slength

                    slashI.centermove((sx, sy))
                    if not weaponType == 'greatsword':
                        slashI.rotate(-angledeg + 90)
                    else:
                        slashI.rotate(-angledeg + 75)
                    slashI.draw(window)

                    s += dt * 20
                else:
                    s = 0
                    slash = False
                    attacked = False

            playerH.update()
            #print(playerH.health)
            if playerH.dead:
                running = False

            pHandler.update(window,scale,EnemyHandler,pHandler,EnemyHandler)
            #testp.update(window,EnemyHandler,pHandler)


            drawHud(window,scale,playerH,font,WaveSys,clock)

        pg.display.flip()



def attack(window, px, py, pa, EnemyHandler,scale,pHandler,WaveSys,weaponType,attackDist,maxhealth,playerH,fireDamage,attackCount,torch): #looks familiar
    
    if weaponType == 'sword':
        
        for torchitem in range(torch):
            if R.random() < 0.25:
                pHandler.add_projectile(projectile(scale,(px,py),None,(-pa+90)+R.randrange(-45,45),4))
                
        for ray in range(20): #amount of rays

            rayangle = (pa - 30 + ray * 5) * M.pi / 180

            dx = M.sin(rayangle)
            dy = M.cos(rayangle)

            sx, sy = (px + dx * (50+attackDist)*scale,py + dy * (50+attackDist)*scale)
            
            for enemy in EnemyHandler.enemy_list:
                if (intersect((px, py), (sx, sy),(enemy.x - 10, enemy.y - 10),(enemy.x + 10, enemy.y + 10)) or intersect((px, py), (sx, sy),(enemy.x - 10, enemy.y + 10),(enemy.x + 10, enemy.y - 10))):
                    enemy.health -= 1    
                    enemy.hit(pHandler,scale,WaveSys)
                    
            #pg.draw.line(window, "red", (px, py),(sx, sy), 2)
            


    elif weaponType == 'rapier':
        
        for torchitem in range(torch):
            if R.random() < 0.25:
                pHandler.add_projectile(projectile(scale,(px,py),None,(-pa+90)+R.randrange(-15,15),4))
                
        for ray in range(20):
        
            rayangle = (pa - 10 + ray * 1) * M.pi / 180
        
            dx = M.sin(rayangle)
            dy = M.cos(rayangle)
        
            sx, sy = (px + dx * (80+(attackDist*2))*scale,py + dy * (80+(attackDist*2))*scale)
                    
            for enemy in EnemyHandler.enemy_list:
                if (intersect((px, py), (sx, sy),(enemy.x - 10, enemy.y - 10),(enemy.x + 10, enemy.y + 10)) or intersect((px, py), (sx, sy),(enemy.x - 10, enemy.y + 10),(enemy.x + 10, enemy.y - 10))):
                    enemy.health -= 2
                    enemy.hit(pHandler,scale,WaveSys)
                            
            #pg.draw.line(window, "red", (px, py),(sx, sy), 2)
            


    elif weaponType == 'greatsword':
        
        for torchitem in range(torch):
            if R.random() < 0.25:
                pHandler.add_projectile(projectile(scale,(px,py),None,(-pa+90)+R.randrange(-70,70),4))
                
        for ray in range(40):
            
            rayangle = (pa - 90 + ray * 4.5) * M.pi / 180
            
            dx = M.sin(rayangle)
            dy = M.cos(rayangle)
            
            sx, sy = (px + dx * (50+(attackDist/2))*scale,py + dy * (50+(attackDist/2))*scale)
                        
            for enemy in EnemyHandler.enemy_list:
                if (intersect((px, py), (sx, sy),(enemy.x - 10, enemy.y - 10),(enemy.x + 10, enemy.y + 10)) or intersect((px, py), (sx, sy),(enemy.x - 10, enemy.y + 10),(enemy.x + 10, enemy.y - 10))):
                    enemy.health -= 1
                    enemy.hit(pHandler,scale,WaveSys)
                                
            #pg.draw.line(window, "red", (px, py),(sx, sy), 2)
            


    elif weaponType == 'cysfang':
        
        for torchitem in range(torch):
            if R.random() < 0.25:
                pHandler.add_projectile(projectile(scale,(px,py),None,(-pa+90)+R.randrange(-45,45),4))
                
        for ray in range(20):
                
            rayangle = (pa - 40 + ray * 4) * M.pi / 180
                
            dx = M.sin(rayangle)
            dy = M.cos(rayangle)
                
            sx, sy = (px + dx * 60*scale,py + dy * 60*scale)
                            
            for enemy in EnemyHandler.enemy_list:
                if (intersect((px, py), (sx, sy),(enemy.x - 10, enemy.y - 10),(enemy.x + 10, enemy.y + 10)) or intersect((px, py), (sx, sy),(enemy.x - 10, enemy.y + 10),(enemy.x + 10, enemy.y - 10))):
                    enemy.health -= 5
                    if playerH.health <= maxhealth:
                        playerH.health += 1
                    enemy.hit(pHandler,scale,WaveSys)
                                    
            #pg.draw.line(window, "red", (px, py),(sx, sy), 2)



    elif weaponType == 'kaen':
        
        for torchitem in range(torch):
            if R.random() < 0.25:
                pHandler.add_projectile(projectile(scale,(px,py),None,(-pa+90)+R.randrange(-45,45),4))
                
        for ray in range(20):
                    
            rayangle = (pa - 40 + ray * 4) * M.pi / 180
                    
            dx = M.sin(rayangle)
            dy = M.cos(rayangle)
                    
            sx, sy = (px + dx * 60*scale,py + dy * 60*scale)
            sx2, sy2 = (px + dx * R.randrange(1,60)*scale,py + dy * R.randrange(1,60) *scale)
            
            pHandler.add_projectile(projectile(scale,(sx2,sy2),None,0,1))
                                
            for enemy in EnemyHandler.enemy_list:
                if (intersect((px, py), (sx, sy),(enemy.x - 10, enemy.y - 10),(enemy.x + 10, enemy.y + 10)) or intersect((px, py), (sx, sy),(enemy.x - 10, enemy.y + 10),(enemy.x + 10, enemy.y - 10))):
                    enemy.health -= 1 + fireDamage
                    enemy.hit(pHandler,scale,WaveSys)
                                        
            #pg.draw.line(window, "red", (px, py),(sx, sy), 2)
            


    elif weaponType == 'arcanestaff':
        pHandler.add_projectile(projectile(scale,(px,py),None,0))
        for torchitem in range(torch):
            if R.random() < 0.25:
                pHandler.add_projectile(projectile(scale,(px,py),None,(-pa+90)+R.randrange(-45,45),4))

    elif weaponType == 'crossbow':
        pHandler.add_projectile(projectile(scale,(px,py),None,-pa+90,3))
        for torchitem in range(torch):
            if R.random() < 0.25:
                pHandler.add_projectile(projectile(scale,(px,py),None,(-pa+90)+R.randrange(-45,45),4))





class shopButton:
    def __init__(self,items,weights,scale,pos,weapons=False):
        self.x,self.y = pos
        self.scale = scale
        self.picked = R.choices(range(len(items)), weights, k=1)[0]
        self.item = items[self.picked]
        self.button = Button(f"resources/textures/ui/button.png", pos, 2*scale, 2*scale)
        if weapons == True:
            self.image = Button(f"resources/textures/weapons/{self.item}.png", pos, 2*scale, 2*scale)
        else:
            self.image = Button(f"resources/textures/ui/items/{self.item}.png", pos, 2*scale, 2*scale)

    def newstock(self,items,weights, scale, pos):
        self.picked = R.choices(range(len(items)), weights, k=1)[0]
        self.item = items[self.picked]
        self.button = Button(f"resources/textures/ui/button.png", pos, 2*scale, 2*scale)
        self.image = Button(f"resources/textures/ui/items/{self.item}.png", pos, 2*scale, 2*scale)

    def update(self,window,font,itemdesc1,itemdesc2,itemdesc3):
        self.draw(window,font,itemdesc1,itemdesc2,itemdesc3)


    def draw(self,window,font,itemdesc1,itemdesc2,itemdesc3):
        self.button.draw(window)
        self.image.draw(window)
        desc1 = font.render(itemdesc1[self.picked],False,(100,100,255))
        window.blit(desc1, (self.x, self.y + 40*self.scale))
        desc2 = font.render(itemdesc2[self.picked],False,(255,0,255))
        window.blit(desc2, (self.x, self.y + 80*self.scale))
        desc3 = font.render(itemdesc3[self.picked],False,(255,255,255))
        window.blit(desc3, (self.x, self.y + 120*self.scale))
        
    def is_pressed(self, gkey):
        keys = pg.key.get_pressed()

        if keys[getattr(pg, f"K_{gkey}")]:
            return True
        return False
            
        #mouse_pos = pg.mouse.get_pos()
        #mouse_pressed = pg.mouse.get_pressed()[0]

        #if self.button.rect.collidepoint(mouse_pos):
        #    if mouse_pressed:
        #        return True



def drawHud(window,scale,player,font,wave,clock):

                                #[x,y,w,h]
    pg.draw.rect(window, (0,0,0), [0, 400*scale, 400*scale, 50], 0)
    pg.draw.rect(window, (255,0,0), [0, 400*scale, player.health*scale, 12*scale], 0)
    healthT = font.render(f'{player.health}',False,(255,255,255))
    window.blit(healthT,(5*scale,400*scale))
    waveT = font.render(f'{wave.wave-1}',False,(255,255,255))
    window.blit(waveT,(5*scale,410*scale))
    fpsT = font.render(f'{round(clock.get_fps())}',False,(255,0,255))
    window.blit(fpsT,(200*scale,410*scale))




def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)




if __name__ == "__main__":
    menu()

pg.quit()




