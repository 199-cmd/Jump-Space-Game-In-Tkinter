from setting import *
import pygame as pg
from random import *
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spsheet = pg.image.load(filename).convert()
    def get_img(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spsheet,(0,0),(x,y,width,height))
        image = pg.transform.scale(image,(width//2,height//2))
        return image

class players(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.currentf = 0
        self.lastup = 0
        self.load_image()
        self.image = self.standing_fr[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40,height-100)
        self.pos = vec(40 , height-100)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def load_image(self):
        self.standing_fr = [self.game.spritesheet.get_img(581,1265,121,191),
                             self.game.spritesheet.get_img(584,0,121,201)]
        for fr in self.standing_fr:
            fr.set_colorkey(black)
        
        self.walk_r = [self.game.spritesheet.get_img(584,203,121,201)
                        ,self.game.spritesheet.get_img(678,651,121,207)]
        for fr in self.walk_r:
            fr.set_colorkey(black)
        
        self.walk_l = []
        for frame in self.walk_r:
            frame.set_colorkey(black)
            self.walk_l.append(pg.transform.flip(frame,True,False))

        self.jump_fr = self.game.spritesheet.get_img(416,1660,150,181)
        self.jump_fr.set_colorkey(black)   
    def jump(self):
        #jump condition
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self,self.game.platforms, False)
        self.rect.x -= 2
        if hits:
            self.vel.y = -player_jump
        
    def update(self):
        self.animate()
        self.acc = vec(0,player_gra)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -player_acc

        if keys[pg.K_RIGHT]:
            self.acc.x = player_acc

        #fritions
        self.acc.x += self.vel.x * player_friction
        #motion equ
        self.vel += self.acc
        if abs(self.vel.x)< 0.2:
            self.vel.x = 0
        self.pos += self.vel +0.5*self.acc
        if self.pos.x> width:
            self.pos.x = 0
        if self.pos.x <0:
            self.pos.x = width
            
        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.lastup > 350:
                self.lastup = now
                self.currentf = (self.currentf +1)%len(self.walk_l)
                if self.vel.x > 0:
                    self.image = self.walk_r[self.currentf]
                else:
                    self.image = self.walk_l[self.currentf]
        if not self.jumping and  not self.walking:
            if now - self.lastup >350:
                self.lastup = now
                self.currentf = (self.currentf +1)%len(self.standing_fr)
                self.image = self.standing_fr[self.currentf]

                        
class platforms(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        images = [self.game.spritesheet.get_img(0,672,380,94),
                 self.game.spritesheet.get_img(208,1879,201,100)]
        self.image = choice(images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        
        







        
    
