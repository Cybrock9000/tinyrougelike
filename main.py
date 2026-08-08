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
from pets import pet


def menu():
    
    pg.init()
    pg.font.init()
    

    click = pg.mixer.Sound('resources/sounds/ui/click.wav')
    click.set_volume(0.35)
    
    scale = 1 #yes its pixel accurate, games with pixel art that isnt pixel accurate anoy me
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
        fpsT = font.render(f'Game, Music and Art by CyberWolf Games',False,(255,255,255))
        window.blit(fpsT,(125*scale,410*scale))

        if start.is_pressed():
            click.play()
            running = False
        
        pg.display.flip()
        
    racemenu(scale,window)


def racemenu(scale,window):
    click = pg.mixer.Sound('resources/sounds/ui/click.wav')
    click.set_volume(0.35)

    race = ''

    humanB = Button("resources/textures/ui/humanB.png", (5*scale, 5*scale), 2*scale, 2*scale)
    werewolfB = Button("resources/textures/ui/werewolfB.png", (40*scale, 5*scale), 2*scale, 2*scale)
    kitsuneB = Button("resources/textures/ui/kitsuneB.png", (75*scale, 5*scale), 2*scale, 2*scale)
    vampireB = Button("resources/textures/ui/vampireB.png", (110*scale, 5*scale), 2*scale, 2*scale)
    draiknikB = Button("resources/textures/ui/draiknikB.png", (145*scale, 5*scale), 2*scale, 2*scale)
    voidwalkerB = Button("resources/textures/ui/voidwalkerB.png", (180*scale, 5*scale), 2*scale, 2*scale)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if pg.key.name(event.key) == "escape":
                    pg.quit()
                    
        window.fill((25,25,50))
        
        humanB.draw(window)
        werewolfB.draw(window)
        kitsuneB.draw(window)
        vampireB.draw(window)
        draiknikB.draw(window)
        voidwalkerB.draw(window)


        if humanB.is_pressed():
            click.play()
            running = False
            race = 'human'
            
        if werewolfB.is_pressed():
            click.play()
            running = False
            race = 'werewolf'

        if kitsuneB.is_pressed():
            click.play()
            running = False
            race = 'kitsune'

        if voidwalkerB.is_pressed():
            click.play()
            running = False
            race = 'voidwalker'


        pg.display.flip()
        
    weaponmenu(scale,window,race)

def weaponmenu(scale,window,race):
    font = pg.font.SysFont('Arial', 10*scale)
    click = pg.mixer.Sound('resources/sounds/ui/click.wav')
    click.set_volume(0.35)

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
        
    main(scale,window,weaponType,race)


