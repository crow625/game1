#May 16 2021
#game1
'''
Stores all information about the current state of the map.
Also responsible for determining all valid moves.
'''
import game1Units as gu

class GameState():
    def __init__(self): #what executes on startup
        '''
        'g' = grass
        'w' = water
        'm' = mountain
        'd' = desert
        '-' = empty
        '''
        self.gameMap = [
            ['m','m','w','m','g','g','g','g'],
            ['g','m','w','g','g','g','g','g'],
            ['g','g','w','w','g','g','g','g'],
            ['g','g','g','w','w','w','g','g'],
            ['g','g','g','g','g','w','w','w'],
            ['g','g','g','g','g','g','g','g'],
            ['g','g','g','g','g','g','d','d'],
            ['g','g','g','g','g','d','d','d']]
            
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
        
        
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--" #unit leaves the original square
        self.board[move.endRow][move.endCol] = move.unitMoved #and moves to new square
        self.moveLog.append(move) #logs the move
        self.userToMove = not self.userToMove #swap players
        
    def getValidMoves(self):
        return self.getAllPossibleMoves()
        
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.units)):
            for c in range(len(self.units[r])):
                if self.units[r][c] == "--":
                    turn = "-"
                else :
                    turn = self.units[r][c].team
                if (turn == 'u' and self.userToMove) or (turn == 'e' and not self.userToMove):
                    unit = self.units[r][c] #unit on square
                    unit.getMoves(r, c, moves, self, unit.movesLeft)
                    
        return moves
        
    
        
        
            
        
        
        
class Move():
    def __init__(self, startSq, endSq, units, cost):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.unitMoved = units[self.startRow][self.startCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow *10 + self.endCol
        self.cost = cost
    
    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
                