import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.SCALED, vsync=1)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        global levelMaps
        global mapIndex
        levelMaps = ['map1.txt', 'map2.txt', 'map3.txt']
        mapIndex = 0
        self.load_map()
        self.background = pg.Surface(self.screen.get_size())
        self.background = pg.transform.scale(self.background, self.screen.get_size())
        for row in range(GRIDHEIGHT):
            for col in range(GRIDWIDTH):
                self.background.blit(pg.image.load("FloorTile.png"), (col * TILESIZE, row * TILESIZE))

    # function to load the map
    def load_map(self):
        global levelMaps
        global mapIndex
        game_folder = path.dirname(__file__)
        self.map = Map(game_folder, levelMaps, mapIndex)
    
    # function to change to the next map at the end of a level
    def next_map(self):
        global levelMaps
        global mapIndex
        mapIndex = self.map.checkIndex(mapIndex, levelMaps)
        self.load_map()

    # setup for a new level
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.exits = pg.sprite.Group()
        self.hazards = pg.sprite.Group()
        self.bluePortals = pg.sprite.Group()
        self.orangePortals = pg.sprite.Group()
        self.boxes = pg.sprite.Group()
        for row, tiles in enumerate(self.map.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'E':
                    Exit(self, col, row)
                if tile == 'X':
                    Lava(self, col, row)
                if tile == 'O':
                    self.orangePortal = PortalOrange(self, col, row)
                if tile == 'B':
                    self.bluePortal = PortalBlue(self, col, row)
                if tile == '@':
                    Box(self, col, row)
            self.camera = Camera(self.map.width, self.map.height)
                   
    # end of level cleanup 
    def cleanup(self):
        for sprite in self.all_sprites:
            sprite.kill()

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
        self.camera.update(self.player)
        
        # player checks
        if self.player.atExit:
            self.cleanup()
            self.next_map()
            self.new()
        if self.player.dead:
            self.cleanup()
            self.new()
        if self.player.touchingBlue:
            self.player.y = self.orangePortal.y
            self.player.x = self.orangePortal.x + 1
            self.player.touchingBlue = False
        if self.player.touchingOrange:
            self.player.y = self.bluePortal.y
            self.player.x = self.bluePortal.x + 1
            self.player.touchingOrange = False
    
    # draw the gridlines
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)
                if event.key == pg.K_r:
                    self.cleanup()
                    self.new()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
