
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



class Loc:
    # Location object, tracks information about a single location on a map.

    def __init__(self,name,description, interactions,state):
                self.name = name
                self.desc = description
                self.interactions = interactions # Probably an array of "general" interactions
                self.state = state # 0 = Passable, 1 = Permanently Impassable, 2 = Temporarily Impassable
                self.coords = [-1, -1] # Location on the map.
                self.explored = 0 # Has the player "Discovered" this.

    def getCoords(self):
        return self.coords
class Item:
    #Items

    def __init__(self,name,description):
        self.name = name
        self.desc = description

