import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    global collidedBox
    
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.atExit = False
        self.dead = False
        self.touchingBlue = False
        self.touchingOrange = False

    def move(self, dx=0, dy=0):
        global collidedBox
        if self.collide_with_hazard(dx, dy):
            self.dead = True
        if self.collide_with_exit(dx, dy):
            self.atExit = True
        if self.collide_with_portal_blue(dx, dy):
            self.touchingBlue = True
        if self.collide_with_portal_orange(dx, dy):
            self.touchingOrange = True
        if self.collide_with_box(dx, dy):
            collidedBox.move(dx, dy)
        if not self.collide_with_walls(dx, dy):
            if not self.collide_with_immovable_box(dx, dy):
                self.x += dx
                self.y += dy
        

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
    
    def collide_with_exit(self, dx=0, dy=0):
        for exit in self.game.exits:
            if exit.x == self.x + dx and exit.y == self.y + dy:
                return True
        return False
    
    def collide_with_hazard(self, dx=0, dy=0):
        for hazard in self.game.hazards:
            if hazard.x == self.x + dx and hazard.y == self.y + dy:
                return True
        return False
    
    def collide_with_portal_blue(self, dx=0, dy=0):
        for portal in self.game.bluePortals:
            if portal.x == self.x + dx and portal.y == self.y + dy:
                return True
        return False
    def collide_with_portal_orange(self, dx=0, dy=0):
        for portal in self.game.orangePortals:
            if portal.x == self.x + dx and portal.y == self.y + dy:
                return True
        return False

    def collide_with_box(self, dx=0, dy=0):
        global collidedBox
        for box in self.game.boxes:
            if box.x == self.x + dx and box.y == self.y + dy:
                collidedBox = box
                return True
        return False

    def collide_with_immovable_box(self, dx=0, dy=0):
        for box in self.game.boxes:
            if box.x == self.x + dx and box.y == self.y + dy:
                return True
        return False
        
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("Wall.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Exit(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.exits
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("Exit.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class Lava(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.hazards
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("Lava.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class PortalOrange(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.orangePortals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("OrangePortal.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class PortalBlue(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.bluePortals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("BluePortal.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class Box(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.boxes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("Box.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.immovable = False
    
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
    
    def collide_with_box(self, dx=0, dy=0):
        for box in self.game.boxes:
            if box.x == self.x + dx and box.y == self.y + dy:
                return True
        return False
    
    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            if not self.collide_with_box(dx, dy):
                self.x += dx
                self.y += dy
        
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE