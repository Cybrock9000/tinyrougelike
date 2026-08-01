


# /\ all other stuff was deleted because of bloatware /\ (learn microsoft)


import pygame as pg

class Button:
    def __init__(self, image_path, pos, scalew = 1.0, scaleh = 1.0):
        self.image = pg.image.load(image_path).convert_alpha()
        
        og_width = self.image.get_width()
        og_height = self.image.get_height()
        new_width = int(og_width * scalew)
        new_height = int(og_height * scaleh)
        self.image = pg.transform.scale(self.image, (new_width, new_height))
        
        self.rect = self.image.get_rect(topleft = pos)
        
    def draw(self, window):
        window.blit(self.image, self.rect)
        
    def is_pressed(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()[0]
        
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed:
                return True
        return False
    
    def move(self, pos):
        self.rect = self.image.get_rect(topleft = pos)
        
    def new_image(self,image_path,pos,scalew = 1.0,scaleh = 1.0): #just a copy of the init
        self.image = pg.image.load(image_path).convert_alpha()
        
        og_width = self.image.get_width()
        og_height = self.image.get_height()
        new_width = int(og_width * scalew)
        new_height = int(og_height * scaleh)
        self.image = pg.transform.scale(self.image, (new_width, new_height))
        
        self.rect = self.image.get_rect(topleft = pos)
        
        
class BetterImage:
    def __init__(self, image_path, pos, scalew=1.0, scaleh=1.0):
        self.original_image = pg.image.load(image_path).convert_alpha()

        og_width = self.original_image.get_width()
        og_height = self.original_image.get_height()
        new_width = int(og_width * scalew)
        new_height = int(og_height * scaleh)

        self.original_image = pg.transform.scale(
            self.original_image, (new_width, new_height)
        )

        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=pos)
        
    def draw(self, window,flip='R'):
        if flip == 'R':
            window.blit(self.image, self.rect)
        if flip == 'L':
            window.blit(pg.transform.flip(self.image, True, False), self.rect)

        
    
    def move(self, pos):
        self.rect = self.image.get_rect(topleft = pos)

    def centermove(self, pos):
        self.rect = self.image.get_rect(center = pos)
        
    def new_image(self,image_path,pos,scalew = 1.0,scaleh = 1.0):
        self.image = pg.image.load(image_path).convert_alpha()
        
        og_width = self.image.get_width()
        og_height = self.image.get_height()
        new_width = int(og_width * scalew)
        new_height = int(og_height * scaleh)
        self.image = pg.transform.scale(self.image, (new_width, new_height))
        
        self.rect = self.image.get_rect(topleft = pos)

    def rotate(self, angle):
        center = self.rect.center
        self.image = pg.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=center)