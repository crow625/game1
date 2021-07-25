#May 16 2021
#game1
'''
Stores all information about the current state of the map.
Also responsible for determining all valid moves.
'''
import game1Units as gu
import game1Map as gm

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
        #self.numUnits = 0
        
        self.addUnit(gu.Warrior("u", (7, 0)))
        self.addUnit(gu.Warrior("u", (7, 7)))
        self.addUnit(gu.Tarantula("e", (0, 7)))
        self.addUnit(gu.Warrior("e", (0, 0)))
                  
        self.terrainCost = {'g': 1, 'w': -1, 'm': 3, 'd': 2, '-': 1}
        
        self.turnCount = 0
        self.userToMove = True
        self.allUnitsMoved = False
        self.moveLog = []
    
    '''
    Adds a unit to the game map.
        unit = unit object
    '''
    def addUnit(self, unit):
        r, c = unit.loc
        self.units.append(unit.image)
        self.gameMap.mapAddUnit(unit, r, c)
        #self.numUnits += 1
        
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
                    
        return moves
    
    '''
    Determines what actions to take based on the player's clicks and the current game state.
    '''
    def clickLogic(self, playerClicks, validMoves):
        if len(playerClicks) == 1:
            unit = gm.mapGetUnit(playerClicks[0][0], playerClicks[0][1])
            #first click was empty, enemy, or already attacked: return empty clicks
            if (unit is None) or (unit.team == "u" and (not self.userToMove)) or (unit.team == "e" and self.userToMove) or (unit.didAttack):
                return ([], False)
            #else keep the click
            return (playerClicks, False)
        #len must be 2 then: it can't be longer
        #same unit: cancel clicks
        if playerClicks[0] == playerClicks[1]:
            return ([], False)
        firstUnit = gm.mapGetUnit(playerClicks[0][0], playerClicks[0][1])
        secondUnit = gm.mapGetUnit(playerClicks[1][0], playerClicks[1][1])
        #clicked another unit
        if not (secondUnit is None):
            #same team, select new unit
            if firstUnit.team == secondUnit.team:
                return ([playerClicks[1]], False)
            #else enemy
            #if adjacent, attack and reset
            if adjUnits(firstUnit, secondUnit):
                self.attack(firstUnit, secondUnit)
            return ([], False)
        #else empty square, check for valid moves
        move = Move(playerClicks[0], playerClicks[1], self.gameMap, 0, None)
        for m in validMoves:
            if m.moveID == move.moveID:
                makeMove(m)
                return ([], True)
        #invalid empty square
        return ([], False)
                
        
    
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
        print("Attacker dealt " + str(attacker_dmg) + " damage")
        #if defender dies, it does not retaliate
        if defender.hpLeft <= 0:
            self.gameMap.mapAddUnit(None, defender.loc[0], defender.loc[1])
            print("Defender defeated")
            return
        
        attacker.hpLeft -= defender_dmg
        print("Defender dealt " + str(defender_dmg) + " damage")
        if attacker.hpLeft <= 0:
            self.gameMap.mapAddUnit(None, attacker.loc[0], defender.loc[1])
            print("Attacker defeated")
            
    '''
    Prints what will happen if the attacker unit attacks the defender unit, and whether one of the units will be defeated.
    '''
    def attackForecast(self, attacker, defender):
        attacker_dmg = attacker.atk - defender.defense
        defender_dmg = defender.atk - attacker.defense
        if attacker_dmg >= defender.hpLeft:
            print("Enemy " + defender.name + " will be defeated")
        else:
            print("Enemy " + defender.name + " will take " + str(attacker_dmg) + " damage")
            if defender_dmg >= attacker.hpLeft:
                print(attacker.name + " will be defeated")
            else:
                print(attacker.name + " will take " + str(defender_dmg) + " damage")
            
    '''
    Determines if a player has won yet.
    Returns True if a player has won, False otherwise.
    '''
    def victoryCheck(self):
        playerCount = self.gameMap.numUnits["u"]
        enemyCount = self.gameMap.numUnits["e"]
        if enemyCount == 0:
            if playerCount == 0:
                print("Stalemate")
                return True
            else:
                print("Player wins!")
                return True
        elif playerCount == 0:
            print("Enemy wins!")
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

'''
Prints a unit's remaining HP and moves when moused over.
Only prints HP for enemy units.
'''
def mouseover(unit, toMove):
    if (toMove and unit.team == 'u') or ((not toMove) and unit.team == 'e'):
        print(unit.name + " has " + str(unit.hpLeft) + " HP left and " + str(unit.movesLeft) + " moves left")
    else:
        print("Enemy " + unit.name + " has " + str(unit.hpLeft) + " HP left")
    return unit.loc
    
        
        
class Move():
    def __init__(self, startSq, endSq, gameMap, cost, path):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.unitMoved = gameMap.mapGetUnit(self.startRow, self.startCol)
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow *10 + self.endCol
        self.cost = cost
        self.path = path
    
    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        else:
            return False
                