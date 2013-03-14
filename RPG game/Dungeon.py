import pygame,Room, Map,Tile, random
from pygame.locals import * #locals has Constants

class Dungeon:
    Floors=[]
    def __init__(self, NumFloors, FloorSize):
        for Floor in range(0,NumFloors):
            self.Floors.append(DungeonFloor(FloorSize))

class DungeonFloor:
    Rooms=[]
    
    HallwayMin=4
    HallwayMax=20
    RoomMin=6
    RoomMax=12

    FloorImage='OpenTile.png'
    WallImage='StoneTile.png'
    DebugImage='DebugTile.png'
    
    '''
    New Algorithm
    0: fill map with solid(Dirt)
    1: Dig initial room
    2: pick a feature
    3: pick a wall
    4: Pick Feature
    5: build new feature next to wall
        a: see if there is room
        b: Add feature
        c: Connect features
    6: repeat 2-5 until dungeon is full
    7: Furnish and populate dungeon
    8: add stairs
    '''
    #Makes a Size x Size square dungeon map
    def __init__(self, Size):
        self.Size = Size
        self.PixelDimensions=(self.Size*Tile.Dimension,self.Size*Tile.Dimension)
        #0: fill map with solid(Dirt)
        self.Map=Map.Map(self.Size)
        
        random.seed(3)

        #1: Dig initial feature
        RoomSize=(random.randint(5,11),random.randint(5,11))
        self.addRoom((1,1),RoomSize,self.FloorImage,self.WallImage,0)

        #2-6
        self.buildFeatures(20)

        #7-8
        #TO DO
    def buildFeatures(self, NumFeatures):
        if NumFeatures < 1:
            return
        #2: Pick a feature
        Room = self.Rooms[random.randint(0,len(self.Rooms)-1)]
        #print('Room: ',Room.Pos)
        #3: Pick a wall
        Wall,WallTile,WallTilePos = self.pickWall(Room)
        #print('Wall: ',Wall,' Tile: ',WallTile,WallTilePos)
            
        #4: Pick Feature
        Feature, RoomSize = self.selectFeature(Room,Wall)

        #5: Build new feature next wall

        #5a: Check if there is room
        if Wall is 1:#North Wall
            RoomPos=(WallTilePos[0]-(RoomSize[0]-1),WallTilePos[1]-(RoomSize[1]-1))
        elif Wall is 2:#East Wall
            RoomPos=(WallTilePos[0],WallTilePos[1])
        elif  Wall is 3:#South Wall
            RoomPos=(WallTilePos[0],WallTilePos[1])
        elif Wall is 4:#West Wall
            RoomPos=(WallTilePos[0]-RoomSize[0],WallTilePos[1]-RoomSize[1])
            
        if RoomPos[0] < 0 or RoomPos[1] < 0 or not self.Map.checkSpace(RoomSize,RoomPos):#Not a valid room location/size
            self.buildFeatures(NumFeatures)#if invalid, start over
            return
        
        #5b: add feature
        try:
            self.addRoom(RoomPos,RoomSize,self.FloorImage,self.WallImage,Feature)
            Room.ConnectedRooms.append(self.Rooms[len(self.Rooms)-1])
            self.Rooms[len(self.Rooms)-1].ConnectedRooms.append(Room)


            #5c: Connect Features
            if Wall is 1:#North Wall
                self.Map.changeTile((WallTilePos[0],WallTilePos[1]),self.DebugImage,False,True)    
            elif Wall is 2:#East Wall
                self.Map.changeTile((WallTilePos[0],WallTilePos[1]),self.DebugImage,False,True)
            elif  Wall is 3:#South Wall
                self.Map.changeTile((WallTilePos[0]+1,WallTilePos[1]),self.DebugImage,False,True)
            elif Wall is 4:#West Wall
                self.Map.changeTile((WallTilePos[0],WallTilePos[1]),self.DebugImage,False,True)
            

            
            #6: repeat 2-5 until dungeon is full
            self.buildFeatures(NumFeatures-1)
            return
        except IndexError:
            #print('Reject: Out of Bounds')
            self.buildFeatures(NumFeatures)
            return
        
    def addRoom(self, Pos, Size,FloorImage,WallImage,Type):
        self.Rooms.append(self.Map.addRoom(Pos, Size,FloorImage,WallImage,Type))

    def pickWall(self, Room):
        #Pick a wall
        Wall=0
        if Room.Type is 1:#Horizontal Hallway. Weighted towards East\West Walls
            Wall=random.choice([1,2,2,2,3,4,4,4])
        elif Room.Type is 2:#Vertical Hallway. Weighted towards North\South Walls
            Wall=random.choice([1,1,1,2,3,3,3,4])
        else:#Room, all walls equal chance
            Wall = random.randint(1,4)

        WallTile=0
        WallTilePos=(0,0)
        
        if Wall is 1:#North wall
            #Pick a specific Tile along the wall
            WallTile=random.randint(1, Room.Size[0]-1)
            WallTilePos=(WallTile+Room.Pos[0],Room.Pos[1])
           
        elif Wall is 2:#East wall
            #Pick a specific Tile along the wall
            WallTile=random.randint(1,Room.Size[0]-1)
            WallTilePos=(Room.Pos[0]+Room.Size[0],WallTile+Room.Pos[1])
            
        elif Wall is 3:#South wall
            #Pick a specific Tile along the wall
            WallTile=random.randint(1, Room.Size[0]-1)
            WallTilePos=(WallTile+Room.Pos[0],Room.Pos[1]+Room.Size[1])
            
        elif Wall is 4:#West wall
            #Pick a specific Tile along the wall
            WallTile=random.randint(1,Room.Size[1]-1)
            WallTilePos=(Room.Pos[0],WallTile+Room.Pos[1])

        return Wall,WallTile,WallTilePos
    
    def selectFeature(self,Room,Wall):
        '''
        0:Room
        1:Horizontal Hallway (1 tile tall room)
        2:Vertical Hallway (1 tile wide room)
        '''
        Feature=-1
        if Room.Type is 0:#Room
            #Rooms only spawn Hallways
            #Vertical on North and South Walls
            #Horizontal on East and West
            if Wall is 1:#N
                Feature = 1
                RoomSize=(self.HallwayMin,random.randint(self.HallwayMin,self.HallwayMax))
            elif Wall is 2:#E
                Feature = 2
                RoomSize=(random.randint(self.HallwayMin,self.HallwayMax),self.HallwayMin)
            elif Wall is 3:#S
                Feature = 1
                RoomSize=(self.HallwayMin,random.randint(self.HallwayMin,self.HallwayMax))
            elif Wall is 4:#W
                Feature = 2
                RoomSize=(random.randint(self.HallwayMin,self.HallwayMax),self.HallwayMin)

        #Hallways can spawn more Hallways or Rooms     
        elif Room.Type is 1:#Horizontal Hallway
            #Only Vertical Hallways on North and South Walls
            if Wall is 1 or Wall is 3:
                Feature = 2
                RoomSize=(self.HallwayMin,random.randint(self.HallwayMin,self.HallwayMax))
            #Rooms on East and West Walls        
            elif Wall is 2 or Wall is 4:
                Feature = 0
                RoomSize=(random.randint(self.RoomMin,self.RoomMax),random.randint(self.RoomMin,self.RoomMax))
                
                        
        elif Room.Type is 2:#Vertical Hallway
            #Only Horizontal Hallways on East and West Walls
            if Wall is 2 or Wall is 4:
                Feature = 1
                RoomSize=(random.randint(self.HallwayMin,self.HallwayMax),self.HallwayMin)
            #Rooms on North and South Walls        
            elif Wall is 1 or Wall is 3:
                Feature = 0
                RoomSize=(random.randint(self.RoomMin,self.RoomMax),random.randint(self.RoomMin,self.RoomMax))
                

        #print('Feature: ',Feature,' Size: ',RoomSize)
        
        return Feature,RoomSize
        
        
    def Draw(self, Surface):
        self.Map.Draw(Surface)
            
            
