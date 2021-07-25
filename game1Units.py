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
            if pathLength >= 0 and gs.gameMap.mapGetUnit(endRow, endCol) is None:
                path = sp.shortestPath(gs.gameMap.getTile(endRow, endCol))
                new_move = ge.Move((r, c), (endRow, endCol), gs.gameMap, pathLength, path)
                moves.append(new_move)
    return moves

def attack(attacker, defender, gs):
    #Fire Emblem style combat. Attacker hits first, then defender retaliates.
    attacker_dmg = attacker.atk - defender.defense
    defender_dmg = defender.atk - attacker.defense
    
    defender.hpLeft -= attacker_dmg
    #if defender dies, it does not retaliate
    if defender.hpLeft <= 0:
        gs.gameMap.mapAddUnit(None, defender.loc[0], defender.loc[1])
        print("Defender defeated")
        return
    attacker.hpLeft -= defender_dmg
    if attacker.hpLeft <= 0:
        gs.gameMap.mapAddUnit(None, attacker.loc[0], defender.loc[1])

class Warrior():
    def __init__(self, team, loc):
        self.maxMoves = 4
        self.moveCost = {'g': 1, 'd': 2, 'm': 3, 'w': -1}
        self.movesLeft = self.maxMoves
        self.team = team
        self.name = 'W'
        self.image = self.team + self.name
        self.loc = loc
        
        self.didAttack = False
        self.maxHP = 20
        self.hpLeft = self.maxHP
        self.atk = 10
        self.defense = 5
        
class Tarantula():
    def __init__(self, team, loc):
        self.maxMoves = 3
        self.moveCost = {'g': 2, 'd': 1, 'm': 2, 'w': -1}
        self.movesLeft = self.maxMoves
        self.team = team
        self.name = "Tarantula"
        self.image = self.team + self.name
        self.loc = loc
        
        self.didAttack = False
        self.maxHP = 25
        self.hpLeft = self.maxHP
        self.atk = 12
        self.defense = 8