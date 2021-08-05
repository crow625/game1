#May 16 2021
#game1
'''
Stores all information about the current state of the map.
Also responsible for determining all valid moves.
'''
import game1Units as gu
import game1Map as gm
from os import listdir

class GameState():
    def __init__(self, mapname): #what executes on startup
        '''
        'g' = grass
        'w' = water
        'm' = mountain
        'd' = desert
        '-' = empty
        '''
        self.gameMap = gm.MapArray(mapname)
        
        self.units = []
        self.allUnits = []
        unitFiles = listdir("./stats")
        unitFiles.remove("Example.txt")
        for file in unitFiles:
            self.allUnits.append('u' + file[0:-4])
            self.allUnits.append('e' + file[0:-4])
        self.allUnits.sort()
        #self.numUnits = 0
        
        self.addUnit(gu.Unit("Warrior", 'u', (3, 0)))
        self.addUnit(gu.Unit("Warrior", 'u', (3, 3)))
        self.addUnit(gu.Unit("Tarantula", 'e', (0, 3)))
        self.addUnit(gu.Unit("Warrior", 'e', (0, 0)))
                  
        self.terrainCost = {'g': 1, 'w': -1, 'm': 3, 'd': 2, '-': 1}
        
        self.turnCount = 0
        self.userToMove = True
        self.allUnitsMoved = False
        self.moveLog = []
        self.TEXT = {}
        
        self.delayTime = 16
        self.prevMouseover = ()
        self.activeMouseover = ()
        self.mouseoverDelay = {}
        self.didMouseover = ()
        
        self.prevForecast = ()
        self.activeForecast = ()
        self.forecastDelay = {}
        self.didForecast = ()
        
        
    '''
    Loads the game's text.
        filename = string location of game text file
    '''
    def loadText(self, filename):
        file = open(filename, 'r')
        for line in file:
            if '#' in line:
                continue
            line = line.strip('\n')
            key = line.split('=')
            self.TEXT[key[0]] = key[1]
    
    '''
    Adds a unit to the game map.
        unit = unit object
    '''
    def addUnit(self, unit):
        r, c = unit.loc
        try:
            self.gameMap.mapAddUnit(unit, r, c)
            self.units.append(unit.image)
        #self.numUnits += 1
        except:
            print("Could not add {} at {}, {}, coordinates out of bounds.".format(unit.name, r, c))
        
    '''
    Moves a unit from one location to another.
    Consumes unit's movement accordingly.
        move = move object
    '''
    def makeMove(self, move):
        self.gameMap.mapAddUnit(None, move.startRow, move.startCol) #unit leaves the original square
        self.gameMap.mapAddUnit(move.unitMoved, move.endRow, move.endCol) #and moves to new square
        self.moveLog.append(move) #logs the move
        move.unitMoved.movesLeft -= move.cost
    
    '''
    Returns a list of all moves a player can make within the ruleset.
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()
        
    '''
    Returns a list of all moves a player can make.
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(self.gameMap.getYdim()):
            for c in range(self.gameMap.getXdim()):
                if self.gameMap.mapGetUnit(r, c) is None:
                    turn = "-"
                else :
                    turn = self.gameMap.mapGetUnit(r, c).team
                if (turn == 'u' and self.userToMove) or (turn == 'e' and not self.userToMove):
                    moves = gu.getMoves(r, c, moves, self)
        self.getValidAttacks(moves)            
        return moves
    
    '''
    Appends coordinates to a move's attacks field if there is an enemy within range.
    '''
    def getValidAttacks(self, moves):
        #adds tuple coordinates to move's attacks array field
        for m in moves:
            for d in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                adj = (m.endRow + d[0], m.endCol + d[1])
                if (adj[0] < 0 or adj[0] >= self.gameMap.getYdim()) or (adj[1] < 0 or adj[1] >= self.gameMap.getXdim()):
                    continue
                target = self.gameMap.mapGetUnit(adj[0], adj[1])
                if (target is None) or (m.unitMoved.team == target.team):
                    continue
                m.attacks.append((adj[0], adj[1]))
                
    '''
    Determines what actions to take based on the player's clicks and the current game state.
        playerClicks = array of tuples that indicate coordinates the player has clicked (row, col)
        validMoves = array of Move objects that the player can make in the current gamestate
    '''
    def clickLogic(self, playerClicks, validMoves):
        if len(playerClicks) == 1:
            unit = self.gameMap.mapGetUnit(playerClicks[0][0], playerClicks[0][1])
            #first click was empty, enemy, or already attacked: return empty clicks
            if (unit is None) or (unit.team == "u" and (not self.userToMove)) or (unit.team == "e" and self.userToMove) or (unit.didAttack):
                return ([], False)
            #else keep the click
            return (playerClicks, False)
        #len must be 2 then: it can't be longer
        #same unit: cancel clicks
        if playerClicks[0] == playerClicks[1]:
            return ([], True)
        firstUnit = self.gameMap.mapGetUnit(playerClicks[0][0], playerClicks[0][1])
        secondUnit = self.gameMap.mapGetUnit(playerClicks[1][0], playerClicks[1][1])
        #clicked another unit
        if not (secondUnit is None):
            #same team, select new unit
            if firstUnit.team == secondUnit.team:
                return ([playerClicks[1]], False)
            #else enemy
            #if adjacent, attack and reset, else toss clicks
            if adjUnits(firstUnit, secondUnit):
                self.attack(firstUnit, secondUnit)
                return ([], True)
            '''
            #fast attack: works but does not take most direct route. Should display forecast of route taken or follow the path of mouse.
            else:
                for m in validMoves:
                    if (playerClicks[1][0], playerClicks[1][1]) in m.attacks:
                        self.makeMove(m)
                        self.attack(firstUnit, secondUnit)
                        return ([], True)
            '''    
            return ([], False)
        #else empty square, check for valid moves
        move = Move(playerClicks[0], playerClicks[1], self.gameMap, 0, None)
        for m in validMoves:
            if m.moveID == move.moveID:
                self.makeMove(m)
                return ([], True)
        #invalid empty square
        return ([], False)
                
    '''
    Restores the moves left and attack readiness for all units of the team whose turn is next.
    Triggers at the end of a turn.
    '''
    def refreshMoves(self):
        self.userToMove = not self.userToMove
        for row in self.gameMap.getMap():
            for tile in row:
                unit = tile.getUnit()
                if unit is None:
                    continue
                elif (unit.team == 'u' and self.userToMove) or (unit.team == 'e' and not self.userToMove):
                    unit.movesLeft = unit.maxMoves
                    unit.didAttack = False
    
    '''
    Keeps track of how long one tile has been moused over.
    Prints the mouseover info for the unit on that tile
    once it has been moused over for the required time.
        pos = tuple of coordinates (row, col)
    '''
    def mouseoverLogic(self, pos):
        if pos[1] >= self.gameMap.getXdim():
            return
        self.prevMouseover = self.activeMouseover
        self.activeMouseover = pos
        self.mouseoverDelay.setdefault(pos, 0)
        if self.prevMouseover == pos:
            self.mouseoverDelay[pos] = self.mouseoverDelay.get(pos) + 1
        else:
            self.mouseoverDelay[self.prevMouseover] = 0
        if self.mouseoverDelay.get(pos) == self.delayTime:
            self.mouseoverDelay[pos] = 0
            if not (self.gameMap.mapGetUnit(pos[0], pos[1]) is None or self.didMouseover == pos):
                self.mouseover(self.gameMap.mapGetUnit(pos[0], pos[1]))
                self.didMouseover = pos
          
    '''
    Keeps track of how long one tile has been moused over while a unit has been selected.
    Prints the attack forecast between the selected unit and the unit moused over
    once the mouseover time has been reached.
        pos = tuple of coordinates (row, col)
        playerClicks = array of tuples that indicate coordinates the player has clicked (row, col)
    '''
    def forecastLogic(self, pos, playerClicks):
        if pos[1] >= self.gameMap.getXdim():
            return
        if len(playerClicks) == 0:
            return
        unit1 = self.gameMap.mapGetUnit(playerClicks[0][0], playerClicks[0][1])
        unit2 = self.gameMap.mapGetUnit(pos[0], pos[1])
        if (unit2 is None) or unit1.team == unit2.team:
            return
        self.prevForecast = self.activeForecast
        self.activeForecast = pos
        self.forecastDelay.setdefault(pos, 0)
        if self.prevForecast == pos:
            self.forecastDelay[pos] = self.forecastDelay.get(pos) + 1
        else:
            self.forecastDelay[self.prevForecast] = 0
        if self.forecastDelay.get(pos) == self.delayTime:
            self.forecastDelay[pos] = 0
            if self.didForecast != (unit1.loc, pos):
                self.attackForecast(unit1, unit2)
                self.didForecast = (unit1.loc, pos)
                
    '''
    Prints a unit's remaining HP and moves when moused over.
    Only prints HP for enemy units.
        unit = unit object of any team
    '''
    def mouseover(self, unit):
        if (self.userToMove and unit.team == 'u') or ((not self.userToMove) and unit.team == 'e'):
            if unit.didAttack:
                print(self.TEXT.get("TXT_USER_NO_ATTACK").format(unit.name, unit.hpLeft, unit.movesLeft))
            else:
                print(self.TEXT.get("TXT_USER_HAS_ATTACK").format(unit.name, unit.hpLeft, unit.movesLeft))
        else:
            print(self.TEXT.get("TXT_ENEMY_PREVIEW").format(unit.name, unit.hpLeft))
        return unit.loc
                
        
    '''
    Initiates an attack between two units.
    Fire Emblem-style combat: Attacker hits first, then defender retaliates.
    Damage dealt = attack - defense
    Attacking consumes all movement.
        attacker = unit object who initiates attack
        defender = unit object who retaliates
    '''
    def attack(self, attacker, defender):
        attacker_dmg = attacker.atk - defender.defense
        defender_dmg = defender.atk - attacker.defense
        #attacking consumes all movement
        attacker.movesLeft = 0
        attacker.didAttack = True
    
        defender.hpLeft -= attacker_dmg
        print(self.TEXT.get("TXT_USER_ATTACK").format(attacker.name, attacker_dmg))
        #if defender dies, it does not retaliate
        if defender.hpLeft <= 0:
            self.gameMap.mapAddUnit(None, defender.loc[0], defender.loc[1])
            print(self.TEXT.get("TXT_ENEMY_SLAIN").format(defender.name))
            return
        
        attacker.hpLeft -= defender_dmg
        print(self.TEXT.get("TXT_ENEMY_ATTACK").format(defender.name, defender_dmg))
        if attacker.hpLeft <= 0:
            self.gameMap.mapAddUnit(None, attacker.loc[0], defender.loc[1])
            print(self.TEXT.get("TXT_USER_SLAIN").format(attacker.name))
            
    '''
    Prints what will happen if the attacker unit attacks the defender unit, and whether one of the units will be defeated.
        attacker = unit object who initiates attack
        defender = unit object who retaliates
    '''
    def attackForecast(self, attacker, defender):
        attacker_dmg = attacker.atk - defender.defense
        defender_dmg = defender.atk - attacker.defense
        if attacker_dmg >= defender.hpLeft:
            print(self.TEXT.get("TXT_FC_ENEMY_SLAIN").format(defender.name))
        else:
            print(self.TEXT.get("TXT_FC_ENEMY_TAKES").format(defender.name, attacker_dmg))
            if defender_dmg >= attacker.hpLeft:
                print(self.TEXT.get("TXT_FC_USER_SLAIN").format(attacker.name))
            else:
                print(self.TEXT.get("TXT_FC_USER_TAKES").format(attacker.name, defender_dmg))
            
    '''
    Determines if a player has won yet.
    Returns True if a player has won, False otherwise.
    '''
    def victoryCheck(self):
        playerCount = self.gameMap.numUnits["u"]
        enemyCount = self.gameMap.numUnits["e"]
        if enemyCount == 0:
            if playerCount == 0:
                print(self.TEXT.get("TXT_STALEMATE"))
                return True
            else:
                print(self.TEXT.get("TXT_USER_WIN"))
                return True
        elif playerCount == 0:
            print(self.TEXT.get("TXT_ENEMY_WIN"))
            return True
        return False
    
'''
Determines if two units are adjacent.
    u1: unit object
    u2: unit object
'''
def adjUnits(u1, u2):
    (r, c) = u1.loc[0] - u2.loc[0], u1.loc[1] - u2.loc[1]
    if (r, c) in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        return True
    return False      
        
class Move():
    def __init__(self, startSq, endSq, gameMap, cost, path):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.unitMoved = gameMap.mapGetUnit(self.startRow, self.startCol)
        self.moveID = (self.startRow, self.startCol, self.endRow, self.endCol)
        self.cost = cost
        self.path = path
        self.attacks = []
    
    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        else:
            return False
                