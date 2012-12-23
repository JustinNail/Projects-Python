import pygame
from pygame.locals import * #locals has Constants

WHITE=pygame.Color(255,255,255)
BLACK=pygame.Color(0,0,0)
Dimension = 16

class Tile:
    Pos=(0,0)

    #Pos in tiles as 2-tuple(X,Y), Solid True if impassable
    def __init__(self, Pos=(0,0),Image='OpenTile.png', Solid=False,Used=False):
        self.Pos=Pos
        self.Solid=Solid
        self.Image=pygame.image.load(Image)
        self.Used=Used

    def Draw(self, Surface):
        Surface.blit(self.Image,self.Pos)
