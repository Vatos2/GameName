
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
        self.inventory = self.inventory.append(item)
        print("You got the ", "<",item.name,">", "!")

    def listInventory(self):
        print(self.inventory)



class Loc:
    # Location object, tracks information about a single location on a map.

    def __init__(self,name,description, interactions,state):
                self.name = name
                self.desc = description
                self.interactions = interactions # Probably an array of "general" interactions
                self.state = state # 0 = Passable, 1 = Permanently Impassable, 2 = Temporarily Impassable
                self.coords = [-1, -1] # Location on the map.
                self.explored = 0 # Has the player "Discovered" this 0 for no 1 for yes.

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
        self.playerx = self.player.location.coords[0]
        self.playery = self.player.location.coords[1]

    def updatePlayerLoc(self,x,y):
        self.player.setLocation(self.map[x][y])
        self.playerx = self.player.location.getCoords[0]
        self.playery = self.player.location.getCoords[1]

    def move(self,direction):
        # For moving the player around, we'll take as input cardinal directions N,W,E,S.
        # Remember len(map) is y length, len(map[0]) is xlength!
        direction = direction.upper()
        if direction == "N":
            if (self.player.playery + 1 < len(self.map)):
                if (self.map[self.player.playerx][self.player.playery + 1]).isPassable():
                    self.updatePlayerLoc(self.player.playerx,self.player.playery + 1)
                    print("You move north.")
                    if self.player.location.isExplored():
                        self.player.location.discover()


        elif direction == "S":
            if (self.player.playery - 1 > 0):
                if (self.map[self.player.playerx][self.player.playery - 1]).isPassable():
                    self.updatePlayerLoc(self.player.playerx,self.player.playery - 1)
                    print("You move south.")
                    if self.player.location.isExplored():
                        self.player.location.discover()
                    print("You are now in: ", self.player.location.name)
        elif direction == "W":
            if (self.player.playerx - 1 > 0):
                if (self.map[self.player.playerx - 1][self.player.playery]).isPassable():
                    self.updatePlayerLoc(self.player.playerx-1,self.player.playery)
                    print("You move west.")
                    if self.player.location.isExplored():
                        self.player.location.discover()
                    print("You are now in: ", self.player.location.name)

        elif direction == "E":
            if (self.player.playerx + 1 < len(self.map[0])):
                if (self.map[self.player.playerx + 1][self.player.playery]).isPassable():
                    self.updatePlayerLoc(self.player.playerx + 1, self.player.playery)
                    print("You move east.")
                    if self.player.location.isExplored():
                        self.player.location.discover()
                    print("You are now in: ", self.player.location.name)