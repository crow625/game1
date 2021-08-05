#May 16 2021
#game1
'''
Responsible for handling user input and displaying the current game state.
'''

import sys
import pygame as p
import pygame.freetype as pf
import game1Engine as ge

p.init()

HEIGHT = 768
LIBRARY_WIDTH = 320
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
text_file = "gametext.txt"

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
    DIMENSIONS = (XDIMENSION, YDIMENSION, SQ_SIZE, LIBRARY_WIDTH, WIDTH, HEIGHT)
    
    screen = p.display.set_mode((WIDTH + LIBRARY_WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages(SQ_SIZE, gs.allUnits)
    gs.loadText(text_file)
    libPage = 0
    maxLib = len(gs.allUnits)//3
    running = True
    phase1 = False
    phase2 = True
    playerClicks = []
    while running:
        location = p.mouse.get_pos()
        col = location[0]//SQ_SIZE
        row = location[1]//SQ_SIZE
        gs.mouseoverLogic((row, col))
        gs.forecastLogic((row, col), playerClicks)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                
            if e.type == p.KEYDOWN:
                if e.key == p.K_RETURN: #enter ends turn
                    playerClicks = []
                    gs.refreshMoves()
                    validMoves = gs.getValidMoves()
                elif e.key == p.K_RIGHT and libPage < maxLib:
                    libPage += 1
                elif e.key == p.K_LEFT and libPage > 0:
                    libPage -= 1
                    
            elif e.type == p.MOUSEBUTTONDOWN:
                playerClicks.append((row, col))
                
                (playerClicks, moveMade) = gs.clickLogic(playerClicks, validMoves)
                            
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            #animateMove(screen, gs.gameMap, DIMENSIONS, m)
                    
        gameOver = gs.victoryCheck()
        if gameOver:
            running = False
        drawGameState(screen, gs, DIMENSIONS, playerClicks, validMoves, gs.TEXT, libPage)
        clock.tick(MAX_FPS)
        p.display.flip()
        
'''
Draws everything about the current state of the game.
    screen = Where the game is displayed
    gs = The current game state
    dims = a tuple that indicates the game dimensions
    playerClicks = an array of 2-D tuples that indicate the player's latest clicks
    validMoves = a list of moves the player can make
'''
def drawGameState(screen, gs, dims, playerClicks, validMoves, text, libPage):
    drawMap(screen, gs.gameMap, dims)
    drawUnits(screen, gs.gameMap, dims)
    highlightSquares(screen, dims[2], playerClicks, validMoves)
    drawLibrary(screen, dims, text, gs.allUnits, libPage)
    
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
            unit = gameMap.mapGetUnit(r, c)
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
        
'''
Highlights all squares a unit can move to when selected.
    screen = Where the game is displayed
    sqSize = the length of a tile
    playerClicks = an array of 2-D tuples that indicate the player's latest clicks
    validMoves = a list of moves the player can make
'''
def highlightSquares(screen, sqSize, playerClicks, validMoves):
    if len(playerClicks) > 0:
        r, c = playerClicks[-1]
        s = p.Surface((sqSize, sqSize))
        s.set_alpha(100)
        s.fill(p.Color("white"))
        screen.blit(s, (c*sqSize, r*sqSize))
        
        for move in validMoves:
            if move.startRow == r and move.startCol == c:
                p.draw.circle(screen, (50, 50, 50, 100), ((move.endCol + 0.5)*sqSize , (move.endRow + 0.5)*sqSize), sqSize/6)
                p.draw.circle(screen, (240, 240, 240, 100), ((move.endCol + 0.5)*sqSize , (move.endRow + 0.5)*sqSize), sqSize/8)
                for atk in move.attacks:
                    p.draw.circle(screen, (50, 50, 50, 100), ((atk[1] + 0.5)*sqSize , (atk[0] + 0.5)*sqSize), sqSize/6)
                    p.draw.circle(screen, (240, 50, 50, 100), ((atk[1] + 0.5)*sqSize , (atk[0] + 0.5)*sqSize), sqSize/8)
               
'''
Draws the library of unit statistics to the right on the game map.
    screen = where the game is displayed
    dims = a tuple that indicates the game dimensions
    text = the dictionary of game text from the game state.
'''
def drawLibrary(screen, dims, text, unitList, page):
    sqSize = dims[2]
    libWidth = dims[3]
    width = dims[4]
    height = dims[5]
    lib = p.Surface((libWidth, height))
    lib.fill(p.Color("sky blue")) #bg
    p.draw.rect(lib, p.Color("royal blue"), p.Rect(0, 0, libWidth, height), BORDER_WIDTH) #bg border
    pf.SysFont(p.font.get_default_font(), 25).render_to(lib, (8, 8), text.get("TXT_LIB_HEAD"), p.Color("black")) #header text
    
    unit1 = unitList[page*3]
    lib.blit(IMAGES[unit1], p.Rect(32, 32, libWidth, libWidth))
    if len(unitList) > page*3 + 2:
        unit3 = unitList[page*3 + 2]
        lib.blit(IMAGES[unit3], p.Rect(32, 32 + sqSize*2, sqSize, sqSize))
    if len(unitList) > page*3 + 1:
        unit2 = unitList[page*3 + 1]
        lib.blit(IMAGES[unit2], p.Rect(32, 32 + sqSize, sqSize, sqSize))
        
    screen.blit(lib, (width, 0))
    
if __name__ == "__main__":
    main()
    