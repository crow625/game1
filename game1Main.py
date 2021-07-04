#May 16 2021
#game1
'''
Responsible for handling user input and displaying the current game state.
'''

import sys
import pygame as p
import game1Engine

p.init()

WIDTH = HEIGHT = 768
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}
COLORS = {'g': p.Color("green"), 'w': p.Color("royal blue"),
          'm': p.Color("gray"), 'd': p.Color("yellow"),
          '-': p.Color("white")}
BORDER_COLORS = {'g': p.Color("dark green"), 'w': p.Color("blue"),
                 'm': p.Color("dim gray"), 'd': p.Color("goldenrod"),
                 '-': p.Color("white")}
BORDER_WIDTH = 2
if len(sys.argv) > 1:
    mapname = sys.argv[1]
else:
    mapname = "map1.txt"

'''
Load images
'''
def loadImages(dims):
    units = ["uW", "eW"]
    for unit in units:
        IMAGES[unit] = p.transform.scale(p.image.load("./images/" + unit + ".png"), (dims[2], dims[3]))
        
        
'''
The main driver for code.
'''
def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = game1Engine.GameState(mapname)
    YDIMENSION = gs.gameMap.getYdim()
    XDIMENSION = gs.gameMap.getXdim()
    SQ_X = WIDTH//XDIMENSION
    SQ_Y = HEIGHT//YDIMENSION
    DIMENSIONS = (XDIMENSION, YDIMENSION, SQ_X, SQ_Y)
    
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages(DIMENSIONS)
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.KEYDOWN:
                if e.key == p.K_RETURN: #enter ends turn
                    gs.userToMove = not gs.userToMove
                    for r in gs.gameMap.getMap():
                        for t in r:
                            unit = t.getUnit()
                            if unit is None:
                                continue
                            elif (unit.team == 'u' and gs.userToMove) or (unit.team == 'e' and not gs.userToMove):
                                unit.movesLeft = unit.maxMoves
                                
                    validMoves = gs.getValidMoves()
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_X
                row = location[1]//SQ_Y
                #sqSelected is always the most recent location
                sqSelected = (row, col)
                playerClicks.append(sqSelected)
                
                if len(playerClicks) == 1:
                    print("1 click")
                    firstUnit = gs.gameMap.getTile(playerClicks[0][0], playerClicks[0][1]).getUnit()
                    #first click was empty: toss
                    if firstUnit is None:
                        print("empty toss")
                        sqSelected = ()
                        playerClicks = []
                    #first click was wrong team: toss
                    elif (firstUnit.team == "u" and (not gs.userToMove)) or (firstUnit.team == "e" and gs.userToMove):
                        print("enemy toss")
                        sqSelected = ()
                        playerClicks = []
                    #unit with no moves: toss
                    elif firstUnit.movesLeft <= 0:
                        print("no moves left toss")
                        sqSelected = ()
                        playerClicks = []
                        
                    
                #will only get here if first click was valid unit with moves
                elif len(playerClicks) == 2:
                    print("2 click")
                    firstUnit = gs.gameMap.getTile(playerClicks[0][0], playerClicks[0][1]).getUnit()
                    secondUnit = gs.gameMap.getTile(playerClicks[1][0], playerClicks[1][1]).getUnit()
                    
                    #clicked same unit twice: toss last click
                    if playerClicks[1] == playerClicks[0]:
                        print("same unit")
                        playerClicks.pop()
                    
                    #clicked on another unit
                    elif not (secondUnit is None):
                        #enemy unit: toss last click
                        if firstUnit.team != secondUnit.team:
                            print("enemy unit")
                            sqSelected = ()
                            playerClicks.pop()
                        #else team unit: make last click first click
                        else:
                            print("other team unit")
                            playerClicks[0] = playerClicks[1]
                            playerClicks.pop()
                    #clicked empty square
                    else:
                        print("clicked empty square")
                        move = game1Engine.Move(playerClicks[0], playerClicks[1], gs.gameMap, 0, None)
                        for m in validMoves:
                            if m.moveID == move.moveID:
                                print("valid move")
                                gs.makeMove(m)
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                                break
                        if moveMade:
                            sqSelected = ()
                            playerClicks = []
                        else:
                            print("invalid move")
                            sqSelected = ()
                            playerClicks.pop()
                        
                            
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            #animateMove(screen, gs.gameMap, DIMENSIONS, m)
            #restore moves at turn rollover
            '''
            for unit in gs.units:
                if unit == "--":
                    continue
                elif (unit.team == 'u' and gs.userToMove) or (unit.team == 'e' and (not gs.userToMove)):
                    unit.movesLeft = unit.maxMoves
            '''
                    
        drawGameState(screen, gs.gameMap, DIMENSIONS, sqSelected, validMoves)
        clock.tick(MAX_FPS)
        p.display.flip()
        