def main(scale, window, weaponType,race):
    click = pg.mixer.Sound('resources/sounds/ui/click.wav')
    click.set_volume(0.35)
    font = pg.font.SysFont('Arial', 10*scale)

    # --------------== Inits ==-----------------------------------------------------------

    songend = pg.USEREVENT + 1

    pg.mixer.music.set_endevent(songend)
    pg.mixer.music.load("resources/music/Lost.wav")
    pg.mixer.music.set_volume(0.5)
    pg.mixer.music.play()
    
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
    attacking = 90
    a = 0
    shake = (0,0)
    
    moonphase = 6 #new moon


    arcaneBolts = 0
    if not race == 'voidwalker':
        shadowOrbs = 0
    else:
        shadowOrbs = 3
    extraenemys = 0
    attackDist = 0
    if not race == 'kitsune':
        fireDamage = 0
    else:
        fireDamage = 10
    if not race == 'kitsune':
        waterDamage = 0
    else:
        waterDamage = -10
    if race == 'werewolf':
        lightDamage = 10
    elif not race == 'voidwalker':
        lightDamage = 0
    else:
        lightDamage = -10
    if not race == 'voidwalker':
        shadowDamage = 0
    else:
        shadowDamage = 10
    lifeDamage = 0
    illusionistsCloak = False
    if not race == 'kitsune':
        torch = 0
    else:
        torch = 5
    rain = 0
    luck = 0
    luck2 = 0
    if not race == 'voidwalker':
        prophecy = False
    else:
        if R.random() <= .10:
            prophecy = True
        else:
            prophecy = False
    lifesteal = 0

    moonweights = (20,10,10,1)
    fullmoonphase = ''

    moonlight = 0
    moonshadow = 0
    moonfire = 0
    moonwater = 0
    moonls = 0
    


    requiem = False

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

    shattering = 0

    # --------------== Images ==-----------------------------------------------------------
    playerframes = []
    pFrame = 0
    panimtimer = 0
    for i in range(11):
        playerframes.append(BetterImage(f"resources/textures/races/{race}/base{i-1}.png", (0, 0), scale, scale))
    arm = BetterImage(f"resources/textures/races/{race}/arm.png", (0, 0), scale, scale)

    sword = BetterImage(f"resources/textures/weapons/{weaponType}.png", (0, 0), scale, scale)

    mapI = R.choice((1,2,3,4)) #randrange was not working right
    #print(mapI)
    mapP = BetterImage(f"resources/textures/maps/map{mapI}.png", (0, 0), scale, scale)

    moonframes = []
    for i in range(12):
        moonframes.append(BetterImage(f"resources/textures/moon/{i+1}.png", (400*scale-(32*scale), 400*scale), scale, scale))

    moonframes.append(BetterImage(f"resources/textures/moon/1b.png", (400*scale-(32*scale), 400*scale), scale, scale))
    moonframes.append(BetterImage(f"resources/textures/moon/1r.png", (400*scale-(32*scale), 400*scale), scale, scale))
    moonframes.append(BetterImage(f"resources/textures/moon/1se.png", (400*scale-(32*scale), 400*scale), scale, scale))
    
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


    items =     ['requiem',                'gring',              'rring',       'bring',        'coin',      'arcaneB',                   'firestone',      'illusionistsCloak',        'torch',                            'waterbubble',                 'waterbottle',           'prophecy',          'fang',          'shardofdarkness']
    itemweights=(1,                         50-luck-luck2,        50-luck-luck2, 50-luck-luck2,  5,           10-luck2,                    10-luck2,         1+luck,                     7,                                  7,                             3+luck,                  1,                   2+luck2,         1+luck+luck2)
    itemdesc1 = ['Summons The Mechanical', 'Emerald Ring',       'Ruby Ring',   'Saphire Ring', '+1 luck',   'Arcane book',               'Firestone',      'Illusionists Cloak',       'Torch',                            'Water Bubble',                'Water Bottle',          'The Prophecy',      'Vampire Fang',  'Shard of Darkness']
    itemdesc2 = ['Requem',                 '+1 Attack distance', '+5 Health',   '+5 speed',     '+5 Enemys', 'Summons a arcane bolt',     '+10 Fire magic', '90% to block projectiles', 'Every attack has 25% chance',      '+1% to block Melee (60%max)', '+1 rain (1+Water dmg)', '',                  '+1 lifesteal',  '+1 Shadow Orb']
    itemdesc3 = ['Fire & Mech',            'on melee',           '',            '',             '',          'every 4 seconds (2+light)', '-33% health',    '10% to do double dmg',     'to summon fire bolt (7+Fire dmg)', '-2 Fire dmg, +2 water dmg',   '-2 Fire dmg',           '',                  '-50% health',   '']
    button1 = shopButton(items,itemweights, 1*scale, (100*scale,200*scale))
    button2 = shopButton(items,itemweights, 1*scale, (200*scale,200*scale))
    button3 = shopButton(items,itemweights, 1*scale, (300*scale,200*scale))

    
    running = True
    while running:

        if WaveSys.inshop:
            
            window.fill((10,10,15))

            if justopenedshop == False:
                justopenedshop = True
                for requiems in EnemyHandler.pet_list:
                    requiems.song.stop()
                EnemyHandler.pet_list = []
                button1.newstock(items,itemweights, 1*scale, (100*scale,200*scale))
                button2.newstock(items,itemweights, 1*scale, (200*scale,200*scale))
                button3.newstock(items,itemweights, 1*scale, (300*scale,200*scale))


            button1.update(window, font,itemdesc1,itemdesc2,itemdesc3)
            button2.update(window, font,itemdesc1,itemdesc2,itemdesc3)
            button3.update(window, font,itemdesc1,itemdesc2,itemdesc3)

            ht = font.render(f'Max Health: {maxhealth}',False,(255,0,0))
            window.blit(ht,(10*scale,10*scale))
            st = font.render(f'Speed: {speed}',False,(0,0,255))
            window.blit(st,(10*scale,20*scale))
            adt = font.render(f'Attack Dist: {attackDist}',False,(0,255,0))
            window.blit(adt,(10*scale,30*scale))
            lt = font.render(f'Luck: {luck}',False,(255,255,0))
            window.blit(lt,(10*scale,40*scale))
            ls = font.render(f'Lifesteal: {lifesteal}',False,(200,0,0))
            window.blit(ls,(10*scale,50*scale))
            fd = font.render(f'Fire Damage: {fireDamage}',False,(255,0,0))
            window.blit(fd,(10*scale,60*scale))
            wd = font.render(f'Water Damage: {waterDamage}',False,(0,0,255))
            window.blit(wd,(10*scale,70*scale))
            sd = font.render(f'Shadow Damage: {shadowDamage}',False,(100,100,100))
            window.blit(sd,(10*scale,80*scale))
            lightd = font.render(f'Light Damage: {lightDamage}',False,(200,200,255))
            window.blit(lightd,(10*scale,90*scale))
            ld = font.render(f'Life Damage: {lifeDamage}',False,(0,255,0))
            window.blit(ld,(10*scale,100*scale))
            ee = font.render(f'Extra Enemys: {extraenemys}',False,(155,100,0))
            window.blit(ee,(10*scale,110*scale))
            ab = font.render(f'Arcane Bolts: {arcaneBolts}',False,(200,200,255))
            window.blit(ab,(10*scale,120*scale))
            rt = font.render(f'Rain: {rain}',False,(50,100,255))
            window.blit(rt,(10*scale,130*scale))
            tt = font.render(f'Torch: {torch}',False,(255,100,50))
            window.blit(tt,(10*scale,140*scale))
            so = font.render(f'Shadow Orbs: {shadowOrbs}',False,(100,100,100))
            window.blit(so,(10*scale,150*scale))


            if button1.is_pressed('1') == True: 
                
                if button1.item == 'rring':
                    maxhealth += 5
                elif button1.item == 'bring':
                    speed += 5
                elif button1.item == 'gring':
                    attackDist += 1
                elif button1.item == 'coin':
                    if luck >= 15:
                        luck2 +=1
                        luck -= 1
                    else:
                        luck += 1
                    extraenemys += 5
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
                    if playerH.waterbubblechance >= 0.6: #60%
                        playerH.waterbubblechance = 0.6
                    if race == 'kitsune':
                        fireDamage -= 5
                        waterDamage += 1
                    else:
                        fireDamage -= 2
                        waterDamage += 2
                    if fireDamage <= 0:
                        fireDamage = 0
                elif button1.item == 'waterbottle':
                    rain += 1
                    if race == 'kitsune':
                        fireDamage -= 5
                    else:
                        fireDamage -= 2
                    if fireDamage <= 0:
                        fireDamage = 0
                elif button1.item == 'prophecy':
                    prophecy = True
                elif button1.item == 'fang':
                    lifesteal += 1
                    maxhealth = round(maxhealth-(maxhealth/2))
                elif button1.item == 'shardofdarkness':
                    shadowOrbs += 1
                    if race == 'werewolf':
                        lightDamage -= 2
                        maxhealth -= 2
                elif button1.item == 'requiem':
                    requiem = True
                    
                #specialInventory.append(button1.item)
                #print(specialInventory)
                WaveSys.inshop = False
                justopenedshop = False
                click.play()
                
                px, py = 200*scale, 200*scale
                playerH.health = maxhealth
                pHandler.projectile_list = []

                if requiem == True:
                    EnemyHandler.add_pet(pet((200*scale,200*scale), scale, 0.5, 1, 0))

                if moonphase != 11:
                    moonphase += 1
                else:
                    fullmoonphase = R.choices(('','r','b','se'), moonweights, k=1)[0]
                    moonphase = 0
 
                if R.random() <= 0.1:

                    mapI = R.choice((1,2,3,4))
                    mapP = BetterImage(f"resources/textures/maps/map{mapI}.png", (0, 0), scale, scale)

                WaveSys.newWave(EnemyHandler,extraenemys)

            elif button2.is_pressed('2') == True:

                if button2.item == 'rring':
                    maxhealth += 5
                elif button2.item == 'bring':
                    speed += 5
                elif button2.item == 'gring':
                    attackDist += 1
                elif button2.item == 'coin':
                    if luck >= 15:
                        luck2 +=1
                        luck -= 1
                    else:
                        luck += 1
                    extraenemys += 5
                elif button2.item == 'arcaneB':
                    arcaneBolts += 1
                elif button2.item == 'firestone':
                    maxhealth = round(maxhealth-(maxhealth/3))
                    fireDamage += 10
                    shadowDamage -= 10
                    if shadowDamage <= 0:
                        shadowDamage = 0
                elif button2.item == 'illusionistsCloak':
                    illusionistsCloak = True
                elif button2.item == 'torch':
                    torch += 1
                    fireDamage += 2
                    shadowDamage -= 2
                    if shadowDamage <= 0:
                        shadowDamage = 0
                elif button2.item == 'waterbubble':
                    playerH.waterbubblechance += 0.01 
                    if playerH.waterbubblechance >= 0.6:
                        playerH.waterbubblechance = 0.6
                    fireDamage -= 2
                    waterDamage += 2
                    if fireDamage <= 0:
                        fireDamage = 0
                elif button2.item == 'waterbottle':
                    rain += 1
                    fireDamage -= 2
                    if fireDamage <= 0:
                        fireDamage = 0
                elif button2.item == 'prophecy':
                    prophecy = True
                elif button2.item == 'fang':
                    lifesteal += 1
                    maxhealth = round(maxhealth-(maxhealth/2))
                elif button2.item == 'shardofdarkness':
                    shadowOrbs += 1
                    if race == 'werewolf':
                        lightDamage -= 2
                        maxhealth -= 2
                elif button2.item == 'requiem':
                    requiem = True
                    
                #specialInventory.append(button2.item)
                WaveSys.inshop = False
                justopenedshop = False
                playerH.health = maxhealth
                click.play()
                px, py = 200*scale, 200*scale
                pHandler.projectile_list = []
                EnemyHandler.pet_list = []

                if requiem == True:
                    EnemyHandler.add_pet(pet((200*scale,200*scale), scale, 0.5, 1, 0))

                if moonphase != 11:
                    moonphase += 1
                else:
                    fullmoonphase = R.choices(('','r','b','se'), moonweights, k=1)[0]
                    moonphase = 0

                if R.random() <= 0.1:

                    mapI = R.choice((1,2,3,4))
                    mapP = BetterImage(f"resources/textures/maps/map{mapI}.png", (0, 0), scale, scale)

                WaveSys.newWave(EnemyHandler,extraenemys)

            elif button3.is_pressed('3') == True:

                if button3.item == 'rring':
                    maxhealth += 5
                elif button3.item == 'bring':
                    speed += 5
                elif button3.item == 'gring':
                    attackDist += 1
                elif button3.item == 'coin':
                    if luck >= 15:
                        luck2 +=1
                        luck -= 1
                    else:
                        luck += 1
                    extraenemys += 5
                elif button3.item == 'arcaneB':
                    arcaneBolts += 1
                elif button3.item == 'firestone':
                    maxhealth = round(maxhealth-(maxhealth/3))
                    fireDamage +=10
                    shadowDamage -= 10
                    if shadowDamage <= 0:
                        shadowDamage = 0
                elif button3.item == 'illusionistsCloak':
                    illusionistsCloak = True
                elif button3.item == 'torch':
                    torch += 1
                    fireDamage += 2
                    shadowDamage -= 10
                    if shadowDamage <= 0:
                        shadowDamage = 0
                elif button3.item == 'waterbubble':
                    playerH.waterbubblechance += 0.01 
                    if playerH.waterbubblechance >= 0.6:
                        playerH.waterbubblechance = 0.6
                    fireDamage -= 2
                    waterDamage += 2
                    if fireDamage <= 0:
                        fireDamage = 0
                elif button3.item == 'waterbottle':
                    rain += 1
                    fireDamage -= 2
                    if fireDamage <= 0:
                        fireDamage = 0
                elif button3.item == 'prophecy':
                    prophecy = True
                elif button3.item == 'fang':
                    lifesteal += 1
                    maxhealth = round(maxhealth-(maxhealth/2))
                elif button3.item == 'shardofdarkness':
                    shadowOrbs += 1
                    if race == 'werewolf':
                        lightDamage -= 2
                        maxhealth -= 2
                elif button3.item == 'requiem':
                    requiem = True

                #specialInventory.append(button3.item)
                WaveSys.inshop = False
                justopenedshop = False
                playerH.health = maxhealth
                click.play()
                px, py = 200*scale, 200*scale
                pHandler.projectile_list = []
                EnemyHandler.pet_list = []

                if requiem == True:
                    EnemyHandler.add_pet(pet((200*scale,200*scale), scale, 0.5, 1, 0))

                if moonphase != 11:
                    moonphase += 1
                else:
                    fullmoonphase = R.choices(('','r','b','se'), moonweights, k=1)[0]
                    moonphase = 0

                if R.random() <= 0.1:

                    mapI = R.choice((1,2,3,4))
                    mapP = BetterImage(f"resources/textures/maps/map{mapI}.png", (0, 0), scale, scale)

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

            if event.type == songend:
                if prophecy:
                    if R.random() < 0.1:
                        pg.mixer.music.load("resources/music/ShatteredVoid.wav")
                    else:
                        pg.mixer.music.load("resources/music/Shattered.wav")
                else:
                    pg.mixer.music.load("resources/music/Lost.wav")

                pg.mixer.music.play()

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

            if not race == 'voidwalker':
                playerframes[pFrame].centermove((px+shake[0],py+shake[1]))
            else:
                playerframes[pFrame].centermove((px+R.randrange(-1*scale,1*scale)+shake[0],py+shake[1]))
                
            playerframes[pFrame].draw(window,direction)

            if moving:
                if panimtimer >= speed/20:
                    panimtimer = 0
                    pFrame += 1
                    if pFrame >= 11:
                        pFrame = 1
                else:
                    panimtimer += 1
            else:
                pFrame = 0


            ax, ay = px,py-(3*scale)
            if not race == 'voidwalker':
                arm.centermove((ax+shake[0],ay+shake[1]))
            else:
                arm.centermove((ax+R.randrange(-1*scale,1*scale)+shake[0],ay+shake[1]))
            
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
            
            sword.centermove((handx+shake[0], handy+shake[1]))


            if attacking != 90:
                sword.rotate(-angledeg-attacking+45)
                attacking += 20
            
            else:
                sword.rotate(-angledeg + 90)
            sword.draw(window)
            
            EnemyHandler.update(window,(px,py),playerH,pHandler.projectile_list,fireDamage,pHandler,waterDamage,lightDamage,shadowDamage,shadowOrbs,shake)


            for proj in pHandler.projectile_list:
                if proj.type == 2 or proj.type == 8:
                    if dist(px,py,proj.x,proj.y) <= 10:
                        if illusionistsCloak == True:
                            if R.random() <= 0.10:
                                playerH.health -= 8
                        else:
                            playerH.health -= 4

            if slash:
                if not attacked:
                    attacked = True
                    if not (weaponType == 'rapier' or weaponType == 'arcanestaff' or weaponType == 'crossbow'):
                        attacking = -90
                    a = attack(window, ax, ay, -angledeg-90, EnemyHandler,scale,pHandler,EnemyHandler,weaponType,attackDist,maxhealth,playerH,fireDamage,attackCount,torch,luck,lifesteal)

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

            if a >= 1:
                shake = (R.randrange(-a,a),R.randrange(-a,a))
                mapP.move(shake) 
                a -= 1
            else:
                mapP.move((0,0)) 
                shake = (0,0)

            playerH.update()
            #print(playerH.health)
            if playerH.dead:
                running = False

            pHandler.update(window,scale,EnemyHandler,pHandler,EnemyHandler)
            #testp.update(window,EnemyHandler,pHandler)


            drawHud(window,scale,playerH,font,WaveSys,clock,moonphase,moonframes,fullmoonphase)

        pg.display.flip()



