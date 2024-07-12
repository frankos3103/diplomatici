import re
import random

class Empire:
    empireList = []
    def __init__(self, name, color=None):
        self.name = name
        self.color = color
        Empire.empireList.append(self)

class Unit:

    def __init__(self, empire):
        self.empire = empire
        if isinstance(empire, Empire):
            self.name = self.empire.name
        elif empire == None:
            self.name = None

class Region:

    regionList = []
    regionDict = {}

    def __init__(self, name):
        self.name = name
        self.borders = None
        self.isCenter = False
        self.startEmpire = None
        self.controlledBy = None

        self.occupant = Unit(None)
        self.nextOccupant = self.occupant
        self.movingTo = None
        self.willMove = False
        self.defSupport = None
        self.atkSupport = (None, None)
        self.standoff = False
        self.defeatedBy = None
        self.loser = Unit(None)
        self.retiringInto = None
        Region.regionList.append(self)
        Region.regionDict[name] = self

    def attack(self, attacked):
        if attacked not in self.borders:
            return
        self.movingTo = attacked
    
    def addAtkSupport(self, supported, attacked):
        if (self not in attacked.borders) or (supported not in attacked.borders):
            return
        self.atkSupport = (supported, attacked)
    
    def addDefSupport(self, defended):
        if defended not in self.borders:
            return
        self.defSupport = defended

    def newUnit(self, unit):
        self.occupant = unit
        self.nextOccupant = unit
        if self.isCenter:
            self.controlledBy = unit.empire

    def buildUnit(self):
        empire = self.startEmpire
        if empire == None:
            return
        centers = countCenters(empire)
        units = countUnits(empire)
        if centers > units:
            self.newUnit(Unit(empire))
                
    def clearMove(self):
        self.movingTo = None
        self.defSupport = None
        self.atkSupport = (None, None)

    def defenseEvaluation(self):
        if self.occupant.name == None:
            return 0
        defenseValue = 1
        if self.movingTo != None:
            return defenseValue
        for supporter in self.borders:
            if supporter.defSupport == self and supporter.listAttackers() == []:
                defenseValue += 1
        return defenseValue
    
    def retreat(self, other):
        if self.loser.name != None and self.defeatedBy != other and other.standoff == False and other.occupant.name == None:
            self.retiringInto = other

                
    def listAttackers(self):
        attackers = []
        for region in self.borders:
            if region.movingTo == self:
                attackers.append(region)
        return attackers

    def powerEvaluation(self, destination):
        if self.movingTo != destination:
            return 0
        attackValue = 1
        for supporter in destination.borders:
            if supporter.atkSupport != (self, destination):
                continue
            elif len(supporter.listAttackers()) >= 1 and supporter.listAttackers() != [destination]:
                continue
            elif supporter.listAttackers() == []:
                attackValue += 1
            elif supporter.listAttackers() == [destination]:
                defenseValue = supporter.defenseEvaluation()
                destinationValue = 1
                for region in supporter.borders:
                    if region.atkSupport == (destination, supporter) and region.listAttackers() == []:
                        destinationValue += 1
                if destinationValue <= defenseValue:
                    attackValue += 1
        return attackValue

    def invade(self, other):
        other.nextOccupant = self.occupant
        other.defeatedBy = self
        self.loser = Unit(None)
        self.willMove = True
        if other.willMove == False:
            other.loser = other.occupant
        if self.nextOccupant == self.occupant:
            self.nextOccupant = Unit(None)

    def evaluate(self):
        current = self
        next = self.movingTo
        while current.movingTo != None:
            valueAttackers = {r: r.powerEvaluation(next) for r in next.borders}
            winnerValue = max(valueAttackers.values())
            bestAttackers = [r for r in valueAttackers if valueAttackers[r] == winnerValue]
            winner = bestAttackers[0]
            defenseValue = next.defenseEvaluation()
            if len(bestAttackers) == 1 and next.powerEvaluation(winner) < winnerValue and winner == current:
                if winnerValue > defenseValue and winner.occupant.name != next.occupant.name:
                    self.invade(self.movingTo)
                    return
                elif winnerValue == defenseValue == 1 and next.movingTo != current:
                    current = next
                    next = next.movingTo
                    if current == self:
                        self.invade(self.movingTo)
                        return
                else:
                    return
            else: 
                if len(bestAttackers) > 1:
                    next.standoff = True
                return
            

    def evaluateRetreat(self):
        retiringRegions = [region for region in self.borders if region.retiringInto == self]
        if len(retiringRegions) != 1:
            return
        retiring = retiringRegions[0]
        
        self.occupant = retiring.loser
        self.nextOccupant = self.occupant
        retiring.loser = None
                


