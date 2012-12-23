import pygame, sys, Dungeon, Tile
from pygame.locals import * #locals has Constants

pygame.init() #must come before any other pygame code
fpsClock = pygame.time.Clock() # FPS limit

WINDOW_WIDTH=800
WINDOW_HIEGHT=600

windowSurfaceObj = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HIEGHT))
windowSurfaceObj.fill(pygame.Color(255,255,255))

pygame.display.set_caption('RPG')

test=Dungeon.Dungeon(1,64)

MapSurface = pygame.Surface(test.Floors[0].PixelDimensions)
ViewRect = pygame.Rect(0, 0, WINDOW_WIDTH-40, WINDOW_HIEGHT-200)

while True:#game loop            
    test.Floors[0].Draw(MapSurface)
    windowSurfaceObj.blit(MapSurface.subsurface(ViewRect),(20,0))
        
    #Events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                if not ViewRect.top - Tile.Dimension < 0:
                    ViewRect.move_ip(0,-Tile.Dimension)
                

            elif event.key == K_DOWN:
                if not ViewRect.bottom + Tile.Dimension > MapSurface.get_height():
                    ViewRect.move_ip(0,Tile.Dimension)
                

            elif event.key == K_RIGHT:
                if not ViewRect.right + Tile.Dimension > MapSurface.get_width():
                    ViewRect.move_ip(Tile.Dimension,0)
                

            elif event.key == K_LEFT:
                if not ViewRect.left - Tile.Dimension < 0:
                    ViewRect.move_ip(-Tile.Dimension,0)
                

    pygame.display.update() #Window only drawn when update called
    fpsClock.tick(30)#30 fps MUST CALL AFTER UPDATE
