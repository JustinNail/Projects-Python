import pygame, Tile

class Room:
    Size=(1,1)
    Pos=(0,0)
    Type=0
    ConnectedRooms=[]
    
    #Dimensions in Num. of Tiles, 2-tuple (Col,Row)
    #Type 0: Normal Room
    #Type 1: Horizontal Hallway
    #Type 2: Vertical Hallway
    def __init__(self,Pos=(0,0), Size=(1,1), Type=0):
        self.Size=Size
        self.Pos=Pos
        self.Type=Type
        

   