class SeasonCycle:
    def __init__(self, startYear, adjustments=True):
        self.year = startYear
        if adjustments==True:
            self.seasons = ("spring", "summer", "autumn", "winter", "adjustments")
        else:
            self.seasons = ("spring", "summer", "autumn", "winter")
        self.seasonIndex = 0

    def next(self):
        self.seasonIndex = (self.seasonIndex + 1) % len(self.seasons)
        if self.seasonIndex == 0:
            self.year += 1
    
    def current(self):
        return self.seasons[self.seasonIndex]
    
    def __str__(self):
        return f"{self.current()} {self.year}"




def evaluateAllMoves():
    for region in Region.regionList:
        region.evaluate()
    for region in Region.regionList:
        region.clearMove()
        region.willMove = False
        if region.nextOccupant == Unit(None):
            region.occupant = Unit(None)
        else:
            region.occupant = region.nextOccupant

def evaluateAllRetreats():
    for region in Region.regionList:
        region.evaluateRetreat()
    for region in Region.regionList:
        region.retiringInto = None
        region.defeatedBy = None
        region.loser = Unit(None)
        region.standoff = False

def countCenters(empire):
    count = 0
    for r in Region.regionList:
        if r.isCenter and (r.occupant.empire == empire or r.controlledBy == empire):
            count += 1
    return count

def countUnits(empire):
    count = 0
    for r in Region.regionList:
        if r.occupant.empire == empire:
            count += 1
    return count

def evaluateAllAdjustments():
    for e in Empire.empireList:
            centers = countCenters(e)
            units = countUnits(e)
            for i in range(units-centers):
                unitsList = [r for r in Region.regionList if r.occupant.empire == e]
                toBeRemoved = random.choice(unitsList)
                unitsList.remove(toBeRemoved)
                toBeRemoved.newUnit(Unit(None))

def evaluateSeason(season):
    if season.current() in ("spring", "autumn"):
        evaluateAllMoves()
    elif season.current() == "summer":
        evaluateAllRetreats()
    elif season.current() == "winter":
        evaluateAllRetreats()
        for r in Region.regionList:
            if r.isCenter and r.occupant.name != None:
                r.controlledBy = r.occupant.empire
    elif season.current() == "adjustments":
        evaluateAllAdjustments()

    season = season.next()


def inputMove(string, season):

    string = string.upper()
    diz = Region.regionDict

    if season in ("spring", "autumn"):
        if re.match("^[A-Z]{3} S [A-Z]{3}$", string): # def support
            regions = string.split(" ")
            reg1 = regions[0]
            reg2 = regions[2]
            
            for i in (reg1, reg2):
                if i not in diz:
                    print("nome regione non valido")
                    return False

            reg1 = diz[reg1]
            reg2 = diz[reg2]

            reg1.addDefSupport(reg2)

        elif re.match("^[A-Z]{3} S [A-Z]{3}-[A-Z]{3}$", string): # atk support
            regions = string.split(" ")
            reg1 = regions[0]
            reg2, reg3 = tuple(regions[2].split("-"))

            for i in (reg1, reg2, reg3):
                if i not in diz:
                    print("nome regione non valido")
                    return False

            reg1 = diz[reg1]
            reg2 = diz[reg2]
            reg3 = diz[reg3]

            reg1.addAtkSupport(reg2, reg3)

        elif re.match("^[A-Z]{3}-[A-Z]{3}$", string): # attack
            regions = string.split("-")
            reg1 = regions[0]
            reg2 = regions[1]

            for i in (reg1, reg2):
                if i not in diz:
                    print("nome regione non valido")
                    return False

            reg1 = diz[reg1]
            reg2 = diz[reg2]

            reg1.attack(reg2)

        elif re.match("^[A-Z]{3} S$", string): # defense
            reg1 = string[0:3]
            if reg1 not in diz:
                print("nome regione non valido")
                return False
            reg1 = diz[reg1]
            reg1.clearMove()

        elif re.match("^[EXIT|Q]$", string):
            exit()
            
        
        else:
            print("format non valido")


    elif season in ("summer", "winter"):
        if re.match("^[A-Z]{3}-[A-Z]{3}$", string):
            regions = string.split("-")
            reg1 = regions[0]
            reg2 = regions[1]

            for i in (reg1, reg2):
                if i not in diz:
                    print("nome regione non valido")
                    return False

            reg1 = diz[reg1]
            reg2 = diz[reg2]

            reg1.retreat(reg2)
            return

        else:
            print("input non valido")
            return False
    
    elif season == "adjustments":
        if re.match("^[A-Z]{3}$", string):
            if string in diz:
                diz[string].buildUnit()
