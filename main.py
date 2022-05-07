import random

import pygame as pg
import sys
from settings import *
from objects import *
import copy
from os import path

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        self.font=path.join("PixelatedRegular-aLKm.ttf")
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.grid=[[random.randint(0,1) if random.uniform(0,1)<0.4 else 0 for i in range(GRIDHEIGHT)] for j in range(GRIDWIDTH)]
        self.next=copy.deepcopy(self.grid)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

        for i in range(GRIDWIDTH):
            for j in range(GRIDHEIGHT):
                # count neighbours
                neibours=self.count_neibours(self.grid,i,j)
                state=self.grid[i][j]

                if (state==0 and neibours==3):
                    self.next[i][j]=1
                elif (state==1 and (neibours<2 or neibours>3)):
                    self.next[i][j]=0
                else:
                    self.next[i][j]=state
        self.grid=copy.deepcopy(self.next)


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def count_neibours(self,grid,x,y):
        sum=0
        for i in range(-1,2):
            for j in range(-1,2):
                sum+=grid[(x+i+GRIDWIDTH)%GRIDWIDTH][(y+j+GRIDHEIGHT)%GRIDHEIGHT]
        sum-=grid[x][y]

        return sum


    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        # self.all_sprites.draw(self.screen)

        for i in range(GRIDWIDTH):
            for j in range(GRIDHEIGHT):
                x=i*TILESIZE
                y=j*TILESIZE
                if self.grid[i][j]==1:
                    color=BLACK
                else:
                    color=WHITE
                pg.draw.rect(self.screen,color,(x,y,TILESIZE,TILESIZE))
                pg.draw.rect(self.screen,BLACK,(x,y,TILESIZE,TILESIZE),1)
        # fps
        self.draw_text(str(int(self.clock.get_fps())), self.font, 40, WHITE, 50, 50, align="center")
        pg.display.flip()

    def events(self):



        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mx,my=pg.mouse.get_pos()
                self.grid[mx//TILESIZE][my//TILESIZE]=1


            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

                



# create the game object
g = Game()
g.new()
g.run()
