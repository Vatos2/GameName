import numpy as np


def printArray(args):
    print("\t".join(args))


class Player:
    # The Player Object
    def __init__(self,inventory, hunger, health, energy, location):
            self.inventory = inventory # What items the player has, a list.
            self.hunger = hunger # Hunger, not going to worry about implementing this until later.
            self.health = health # Player health, we don't want this to hit 0
            self.maxHealth = 100
            self.energy = energy # Player's energy, used for action economy.
            self.maxEnergy = 20 # Not a "Hard" Maximum, sleeping will set your current energy to your "max" energy.
            self.location = location # The current location of the player.
            self.coord = location.getCoords

    def isAlive(self):
        if self.health <= 0:
            return False
        else:
            return True
    def modHealth(self,modifier):
        self.health += modifier

    def modEnergy(self,modifier):
        self.energy += modifier

    def setLocation(self,newLoc):
        self.location = newLoc

    def pickup(self,item):
        self.inventory.append(item)
        print("You got the ", "<",item.name,">", "!")

    def listInventory(self):
        if len(self.inventory) == 0:
            print("Your inventory is empty!")
        else:
            for i in range (0,len(self.inventory)):
                print(str(i+1)+".",self.inventory[i].name)




class Loc:
    # Location object, tracks information about a single location on a map.
    # NOTES ON COORDINATE TRACKING: FOR map[x][y], X IS ACTUALLY THE Y COORDINATE, AND X IS THE X IN PYTHON.
    # OUR MAP STARTS AT 0,0 IN THE TOP LEFT CORNER!

    def __init__(self,name,cnct,description, vague, interactions,state):
                self.name = name
                self.desc = description # A description once it's discovered.
                self.vague = vague # The description given "at a glance", used in the "check" action.
                self.interactions = interactions # Probably an array of "general" interactions
                self.state = state # 0 = Passable, 1 = Permanently Impassable, 2 = Temporarily Impassable
                self.coords = [-1, -1] # Location on the map, y and X
                self.explored = 0 # Has the player "Discovered" this 0 for no 1 for yes.
                self.cnct = cnct  # 4 Letter Representation of the location.

    def getCoords(self):
        return self.coords

    def isPassable(self):
        if self.state == 0:
            return True

        elif self.state == 1:
            print("That location is impassable!")
            return False
        elif self.state == 2:
            print("That location is impassable... for now.")
            return False
    def isExplored(self):
        if self.explored == 0:
            return False
        else:
            return True

    def discover(self):
        self.explored = 1
        print("You've discovered the ", self.name)



class Item:
    #Items

    def __init__(self,name,description):
        self.name = name
        self.desc = description



class Instance:
        # The "Game" Object, will allow us to pass our initialization into the main game function.
        # All we need to pass to the instance are the player, and the map since those two objects contain all of our objs
        # If you're unsure where to put any functions, it's probably safe to assume you can put it here.

        def __init__(self, player, map):
            self.player = player
            self.map = map
            self.playery = self.player.location.coords[0]
            self.playerx = self.player.location.coords[1]

        def updatePlayerLoc(self,y,x):
            self.player.setLocation(self.map[y][x])
            self.playery = self.player.location.coords[0]
            self.playerx = self.player.location.coords[1]
            print("You move to: ", self.map[self.playery][self.playerx].name)

        def move(self,direction):
            # For moving the player around, we'll take as input cardinal directions N,W,E,S.
            # Remember len(map) is y length, len(map[0]) is xlength!
            direction = direction.upper()
            if direction == "N":
                if (self.playery - 1 < len(self.map)):
                    if (self.map[self.playery - 1][self.playerx]).isPassable():
                        self.updatePlayerLoc(self.playery - 1,self.playerx)
                        print("You move north.")
                        if self.player.location.isExplored():
                            self.player.location.discover()


            elif direction == "S":
                if (self.playery + 1 > 0):
                    if (self.map[self.playery + 1][self.playerx]).isPassable():
                        self.updatePlayerLoc(self.playery + 1,self.playerx)
                        print("You move south.")
                        if self.player.location.isExplored():
                            self.player.location.discover()
                        print("You are now in: ", self.player.location.name)
            elif direction == "W":
                if (self.playerx - 1 > 0):
                    if (self.map[self.playery][self.playerx-1]).isPassable():
                        self.updatePlayerLoc(self.playery,self.playerx-1)
                        print("You move west.")
                        if self.player.location.isExplored():
                            self.player.location.discover()
                        print("You are now in: ", self.player.location.name)

            elif direction == "E":
                if (self.playerx + 1 < len(self.map[0])):
                    if (self.map[self.playery][self.playerx+1]).isPassable():
                        self.updatePlayerLoc(self.playery, self.playerx+1)
                        print("You move east.")
                        if self.player.location.isExplored():
                            self.player.location.discover()
                        print("You are now in: ", self.player.location.name)

        def check(self):
            # Gives a vague description of things in each cardinal direction, eventually it should check if explored.
            # and if it is explored, give the full desc instead of the vague
            try:
                print("Your current location:",self.map[self.playery][self.playerx].name)
                print("To the North:", self.map[self.playery - 1][self.playerx].vague)
                print("To the South:", self.map[self.playery + 1][self.playerx].vague)
                print("To the East:",self.map[self.playery][self.playerx + 1].vague)
                print("To the West:", self.map[self.playery][self.playerx - 1].vague)

            except:
                print("You've perceived something outside of the map! This shouldn't happen!")

        def showMap(self,setting):
            # Prints the map to console, setting determines how much info is given FULL shows even unexplored areas,
            # VARB shows only the explored areas
            i=0
            print(" [[0]]\t[[1]]\t[[2]]\t[[3]]\t")
            for row in self.map:

                print(i,"|",sep="", end="")
                i+=1
                printArray(x.cnct for x in row)

        def where(self): #Prints the player's location.
            print("You are in: ",self.player.location.name,self.player.location.coords)

        def getLoc(self,y,x): # Tells you what is at the given coordinates
            try:
                print("Y: ",y, "X: ",x)
                print(self.map[y][x].name)
            except:
                print("Y: ", y, "X: ", x)
                print("Location out of bounds!")
