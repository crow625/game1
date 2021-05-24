#May 19 2021
#game1
'''
Defines unit objects and their attributes
'''

import game1Engine as ge

class Warrior():
    def __init__(self, team):
        self.maxMoves = 4
        self.moveCost = {'g': 1, 'd': 2, 'm': 3, 'w': -1}
        self.movesLeft = self.maxMoves
        self.team = team
        self.name = 'W'
        self.image = team + name
            
    def getMoves(self, r, c, moves, gs, n):
        directions = ((0, -1), (-1, 0), (0, 1), (1, 0))
        if n <= 0:
            return
        for d in directions: #move one square at a time
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8: #if on board
                cost = self.moveCost[gs.gameMap[endRow][endCol]]
                #can only move there if there is no unit and the cost is legal
                if gs.units[endRow][endCol] == "--" and cost >= 0:
                    new_move = ge.Move((r,c), (endRow,endCol), gs.units, cost)
                    print("Found move: " + str(endCol) + "," + str(endRow) + " for cost " + str(self.maxMoves - n +cost))
                    if len(moves) == 0:
                        moves.append(new_move)
                    for m in moves:
                        #cheaper route: change cost
                        if new_move == m and new_move.cost < m.cost:
                            print("cheaper alternative")
                            m.cost = new_move.cost
                        #not cheaper: ignore
                        elif new_move == m:
                            print("not cheaper route")
                            continue
                        #different move: append
                        else:
                            moves.append(new_move)
                    #recursive call
                    
                    self.getMoves(endRow, endCol, moves, gs, (n - cost))