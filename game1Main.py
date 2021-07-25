#May 16 2021
#game1
'''
Responsible for handling user input and displaying the current game state.
'''

import sys
import pygame as p
import game1Engine as ge

p.init()

HEIGHT = 768
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
Load images for units in the game.
'''
def loadImages(SQ_SIZE, units):
    for unit in units:
        IMAGES[unit] = p.transform.scale(p.image.load("./images/" + unit + ".png"), (SQ_SIZE - 20, SQ_SIZE - 20))
        
        
'''
The main driver for code.
'''
def main():
    gs = ge.GameState(mapname)
    YDIMENSION = gs.gameMap.getYdim()
    XDIMENSION = gs.gameMap.getXdim()
    SQ_SIZE = HEIGHT//YDIMENSION
    WIDTH = SQ_SIZE*XDIMENSION
    DIMENSIONS = (XDIMENSION, YDIMENSION, SQ_SIZE)
    
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages(SQ_SIZE, gs.units)
    running = True
    sqSelected = ()
    playerClicks = []
    didForecast = ()
    didMouseover = ()
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                
            location = p.mouse.get_pos()
            col = location[0]//SQ_SIZE
            row = location[1]//SQ_SIZE
            #displays a unit's HP and moves left when moused over
            if not (gs.gameMap.mapGetUnit(row, col) is None or didMouseover == (row, col)):
                didMouseover = ge.mouseover(gs.gameMap.mapGetUnit(row, col), gs.userToMove)
            #prints a combat forecast if a unit is selected and hovers over an enemy unit                
            if len(playerClicks) == 1 and didForecast != (row, col) and (not (gs.gameMap.mapGetUnit(row, col) is None)) and (gs.gameMap.mapGetUnit(sqSelected[0], sqSelected[1]).team != gs.gameMap.mapGetUnit(row, col).team):
                gs.attackForecast(gs.gameMap.mapGetUnit(sqSelected[0], sqSelected[1]), gs.gameMap.mapGetUnit(row, col))
                didForecast = (row, col)
            if e.type == p.KEYDOWN:
                if e.key == p.K_RETURN: #enter ends turn
                    sqSelected = ()
                    playerClicks = []
                    gs.userToMove = not gs.userToMove
                    for r in gs.gameMap.getMap():
                        for t in r:
                            unit = t.getUnit()
                            if unit is None:
                                continue
                            elif (unit.team == 'u' and gs.userToMove) or (unit.team == 'e' and not gs.userToMove):
                                unit.movesLeft = unit.maxMoves
                                unit.didAttack = False
                    validMoves = gs.getValidMoves()
                    
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
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
                    '''
                    elif firstUnit.movesLeft <= 0:
                        print("no moves left toss")
                        sqSelected = ()
                        playerClicks = []
                        '''
                    
                #will only get here if first click was valid unit with moves
                elif len(playerClicks) == 2:
                    print("2 click")
                    firstUnit = gs.gameMap.getTile(playerClicks[0][0], playerClicks[0][1]).getUnit()
                    secondUnit = gs.gameMap.getTile(playerClicks[1][0], playerClicks[1][1]).getUnit()
                    
                    #clicked same unit twice: toss both clicks
                    if playerClicks[1] == playerClicks[0]:
                        print("same unit")
                        sqSelected = ()
                        playerClicks = []
                    
                    #clicked on another unit
                    elif not (secondUnit is None):
                        #enemy unit: initiate attack if adjacent
                        # toss if not adjacent
                        if firstUnit.team != secondUnit.team:
                            if ge.adjUnits(firstUnit, secondUnit) and not firstUnit.didAttack:
                                print("adjacent enemy unit")
                                gs.attack(firstUnit, secondUnit)
                                firstUnit.didAttack = True
                                moveMade = True
                            else:
                                print("too far or already attacked")
                            sqSelected = ()
                            playerClicks = []
                        #else team unit: make last click first click
                        else:
                            print("other team unit")
                            playerClicks[0] = playerClicks[1]
                            playerClicks.pop()
                    #clicked empty square
                    else:
                        print("clicked empty square")
                        move = ge.Move(playerClicks[0], playerClicks[1], gs.gameMap, 0, None)
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
                    
        gameOver = gs.victoryCheck()
        if gameOver:
            running = False
        drawGameState(screen, gs.gameMap, DIMENSIONS, sqSelected, validMoves)
        clock.tick(MAX_FPS)
        p.display.flip()
        
'''
Draws everything about the current state of the game.
    screen = Where the game is displayed
    gameMap = a map array object that describes the game state
    dims = a tuple that indicates the game dimensions
    sqSelected = a tuple of coordinates the player last clicked on
    validMoves = a list of moves the player can make
