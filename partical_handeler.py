


class particalHandler:
    def __init__(self):
        self.partical_list = []
        self.projectile_list = []

    def update(self, window,scale,EnemyHandler,pHandler,WaveSys):
        for partical in self.partical_list:
            partical.update(window,scale)

        for projectile in self.projectile_list:
            projectile.update(window,EnemyHandler,pHandler,WaveSys)

        self.partical_list = [partical for partical in self.partical_list if not partical.remove]
        self.projectile_list = [projectile for projectile in self.projectile_list if not projectile.remove]

    def add_partical(self, partical):
        self.partical_list.append(partical)

    def add_projectile(self, projectile):
        self.projectile_list.append(projectile)