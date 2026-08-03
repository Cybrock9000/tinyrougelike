


class enemyHandler:
    def __init__(self):
        self.enemy_list = []

    def update(self, window, playerpos,player,projectile_list,fireDamage,pHandler,waterDamage,lightDamage,shadowDamage,shadowOrbs):
        for enemy in self.enemy_list:
            enemy.update(window, playerpos, self.enemy_list,player,projectile_list,fireDamage,pHandler,waterDamage,lightDamage,shadowDamage,shadowOrbs)

        self.enemy_list = [enemy for enemy in self.enemy_list if not enemy.remove]

    def add_enemy(self, enemy):
        self.enemy_list.append(enemy)
