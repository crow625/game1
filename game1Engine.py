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
        
        self.gameMap.mapAddUnit(gu.Warrior("u"), 7, 0)
        self.gameMap.mapAddUnit(gu.Warrior("u"), 7, 7)
        self.gameMap.mapAddUnit(gu.Warrior("e"), 0, 7)
            
        self.units = [
            ["--", "--", "--", "--", "--", "--", "--", gu.Warrior("e")],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            [gu.Warrior("u"), "--", "--", "--", "--", "--", "--", "--"]]
        
        
        self.terrainCost = {'g': 1, 'w': -1, 'm': 3, 'd': 2, '-': 1}
        
        self.turnCount = 0
        self.userToMove = True
        self.numUnits = 1
        self.allUnitsMoved = False
        self.moveLog = []
        
    def makeMove(self, move):
        self.gameMap.mapAddUnit(None, move.startRow, move.startCol) #unit leaves the original square
        self.gameMap.mapAddUnit(move.unitMoved, move.endRow, move.endCol) #and moves to new square
        self.moveLog.append(move) #logs the move
        move.unitMoved.movesLeft -= move.cost
        
    def getValidMoves(self):
        return self.getAllPossibleMoves()
        
    def getAllPossibleMoves(self):
        moves = []
        for r in range(self.gameMap.getYdim()):
            for c in range(self.gameMap.getXdim()):
                if self.gameMap.mapGetUnit(r, c) is None:
                    turn = "-"
                else :
                    turn = self.gameMap.mapGetUnit(r, c).team
                if (turn == 'u' and self.userToMove) or (turn == 'e' and not self.userToMove):
                    unit = self.gameMap.mapGetUnit(r, c) #unit on square
                    moves = gu.getMoves(r, c, moves, self)
                    
        return moves
        
        
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
                