'''
def drawGameState(screen, gameMap, dims, sqSelected, validMoves):
    drawMap(screen, gameMap, dims)
    drawUnits(screen, gameMap, dims)
    highlightSquares(screen, gameMap, dims, sqSelected, validMoves)
    
'''
Draws the map terrain.
    screen = Where the game is displayed
    gameMap = a map array object that describes the game state
    dims = a tuple that indicates the game dimensions
'''
def drawMap(screen, gameMap, dims):
    XDIMENSION = dims[0]
    YDIMENSION = dims[1]
    SQ_SIZE = dims[2]
    for r in range(YDIMENSION):
        for c in range(XDIMENSION):
            t = gameMap.getTile(r, c)
            terrain = t.getTerrain()
            color = COLORS[terrain]
            border_color = BORDER_COLORS[terrain]
            p.draw.rect(screen,border_color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            p.draw.rect(screen,color, p.Rect(c*SQ_SIZE + BORDER_WIDTH, r*SQ_SIZE + BORDER_WIDTH, SQ_SIZE - 2*BORDER_WIDTH, SQ_SIZE - 2*BORDER_WIDTH))

'''
Draws all units on the map.
    screen = Where the game is displayed
    gameMap = a map array object that describes the game state
    dims = a tuple that indicates the game dimensions
'''
def drawUnits(screen, gameMap, dims):
    XDIMENSION = dims[0]
    YDIMENSION = dims[1]
    SQ_SIZE = dims[2]
    for r in range(YDIMENSION):
        for c in range(XDIMENSION):
            unit = gameMap.getTile(r, c).getUnit()
            if not (unit is None):
                screen.blit(IMAGES[unit.image], p.Rect(c*SQ_SIZE + 10, r*SQ_SIZE + 10, SQ_SIZE, SQ_SIZE))
                drawHP(screen, unit, SQ_SIZE)

'''
Draws the HP bar for a unit based on its current HP.
    screen = Where the game is displayed
    unit = a unit object
    sqSize = the length of a tile
'''
def drawHP(screen, unit, sqSize):
    hpPercent = unit.hpLeft/unit.maxHP
    if hpPercent <= 0.2:
        hpColor = p.Color("red")
    elif hpPercent <= 0.5:
        hpColor = p.Color("gold")
    else:
        hpColor = p.Color("forestGreen")
    s = p.Surface((sqSize*0.8, sqSize*0.125))
    s.fill(p.Color("lightGray"))
    p.draw.rect(s, hpColor, p.Rect(sqSize*0.05, sqSize//32, hpPercent*(sqSize*0.7), sqSize//16))
    screen.blit(s, ((unit.loc[1] + 0.1)*sqSize, (unit.loc[0] + 0.85)*sqSize))
                
def animateMove(screen, gameMap, dims, move):
    for i in range(len(move.path)-1):
        gameMap.mapAddUnit(None, move.path[i].getCoords()[0], move.path[i].getCoords()[1])
        gameMap.mapAddUnit(move.unitMoved, move.path[i+1].getCoords()[0], move.path[i+1].getCoords()[1])
        drawGameState(screen, gameMap, dims)
        p.time.delay(10)
        #p.display.flip()
        
'''
Highlights all squares a unit can move to when selected.
    screen = Where the game is displayed
    gameMap = a map array object that describes the game state
    dims = a tuple that indicates the game dimensions
    sqSelected = a tuple of coordinates the player last clicked on
    validMoves = a list of moves the player can make
'''
def highlightSquares(screen, gameMap, dims, sqSelected, validMoves):
    if sqSelected != ():
        XDIMENSION = dims[0]
        YDIMENSION = dims[1]
        SQ_SIZE = dims[2]
        r, c = sqSelected
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color("white"))
        screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
        
        for move in validMoves:
            if move.startRow == r and move.startCol == c:
                p.draw.circle(screen, (50, 50, 50, 100), ((move.endCol + 0.5)*SQ_SIZE , (move.endRow + 0.5)*SQ_SIZE), SQ_SIZE/6)
                p.draw.circle(screen, (240, 240, 240, 100), ((move.endCol + 0.5)*SQ_SIZE , (move.endRow + 0.5)*SQ_SIZE), SQ_SIZE/8)
    
    
if __name__ == "__main__":
    main()
    