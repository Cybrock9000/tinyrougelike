


class enemyHandler:
    def __init__(self):
        self.enemy_list = []
        self.pet_list = []

    def update(self, window, playerpos,player,projectile_list,fireDamage,pHandler,waterDamage,lightDamage,shadowDamage,shadowOrbs,shake):
        for enemy in self.enemy_list:
            enemy.update(window, playerpos, self.enemy_list,player,projectile_list,fireDamage,pHandler,waterDamage,lightDamage,shadowDamage,shadowOrbs,self.pet_list,shake)
            
        for pet in self.pet_list:
            pet.update(window, playerpos, self.enemy_list,player,projectile_list,fireDamage,pHandler,waterDamage,lightDamage,shadowDamage,shadowOrbs,shake)

        self.enemy_list = [enemy for enemy in self.enemy_list if not enemy.remove]
        self.pet_list = [pet for pet in self.pet_list if not pet.remove]

    def add_enemy(self, enemy):
        self.enemy_list.append(enemy)

    def add_pet(self, pet):
        self.pet_list.append(pet)
