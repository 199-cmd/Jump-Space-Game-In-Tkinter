import pygame as pg
import random
from os import path
from setting import *
from sprites import *

class Game:
    def __init__(self):
        self.running = True
        pg.init()   
        pg.mixer.init()
        self.screen = pg.display.set_mode((width,height))
        pg.display.set_caption("Nitya")
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(font_n)
        self.load_data()
    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir,sheetload))
        

    def new(self):
        self.score = 0
        self.sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = players(self)
        self.sprites.add(self.player)
        for plat in platform_list:
            p = platforms(self,*plat)
            self.sprites.add(p)
            self.platforms.add(p)
        self.run()
        
    def run(self):        
        self.playing = True
        while self.playing:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()
            

    def update(self):
       self.sprites.update()
       if self.player.vel.y >0:
           hits = pg.sprite.spritecollide(self.player , self.platforms, False)
           if hits:
               if self.player.pos.y < hits[0].rect.bottom:
                   self.player.pos.y = hits[0].rect.top
                   self.player.vel.y = 0

       # if player is in 1/4 of screen
       if self.player.rect.top <= height/4:
            self.player.pos.y += max(abs(self.player.vel.y),2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y),2)
                if plat.rect.top >= height:
                    plat.kill()
                    self.score += 10

       if self.player.rect.bottom > height:
            self.playing = False
       #making platforms
       while len(self.platforms) < 6:
           wi = randrange(50, 100)
           p = platforms(self,randrange(0,width - wi)
                         ,randrange(-75, -30))
           self.platforms.add(p)
           self.sprites.add(p)
           
           
       

                    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        self.screen.fill(sky)
        self.sprites.draw(self.screen)
        self.draw_text(str(self.score),22,white,width/2,15)
        pg.display.flip()

    def show_start_screen(self):
        if not self.running:
            return
        self.screen.fill(sky)
        self.draw_text("Jump into the Space",48,white,width/2,height/4)
        self.draw_text("arrows to move, space to jump",22,white,width /2,height /2)
        self.draw_text("press any key to play",22,white,width/2,height * 3/4)
        pg.display.flip()
        self.waiting()
        
    def show_go_screen(self):
        self.screen.fill(sky)
        self.draw_text("GAME FINISHED",48,white,width/2,height/4)
        self.draw_text("Score:"+str(self.score),22,white,width /2,height /2)
        self.draw_text("Press any key to play",22,white,width/2,height * 3/4)
        pg.display.flip()
        self.waiting()

        
    def waiting(self):
        wait = True
        while wait:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    wait = False
                    self.running = False
                if event.type == pg.KEYUP:
                    wait =False
                    
        
    def draw_text(self,text,size,color, x ,y ):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text ,True ,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface,text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