def attack(window, px, py, pa, EnemyHandler,scale,pHandler,WaveSys,weaponType,attackDist,maxhealth,playerH,fireDamage,attackCount,torch,luck,lifesteal): #looks familiar
    a = 0

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
                if enemy.type == 3:
                    if (intersect((px, py), (sx, sy),(enemy.x - 10+32, enemy.y - 90-64),(enemy.x + 10+32, enemy.y + 90-64)) or intersect((px, py), (sx, sy),(enemy.x - 10+32, enemy.y + 90-64),(enemy.x + 90-64, enemy.y - 90-64))):
                        enemy.health -= 1    
                        enemy.hit(pHandler,scale,WaveSys)
                        if R.random() <= lifesteal:
                            if playerH.health <= maxhealth:
                                playerH.health += 1
                        a = 5
                else:
                    if (intersect((px, py), (sx, sy),(enemy.x - 10+16, enemy.y - 10+16),(enemy.x + 10+16, enemy.y + 10+16)) or intersect((px, py), (sx, sy),(enemy.x - 10+16, enemy.y + 10+16),(enemy.x + 10+16, enemy.y - 10+16))):
                        enemy.health -= 1    
                        enemy.hit(pHandler,scale,WaveSys)
                        if R.random() <= lifesteal:
                            if playerH.health <= maxhealth:
                                playerH.health += 1
                        a = 5
                    
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
                if enemy.type == 3:
                    if (intersect((px, py), (sx, sy),(enemy.x - 10+32, enemy.y - 90-64),(enemy.x + 10+32, enemy.y + 90-64)) or intersect((px, py), (sx, sy),(enemy.x - 10+32, enemy.y + 90-64),(enemy.x + 90-64, enemy.y - 90-64))):
                        enemy.health -= 2
                        enemy.hit(pHandler,scale,WaveSys)
                        if R.random() <= lifesteal:
                            if playerH.health <= maxhealth:
                                playerH.health += 1
                        a = 3
                else:
                    if (intersect((px, py), (sx, sy),(enemy.x - 10+16, enemy.y - 10+16),(enemy.x + 10+16, enemy.y + 10+16)) or intersect((px, py), (sx, sy),(enemy.x - 10+16, enemy.y + 10+16),(enemy.x + 10+16, enemy.y - 10+16))):
                        enemy.health -= 2
                        enemy.hit(pHandler,scale,WaveSys)
                        if R.random() <= lifesteal:
                            if playerH.health <= maxhealth:
                                playerH.health += 1
                        a = 3
                            
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
                if enemy.type == 3:
                    if (intersect((px, py), (sx, sy),(enemy.x - 10+32, enemy.y - 90-64),(enemy.x + 10+32, enemy.y + 90-64)) or intersect((px, py), (sx, sy),(enemy.x - 10+32, enemy.y + 90-64),(enemy.x + 90-64, enemy.y - 90-64))):
                        enemy.health -= 1
                        #pg.draw.line(window, "red", (enemy.x - 10+32, enemy.y - 90-64),(enemy.x + 10+32, enemy.y + 90-64), 5)
                        #pg.draw.line(window, "red", (enemy.x - 10+32, enemy.y + 90-64),(enemy.x + 10+32, enemy.y - 90-64), 5)
                        enemy.hit(pHandler,scale,WaveSys)
                        if R.random() <= lifesteal:
                            if playerH.health <= maxhealth:
                                playerH.health += 1
                        a = 5
                else:
                    if (intersect((px, py), (sx, sy),(enemy.x - 10+16, enemy.y - 10+16),(enemy.x + 10+16, enemy.y + 10+16)) or intersect((px, py), (sx, sy),(enemy.x - 10+16, enemy.y + 10+16),(enemy.x + 10+16, enemy.y - 10+16))):
                        #pg.draw.line(window, "red", (enemy.x - 10+16, enemy.y - 10+16),(enemy.x + 10+16, enemy.y + 10+16), 5)
                        #pg.draw.line(window, "red", (enemy.x - 10+16, enemy.y + 10+16),(enemy.x + 10+16, enemy.y - 10+16), 5)
                        enemy.health -= 1
                        enemy.hit(pHandler,scale,WaveSys)
                        if R.random() <= lifesteal:
                            if playerH.health <= maxhealth:
                                    playerH.health += 1
                        a = 5
                                
            #pg.draw.line(window, "red", (px, py),(sx, sy), 2)
            


    elif weaponType == 'cysfang':
        
        for torchitem in range(torch):
            if R.random() < 0.25:
                pHandler.add_projectile(projectile(scale,(px,py),None,(-pa+90)+R.randrange(-45,45),4))

                
        for ray in range(20):
                
            rayangle = (pa - 40 + ray * 4) * M.pi / 180
                
            dx = M.sin(rayangle)
            dy = M.cos(rayangle)
                
            sx, sy = (px + dx * (80+attackDist)*scale,py + dy * (80+attackDist)*scale)
                            
            for enemy in EnemyHandler.enemy_list:
                if enemy.type == 3:
                    if (intersect((px, py), (sx, sy),(enemy.x - 10+32, enemy.y - 90-64),(enemy.x + 10+32, enemy.y + 90-64)) or intersect((px, py), (sx, sy),(enemy.x - 10+32, enemy.y + 90-64),(enemy.x + 90-64, enemy.y - 90-64))):
                        enemy.health -= 5
                        if playerH.health <= maxhealth:
                            playerH.health += 1
                        enemy.hit(pHandler,scale,WaveSys)
                        a = 7
                elif (intersect((px, py), (sx, sy),(enemy.x - 10+16, enemy.y - 10+16),(enemy.x + 10+16, enemy.y + 10+16)) or intersect((px, py), (sx, sy),(enemy.x - 10+16, enemy.y + 10+16),(enemy.x + 10+16, enemy.y - 10+16))):
                    enemy.health -= 5
                    if playerH.health <= maxhealth:
                        playerH.health += 1
                    enemy.hit(pHandler,scale,WaveSys)
                    a = 7

                                    
            #pg.draw.line(window, "red", (px, py),(sx, sy), 2)



    elif weaponType == 'kaen':
        
        for torchitem in range(torch):
            if R.random() < 0.25:
                pHandler.add_projectile(projectile(scale,(px,py),None,(-pa+90)+R.randrange(-45,45),4))
                
        for ray in range(20):
                    
            rayangle = (pa - 40 + ray * 4) * M.pi / 180
                    
            dx = M.sin(rayangle)
            dy = M.cos(rayangle)
                    
            sx, sy = (px + dx * (60+attackDist)*scale,py + dy * (60+attackDist)*scale)
            sx2, sy2 = (px + dx * R.randrange(1,60+attackDist)*scale,py + dy * R.randrange(1,60+attackDist) *scale)

            if R.random() <= 0.25+(luck/100):
                pHandler.add_projectile(projectile(scale,(sx2,sy2),None,0,1))
            if R.random() <= 0.25+(luck/100):
                pHandler.add_projectile(projectile(scale,(sx,sy),None,0,1))
                                
            for enemy in EnemyHandler.enemy_list:
                if enemy.type == 3:
                    if (intersect((px, py), (sx, sy),(enemy.x - 10+32, enemy.y - 90-64),(enemy.x + 10+32, enemy.y + 90-64)) or intersect((px, py), (sx, sy),(enemy.x - 10+32, enemy.y + 90-64),(enemy.x + 90-64, enemy.y - 90-64))):
                        enemy.health -= 1 + fireDamage
                        enemy.hit(pHandler,scale,WaveSys)
                        if R.random() <= lifesteal:
                            if playerH.health <= maxhealth:
                                playerH.health += 1
                        a = 5
                elif (intersect((px, py), (sx, sy),(enemy.x - 10+16, enemy.y - 10+16),(enemy.x + 10+16, enemy.y + 10+16)) or intersect((px, py), (sx, sy),(enemy.x - 10+16, enemy.y + 10+16),(enemy.x + 10+16, enemy.y - 10+16))):
                    enemy.health -= 1 + fireDamage
                    enemy.hit(pHandler,scale,WaveSys)
                    if R.random() <= lifesteal:
                        if playerH.health <= maxhealth:
                            playerH.health += 1
                    a = 5
                                        
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
                
    return a





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



def drawHud(window,scale,player,font,wave,clock,moonphase,moonf,fullmoonphase):

                                #[x,y,w,h]
    pg.draw.rect(window, (0,0,0), [0, 400*scale, 400*scale, 50], 0)
    pg.draw.rect(window, (255,0,0), [0, 400*scale, player.health*scale, 12*scale], 0)
    healthT = font.render(f'{player.health}',False,(255,255,255))
    window.blit(healthT,(5*scale,400*scale))
    waveT = font.render(f'{wave.wave-1}',False,(255,255,255))
    window.blit(waveT,(5*scale,410*scale))
    fpsT = font.render(f'{round(clock.get_fps())}',False,(255,0,255))
    window.blit(fpsT,(200*scale,410*scale))

    
    if moonphase == 0:
        if fullmoonphase == 'r':
            moonf[12].draw(window)
        elif fullmoonphase == 'b':
            moonf[13].draw(window)
        elif fullmoonphase == 'se':
            moonf[14].draw(window)
        else:
            moonf[0].draw(window)
    else:
        moonf[moonphase].draw(window)
        
    #print(str(fullmoonphase)+''+str(moonphase))



def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)




if __name__ == "__main__":
    menu()

pg.quit()




