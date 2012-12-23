import pygame, Tile, Room
from pygame.locals import * #locals has Constants

class Map:
    Tiles=[]

    def __init__(self, Size=1):
        self.Size=Size
        #1: Fill the whole map with solid earth
        #print("Filling with Dirt.png")
        for i in range (self.Size):
            self.Tiles.append([])
            for j in range (self.Size):
                Pos=(i*Tile.Dimension, j*Tile.Dimension)
                self.Tiles[i].append(Tile.Tile(Pos,'DirtTile.png',True))


    def changeTile(self,Pos,ImageName,Solid,Used):
        self.Tiles[Pos[0]][Pos[1]].Image=pygame.image.load(ImageName)
        self.Tiles[Pos[0]][Pos[1]].Solid=Solid
        self.Tiles[Pos[0]][Pos[1]].Used=Used

    
    
    def addRoom(self, Pos, Size,FloorImage,WallImage,Type):
        #print('Building ',Size,' Room at ',Pos)
        for i in range(Size[0]):
            for j in range(Size[1]):
                #Border uses WallImage
                if (i == 0) or (i == Size[0]-1) or (j == 0) or (j == Size[1]-1):
                    #self.changeTile((Pos[0]+1,Pos[1]+j),WallImage,True,True)
                    
                    self.Tiles[Pos[0]+i][Pos[1]+j].Image=pygame.image.load(WallImage)
                    self.Tiles[Pos[0]+i][Pos[1]+j].Solid=True
                    self.Tiles[Pos[0]+i][Pos[1]+j].Used=True
                    
                #The rest uses FloorImage
                else:
                    #self.changeTile((Pos[0]+1,Pos[1]+j),FloorImage,False,True)
                    
                    self.Tiles[Pos[0]+i][Pos[1]+j].Image=pygame.image.load(FloorImage)
                    self.Tiles[Pos[0]+i][Pos[1]+j].Solid=False
                    self.Tiles[Pos[0]+i][Pos[1]+j].Used=True
                    
        return Room.Room(Pos,Size,Type)

    def checkSpace(self,RoomSize,RoomPos):
    #RoomSize and RoomPos are 2-tuples
        for i in range(RoomSize[0]):
            for j in range(RoomSize[1]):
                #print("Checking (",i+RoomPos[0],j+RoomPos[1],")")
                try:
                    if self.Tiles[i+RoomPos[0]][j+RoomPos[1]].Used:#Check to see if it would overlap a pre-existing room
                        #print('Reject: Overlap')
                        #input()
                        return False
                except IndexError: #Check to see if it exceeds the dungeon space
                    #print('Reject: Out of Bounds')
                    #input()
                    return False
        return True

    def Draw(self,Surface):
        for i in range(self.Size):
            for j in range(self.Size):
                self.Tiles[i][j].Draw(Surface)

                
