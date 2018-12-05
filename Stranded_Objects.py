import time
import random
import sys
random.seed(time.time())
def printArray(args):
    print("\t".join(args))

def getRandom():
    return random.randint(0,100)

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

    def exhausted(self): #returns true if you are out of energy.
        if self.energy <= 0:
            return True
        return False

    def pickup(self,item):
        self.inventory.append(item)
        print("You got the ", "<",item.name,">", "!")
    def remove(self,itemname):
        for item in self.inventory:
            if item.name == itemname:
                self.inventory.remove(item)
                print("You lost the ", "<", item.name, ">", "!")


    def listInventory(self):
        if len(self.inventory) == 0:
            print("Your inventory is empty!")
        else:
            for i in range (0,len(self.inventory)):
                print(str(i+1)+".",self.inventory[i].name)

    def checkforitem(self,itemname): # For use in item dependant event outcomes
        if len(self.inventory) == 0:
            return False
        else:
            for i in range(0, len(self.inventory)):
                if self.inventory[i].name == itemname:
                    return True
            return False



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
                self.cnct = cnct  # 4 Letter Representation of the location, for maps.

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
            if not self.player.location.isExplored():
                self.player.location.discover()
                self.eventcheck()

        def move(self,direction):
            # For moving the player around, we'll take as input cardinal directions N,W,E,S.
            # Remember len(map) is y length, len(map[0]) is xlength!
            direction = direction.upper()
            if direction == "N":
                if (self.playery - 1 < len(self.map)):
                    if (self.map[self.playery - 1][self.playerx]).isPassable():
                        self.updatePlayerLoc(self.playery - 1,self.playerx)
                        self.player.modEnergy(-1)


            elif direction == "S":
                if (self.playery + 1 > 0):
                    if (self.map[self.playery + 1][self.playerx]).isPassable():
                        self.updatePlayerLoc(self.playery + 1,self.playerx)
                        self.player.modEnergy(-1)
            elif direction == "W":
                if (self.playerx - 1 > 0):
                    if (self.map[self.playery][self.playerx-1]).isPassable():
                        self.updatePlayerLoc(self.playery,self.playerx-1)
                        self.player.modEnergy(-1)


            elif direction == "E":
                if (self.playerx + 1 < len(self.map[0])):
                    if (self.map[self.playery][self.playerx+1]).isPassable():
                        self.updatePlayerLoc(self.playery, self.playerx+1)
                        self.player.modEnergy(-1)


        def check(self):
            # Gives a vague description of things in each cardinal direction, eventually it should check if explored.
            # and if it is explored, give the full desc instead of the vague
            try:
                print("Your current location:",self.map[self.playery][self.playerx].name)
                print("To the North:", self.map[self.playery - 1][self.playerx].vague)
                print("To the South:", self.map[self.playery + 1][self.playerx].vague)
                print("To the East:",self.map[self.playery][self.playerx + 1].vague)
                print("To the West:", self.map[self.playery][self.playerx - 1].vague)

            except IndexError:
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



        def eventcheck(self):
            if self.player.location.name == "Jungle":
                self.event("wolfattack",100)

        def event(self,eventname,percentchance):  # Not a great way to do this probably, but oh well!
            chance =random.randint(0,100)
            if chance <= percentchance:
                if eventname == "wolfattack":
                    print("\nOut of the trees comes a single wolf, it attacks you. \nWhat do you do?")

                    print("F. Fight it off\n"
                          "R. Run away.")
                    choice = input()
                    choice = choice.upper()

                    if choice == 'F':
                        if self.player.checkforitem("Machete"):
                            print("Using your Machete, you easily kill the wolf.")
                            wolfmeat = Item("Wolf Meat","Can be cooked, and eaten.")
                            self.player.pickup(wolfmeat)
                        else:
                            roll = getRandom()
                            if roll <= 50:
                                print("You fail to fight off the wolf with your bare hands, and are killed.")
                                self.isover()
                            elif roll > 50:
                                print("You manage to scare the wolf off with your bare hands, but are bitten multiple\
                                 times in the process.")
                                self.player.modHealth(-50)

                    else:
                        print("You run away, losing 2 energy.")
                        self.player.modEnergy(-2)

                elif eventname == "passout":
                    print("You've pushed yourself past your limits, and have passed out due to lack of energy.")
                    roll = getRandom()
                    if roll <= 50:
                        print("You are eaten alive in your sleep, that's rough!")
                        self.isover()
                    elif roll > 50:
                        print("You manage to make it back to the beach just in time to fall asleep safely.")
                        self.player.energy = self.player.maxEnergy/2

                elif eventname == "SLEEP":
                    print("You sleep until the next day.")
                    self.player.energy = self.player.maxEnergy

                elif eventname == "FISH":
                    roll = getRandom()
                    if roll <=25:
                        print("You fail to catch anything, and just tire yourself out.")
                        self.player.modEnergy(-1)
                    else:
                        print("You catch a fish with your hands.")
                        rwfish = Item("Raw Fish", "A dead fish, could be cooked.")
                        self.player.pickup(rwfish)

                elif eventname == "COOK":
                        for item in self.player.inventory:
                            if item.name == "Raw Fish":
                                ckfish = Item("Cooked Fish", "A delicious cooked fish.")
                                self.player.remove("Raw Fish")
                                self.player.pickup(ckfish)


                # If the event doesn't trigger,we just move on.


        def isover(self):
            sys.exit("Thanks for playing!")

        def useitem(self,item):
            if item.name == "Electronics Kit":
                if self.player.location.name == "Radio Tower":
                    print("Using the Electronics Kit you've fixed the radio tower, and have called for help.",
                          "A few days later, you are rescued. You've escaped the island, congratulations!")
                    self.isover()

            elif item.name == "Raw Fish":
                print("You ate the raw fish, it wasn't very good.(+5e)")
                self.player.modEnergy(5)
            elif item.name == "Cooked Fish":
                print("You ate the cooked fish, it was great.(+12e)")
                self.player.modEnergy(12)
            else:
                print("That item doesn't do anything here!")

        def passout(self):
            print("You pass out from exhaustion!")
            self.event("passout", 100)

        def useLocation(self):
            location = self.player.location
            if len(self.player.location.interactions) <= 0:
                print("This location currently has no interactions.")
            else:
                print("Enter the number of the interaction you'd like to perform:")
                i = 0
                for option in location.interactions:
                    print(i+1, ".", option)
                    i+=1
                choice = int(input())
                selection = location.interactions[choice-1]
                self.player.modEnergy(-1)
                self.event(selection, 100)