def drawGameState(screen, gameMap, dims, sqSelected, validMoves):
    drawMap(screen, gameMap, dims)
    drawUnits(screen, gameMap, dims)
    highlightSquares(screen, gameMap, dims, sqSelected, validMoves)
    
    
def drawMap(screen, gameMap, dims):
    XDIMENSION = dims[0]
    YDIMENSION = dims[1]
    SQ_X = dims[2]
    SQ_Y = dims[3]
    for r in range(YDIMENSION):
        for c in range(XDIMENSION):
            t = gameMap.getTile(r, c)
            terrain = t.getTerrain()
            color = COLORS[terrain]
            border_color = BORDER_COLORS[terrain]
            p.draw.rect(screen,border_color, p.Rect(c*SQ_X, r*SQ_Y, SQ_X, SQ_Y))
            p.draw.rect(screen,color, p.Rect(c*SQ_X + BORDER_WIDTH, r*SQ_Y + BORDER_WIDTH, SQ_X - 2*BORDER_WIDTH, SQ_Y - 2*BORDER_WIDTH))

            
def drawUnits(screen, gameMap, dims):
    XDIMENSION = dims[0]
    YDIMENSION = dims[1]
    SQ_X = dims[2]
    SQ_Y = dims[3]
    for r in range(YDIMENSION):
        for c in range(XDIMENSION):
            unit = gameMap.getTile(r, c).getUnit()
            if not (unit is None):
                screen.blit(IMAGES[unit.image], p.Rect(c*SQ_X, r*SQ_Y, SQ_X, SQ_Y))
                
def animateMove(screen, gameMap, dims, move):
    for i in range(len(move.path)-1):
        gameMap.mapAddUnit(None, move.path[i].getCoords()[0], move.path[i].getCoords()[1])
        gameMap.mapAddUnit(move.unitMoved, move.path[i+1].getCoords()[0], move.path[i+1].getCoords()[1])
        drawGameState(screen, gameMap, dims)
        p.time.delay(10)
        p.display.flip()
        
def highlightSquares(screen, gameMap, dims, sqSelected, validMoves):
    if sqSelected != ():
        XDIMENSION = dims[0]
        YDIMENSION = dims[1]
        SQ_X = dims[2]
        SQ_Y = dims[3]
        r, c = sqSelected
        s = p.Surface((SQ_X, SQ_Y))
        s.set_alpha(100)
        s.fill(p.Color("white"))
        screen.blit(s, (c*SQ_X, r*SQ_Y))
        
        for move in validMoves:
            if move.startRow == r and move.startCol == c:
                p.draw.circle(screen, (50, 50, 50, 100), ((move.endCol + 0.5)*SQ_X , (move.endRow + 0.5)*SQ_Y), SQ_X/6)
                p.draw.circle(screen, (240, 240, 240, 100), ((move.endCol + 0.5)*SQ_X , (move.endRow + 0.5)*SQ_Y), SQ_X/8)
        p.display.flip()
    
    
if __name__ == "__main__":
    main()
    