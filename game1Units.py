#May 19 2021
#game1
'''
Defines unit objects and their attributes
'''

import game1Engine as ge
import game1Map as gm

'''
Returns a list of every possible move for the unit on the given tile.
    r, c: Integers that indicate coordinates.
    moves: List of all valid moves starting at (r, c).
    gs: The current game state.
'''
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
            if pathLength >= 0 and (gs.gameMap.mapGetUnit(endRow, endCol) is None or r, c == endRow, endCol):
                path = sp.shortestPath(gs.gameMap.getTile(endRow, endCol))
                new_move = ge.Move((r, c), (endRow, endCol), gs.gameMap, pathLength, path)
                moves.append(new_move)
    return moves

'''
Assigns a unit's stats based on its type.
If the unit file cannot be found creates a default unit.
    unit (Unit) = the unit to assign stats to
    filename (string) = where the stats are determined
'''
def readStats(unit, filename):
    try:
        file = open("stats/" + filename + ".txt", 'r')
        file = file.read().split('\n')
        unit.name = file[0]
        unit.maxMoves = int(file[1])
        moveCosts = file[2].split(',')
        unit.moveCost['g'] = int(moveCosts[0].strip())
        unit.moveCost['d'] = int(moveCosts[1].strip())
        unit.moveCost['m'] = int(moveCosts[2].strip())
        unit.moveCost['w'] = int(moveCosts[3].strip())
        unit.maxHP = int(file[3])
        unit.atk = int(file[4])
        unit.defense = int(file[5])
    except:
        unit.name = "Unit"
        unit.maxMoves = 1
        unit.moveCost['g'] = 1
        unit.moveCost['d'] = 1
        unit.moveCost['m'] = 1
        unit.moveCost['w'] = 1
        unit.maxHP = 1
        unit.atk = 1
        unit.defense = 1

'''
A generic unit class. Its stats are drawn from a file in the stats folder.
    name (String) = the unit's type. Determines what file its stats are drawn from.
    team (char) = which team the unit is on ('u' or 'e')
    loc (tuple) = coordinates where the unit will be placed
'''
class Unit():
    def __init__(self, name, team):
        self.moveCost = {}
        self.team = team
        self.loc = (-1, -1)
        readStats(self, name)
        self.image = self.team + self.name
        self.movesLeft = self.maxMoves
        self.hpLeft = self.maxHP
        self.didAttack = False
    