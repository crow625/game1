#May 19 2021
#game1
'''
Defines unit objects and their attributes
'''

import game1Engine as ge
import game1Map as gm

#Returns a list of every possible move for the unit on the given tile
def getMoves(r, c, moves, gs):
    u = gs.gameMap.mapGetUnit(r, c)
    sp = gm.ShortestPaths()
    sp.compute(gs.gameMap.getTile(r, c), u)
    for i in gs.gameMap.getMap(): #i = row
        for j in i: #j = tile
            #iterate through every tile, if distance is valid add a move
            endRow = j.getCoords()[0]
            endCol = j.getCoords()[1]
            pathLength = sp.shortestPathLength(j)
            if pathLength >= 0 and gs.gameMap.mapGetUnit(endRow, endCol) is None:
                path = sp.shortestPath(gs.gameMap.getTile(endRow, endCol))
                new_move = ge.Move((r, c), (endRow, endCol), gs.gameMap, pathLength, path)
                moves.append(new_move)
    return moves

class Warrior():
    def __init__(self, team):
        self.maxMoves = 4
        self.moveCost = {'g': 1, 'd': 2, 'm': 3, 'w': -1}
        self.movesLeft = self.maxMoves
        self.team = team
        self.name = 'W'
        self.image = self.team + self.name
        
    '''        
    def getMoves(self, r, c, moves, gs):
        sp = gm.ShortestPaths()
        sp.compute(gs.gameMap.getTile(r, c), self)
        for i in gs.gameMap.getMap():
            for j in i:
                #iterate through every tile, if distance is valid add a move
                endRow = j.getCoords()[0]
                endCol = j.getCoords()[1]
                pathLength = sp.shortestPathLength(j)
                if pathLength >= 0 and gs.units[endRow][endCol] == "--":
                    new_move = ge.Move((r, c), (endRow, endCol), gs.units, pathLength)
    '''