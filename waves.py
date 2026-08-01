from enemys import *
import random as R


class Wavesystem:
    def __init__(self, scale):
        self.wave = 2 # it starts on 2 because if its 1 then the whole game breaks, idk why
        self.scale = scale
        self.inshop = False

        self.spawnlimit = 50
        self.totalspawn = 0
        self.spawned = 0



    def update(self, EnemyHandler):
        while (len(EnemyHandler.enemy_list) < self.spawnlimit and self.spawned < self.totalspawn):
            self.spawn_enemy(EnemyHandler)
            self.spawned += 1

        if (self.spawned == self.totalspawn and len(EnemyHandler.enemy_list) == 0 and self.wave != 1):
            self.inshop = True



    def spawn_enemy(self, EnemyHandler):
        pos = (R.randrange(0, 400) * self.scale,R.randrange(0, 400) * self.scale,)

        etype = R.choice((0,1,2))
        if self.wave > 10 and etype == 2:
            EnemyHandler.add_enemy(enemy(pos, self.scale, 1, (5+(1.125*self.wave)), 2))
        elif self.wave > 5 and etype == 1:
            EnemyHandler.add_enemy(enemy(pos, self.scale, 1, (10+(1.125*self.wave)), 1))
        else:
            EnemyHandler.add_enemy(enemy(pos, self.scale, 0.5, (10+(1.125*self.wave))))
            print(10+(1.125*self.wave))



    def newWave(self, EnemyHandler, extraenemys):
        self.totalspawn = int(5 * (1.15 ** self.wave)) + extraenemys
        #print(self.totalspawn)
        self.spawned = 0
        self.inshop = False

        while len(EnemyHandler.enemy_list) < self.spawnlimit and self.spawned < self.totalspawn:
            self.spawn_enemy(EnemyHandler)
            self.spawned += 1

        self.wave += 1