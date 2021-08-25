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
UNITS_PER_PAGE = 4
ALTERNATE = True
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
    IMAGES["uUnit"] = p.transform.scale(p.image.load("./images/uUnit.png"), (LIBRARY_WIDTH//2, LIBRARY_WIDTH//2))
    IMAGES["eUnit"] = p.transform.scale(p.image.load("./images/eUnit.png"), (LIBRARY_WIDTH//2, LIBRARY_WIDTH//2))
    for unit in units:
        for team in unit:
            try:
                IMAGES[team.image] = p.transform.scale(p.image.load("./images/" + team.image + ".png"), (LIBRARY_WIDTH//2, LIBRARY_WIDTH//2))
            except:
                print("Could not find unit {} image".format(team.image))
                IMAGES[team.image] = p.transform.scale(p.image.load("./images/uUnit.png"), (LIBRARY_WIDTH//2, LIBRARY_WIDTH//2))
        
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
    tryEnd = False
    howTo = False
    loadImages(SQ_SIZE, gs.allUnits)
    gs.loadText(text_file)
    libPage = 0
    libSelected = None
    if len(gs.allUnits)%UNITS_PER_PAGE == 0:
        maxLib = len(gs.allUnits)//UNITS_PER_PAGE - 1
    else:
        maxLib = len(gs.allUnits)//UNITS_PER_PAGE
    #gameTime = 0
    running = True
    playerClicks = []
   
    while running:
        gs.gameTime += 1
        if ALTERNATE and gs.gameTime%50 == 0:
            gs.cycle = 0
        elif ALTERNATE and gs.gameTime%25 == 0:
            gs.cycle = 1
        location = p.mouse.get_pos()
        col = location[0]//SQ_SIZE
        row = location[1]//SQ_SIZE
        if gs.phase2:
            gs.mouseoverLogic((row, col))
            gs.forecastLogic((row, col), playerClicks)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                
            if e.type == p.KEYDOWN:
                if e.key == p.K_RETURN: #enter ends turn
                    if gs.phase2:
                        playerClicks = []
                        gs.refreshMoves()
                        validMoves = gs.getValidMoves()
                    elif gs.phase1 and not tryEnd:
                        tryEnd = True
                        print("End phase 1?")
                    elif gs.phase1 and tryEnd:
                        playerClicks = []
                        gs.userToMove = not gs.userToMove
                        if gs.userToMove: #end of phase 1
                            gs.phase1 = False
                            gs.phase2 = True
                            validMoves = gs.getValidMoves()
                
                elif e.key == p.K_RIGHT and libPage < maxLib:
                    libPage += 1
                    tryEnd = False
                elif e.key == p.K_LEFT and libPage > 0:
                    libPage -= 1
                    tryEnd = False
                    
            elif e.type == p.MOUSEBUTTONDOWN:
                tryEnd = False
                playerClicks.append((row, col))
                if col < gs.gameMap.getXdim():
                    if gs.phase2:
                        (playerClicks, moveMade) = gs.clickLogic(playerClicks, validMoves)
                    elif gs.phase1:
                        playerClicks = gs.addUnitLogic(playerClicks, libSelected, libPage, UNITS_PER_PAGE)
                    libSelected = None
                else: #clicking in the library resets playerclicks and does not trigger clickLogic
                    playerClicks = []
                    newLib = gs.libLogic(location, DIMENSIONS, libPage, UNITS_PER_PAGE, howTo)
                    if newLib == '?':
                        howTo = True
                    elif newLib == 'X':
                        howTo = False
                    elif newLib == libSelected:
                        libSelected = None
                    else:
                        libSelected = newLib
                            
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            #animateMove(screen, gs.gameMap, DIMENSIONS, m)
        if gs.phase2 and gs.victoryCheck():
            running = False
        drawGameState(screen, gs, DIMENSIONS, playerClicks, validMoves, libPage, location, libSelected, howTo)
        clock.tick(MAX_FPS)
        p.display.flip()
        
'''
Draws everything about the current state of the game and library.
    screen = Where the game is displayed
    gs = The current game state
    dims = a tuple that indicates the game dimensions
    playerClicks = an array of 2-D tuples that indicate the player's latest clicks
    validMoves = a list of moves the player can make
    text = dictionary, the game's text files
    libPage = the current page of the library
    mousePos = the mouse's coordinates. tuple (x, y)
    libSelected = the unit slot selected in the library. None if no library unit selected.
    howTo = boolean that indicated whether the how to play screen is currently being displayed.
'''
def drawGameState(screen, gs, dims, playerClicks, validMoves, libPage, mousePos, libSelected, howTo):
    drawMap(screen, gs.gameMap, dims)
    drawUnits(screen, gs.gameMap, dims)
    if howTo:
        drawHowTo(screen, gs.TEXT, dims)
    else:
        drawLibrary(screen, dims, gs.TEXT, gs.allUnits, libPage, gs.cycle, gs.userToMove, gs.turnCount)
    if gs.userToMove:
        startSet = gs.gameMap.userStart
    else:
        startSet = gs.gameMap.enemyStart
    highlightSquares(screen, dims, playerClicks, validMoves, libSelected, gs.phase1, startSet)
    #drawSelectedUnit(screen, playerClicks, mousePos, gs.gameMap, dims[2])
    
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
                screen.blit(p.transform.scale(IMAGES[unit.image], (SQ_SIZE - 20, SQ_SIZE - 20)), p.Rect(c*SQ_SIZE + 10, r*SQ_SIZE + 10, SQ_SIZE - 20, SQ_SIZE - 20))
                drawHP(screen, unit, SQ_SIZE)

'''
Draws the HP bar for a unit based on its current HP.
Also displays its current HP as a number to the right of the bar.
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
    p.draw.circle(screen, p.Color("lightGray"), ((unit.loc[1]+0.917)*sqSize, (unit.loc[0]+0.916)*sqSize), sqSize//13) #hp number circle
    s = p.Surface((sqSize*0.8, sqSize*0.125)) #gray background of HP bar
    s.fill(p.Color("lightGray"))
    p.draw.rect(s, hpColor, p.Rect(sqSize*0.05, sqSize//32, hpPercent*(sqSize*0.7), sqSize//16)) #HP bar
    screen.blit(s, ((unit.loc[1] + 0.1)*sqSize, (unit.loc[0] + 0.85)*sqSize))
    if unit.hpLeft < 10:
        margin = 0.9
    else:
        margin = 0.86
    pf.SysFont(p.font.get_default_font(), sqSize//10).render_to(screen, ((unit.loc[1]+margin)*sqSize, (unit.loc[0]+0.88)*sqSize), str(unit.hpLeft), p.Color("black"))
                
def animateMove(screen, gameMap, dims, move):
    for i in range(len(move.path)-1):
        gameMap.mapAddUnit(None, move.path[i].getCoords()[0], move.path[i].getCoords()[1])
        gameMap.mapAddUnit(move.unitMoved, move.path[i+1].getCoords()[0], move.path[i+1].getCoords()[1])
        drawGameState(screen, gameMap, dims)
        p.time.delay(10)
        
'''
Highlights all squares a unit can move to when selected.
Also highlights a unit in the library when selected.
    screen = Where the game is displayed
    sqSize = the length of a tile
    playerClicks = an array of 2-D tuples that indicate the player's latest clicks
    validMoves = a list of moves the player can make
    libSelected = the unit slot selected in the library. None if no unit selected.
    phase1 = boolean that indicates whether the game is in phase 1.
    startSet = the set of starting tiles for the player whose turn it is. array of (r, c) tuples
'''
def highlightSquares(screen, dims, playerClicks, validMoves, libSelected, phase1, startSet):
    if len(playerClicks) > 0:
        sqSize = dims[2]
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
    if not (libSelected is None) and phase1:
        sqSize = dims[2]
        libWidth = dims[3]
        width = dims[4]
        s = p.Surface((libWidth//2, libWidth//2))
        s.set_alpha(100)
        s.fill(p.Color("white"))
        screen.blit(s, (16 + width, 64 + libSelected*libWidth//2))
        for loc in startSet:
            s = p.Surface((sqSize, sqSize))
            s.set_alpha(100)
            s.fill(p.Color("white"))
            screen.blit(s, (loc[1]*sqSize, loc[0]*sqSize))

               
'''
Draws the library of unit statistics to the right on the game map.
    screen = where the game is displayed
    dims = a tuple that indicates the game dimensions
    text = the dictionary of game text from the game state.
'''
def drawLibrary(screen, dims, text, unitList, page, cycle, userToMove, turnCount):
    sqSize = dims[2]
    libWidth = dims[3]
    width = dims[4]
    height = dims[5]
    lib = p.Surface((libWidth, height))
    lib.fill(p.Color("sky blue")) #bg
    p.draw.rect(lib, p.Color("royal blue"), p.Rect(0, 0, libWidth, height), BORDER_WIDTH) #bg border
    pf.SysFont(p.font.get_default_font(), 30).render_to(lib, (8, 8), text.get("TXT_LIB_HEAD"), p.Color("black")) #header text
    pf.SysFont(p.font.get_default_font(), libWidth//10).render_to(lib, (libWidth*0.93, 8), "?", p.Color("black")) #how to play clickable
    
    unit1 = unitList[page*UNITS_PER_PAGE][cycle]
    drawUnitInfo(lib, libWidth, unit1, 0)
    if len(unitList) > page*UNITS_PER_PAGE + 3 and UNITS_PER_PAGE >= 4:
        unit4 = unitList[page*UNITS_PER_PAGE + 3][cycle]
        drawUnitInfo(lib, libWidth, unit4, 3)
    if len(unitList) > page*UNITS_PER_PAGE + 2:
        unit3 = unitList[page*UNITS_PER_PAGE + 2][cycle]
        drawUnitInfo(lib, libWidth, unit3, 2)
    if len(unitList) > page*UNITS_PER_PAGE + 1:
        unit2 = unitList[page*UNITS_PER_PAGE + 1][cycle]
        drawUnitInfo(lib, libWidth, unit2, 1)
        
    if userToMove:
        turn = "TXT_USER_MOVE"
    else:
        turn = "TXT_ENEMY_MOVE"
    if turnCount < 10:
        margin = 0.9
    else:
        margin = 0.87
    pf.SysFont(p.font.get_default_font(), 30).render_to(lib, (8, libWidth*2 + 96), text.get(turn), p.Color("black"))
    pf.SysFont(p.font.get_default_font(), 30).render_to(lib, (libWidth*margin, libWidth*2 + 96), str(turnCount), p.Color("black"))
    screen.blit(lib, (width, 0))
    
'''
Displays a unit's stats in the library.
    lib = the library screen
    libWidth = the width of the library
    unit = the unit whose stats are being displayed
    slot = how far down on the library the unit is displayed
'''
def drawUnitInfo(lib, libWidth, unit, slot):
    titleSpace = 64
    fontSize = libWidth//16
    moveCost = {}
    for key in unit.moveCost.keys():
        if unit.moveCost.get(key) < 0:
            moveCost[key] = 'X'
        else:
            moveCost[key] = unit.moveCost.get(key)
    unitText = [unit.name,
                "HP: {}".format(unit.maxHP),
                "Atk: {}".format(unit.atk),
                "Def: {}".format(unit.defense),
                "Moves: {}".format(unit.maxMoves),
                "G: {} D: {}".format(moveCost['g'], moveCost['d']),
                "M: {} W: {}".format(moveCost['m'], moveCost['w'])]
    lib.blit(IMAGES[unit.image], p.Rect(16, 64 + slot*libWidth//2, 1, 1))
    for line in range(len(unitText)):
        pf.SysFont(p.font.get_default_font(), fontSize).render_to(lib, (libWidth*0.6, titleSpace + fontSize*line + slot*libWidth//2), unitText[line], p.Color("black"))

'''
Draws the how to play screen over the library.
    screen = where the game is displayed
    text = the dictionary of game text from the game state.
    dims = a tuple that indicates the game dimensions
'''
def drawHowTo(screen, text, dims):
    libWidth = dims[3]
    width = dims[4]
    height = dims[5]
    headFont = libWidth//10
    subHeadFont = libWidth//12
    parFont = libWidth//20
    spacer = 8
    
    lib = p.Surface((libWidth, height))
    lib.fill((15, 10, 30, 100)) #bg
    #header
    pf.SysFont(p.font.get_default_font(), headFont).render_to(lib, (8, spacer), text.get("TXT_HOW_HEAD"), p.Color("white"))
    pf.SysFont(p.font.get_default_font(), headFont).render_to(lib, (libWidth*0.92, spacer), "X", p.Color("white"))
    #subhead 1
    spacer = libWidth*0.2
    pf.SysFont(p.font.get_default_font(), subHeadFont).render_to(lib, (8, spacer), text.get("TXT_HOW_SUBH_1"), p.Color("white"))
    spacer += libWidth*0.1
    for i in (1, 2, 3):
        parText = text.get("TXT_HOW_PAR_"+str(i))
        parChunks = chunkText(parText, 40)
        for j in range(len(parChunks)):
            pf.SysFont(p.font.get_default_font(), parFont).render_to(lib, (8, spacer), parChunks[j], p.Color("white"))
            spacer += libWidth*0.05
    #subhead 2
    spacer += libWidth*0.05
    pf.SysFont(p.font.get_default_font(), subHeadFont).render_to(lib, (8, spacer), text.get("TXT_HOW_SUBH_2"), p.Color("white"))
    spacer += libWidth*0.1
    for i in (4, 5, 6, 7, 8):
        parText = text.get("TXT_HOW_PAR_"+str(i))
        parChunks = chunkText(parText, 40)
        for j in range(len(parChunks)):
            pf.SysFont(p.font.get_default_font(), parFont).render_to(lib, (8, spacer), parChunks[j], p.Color("white"))
            spacer += libWidth*0.05
    screen.blit(lib, (width, 0))

'''
Split a long string of text into chunks that are smaller than a specified limit.
    text (string) = the string to be split
    charLimit (int) = the maximum length of a string
returns: list of subsections of the text.
'''
def chunkText(text, charLimit):
    words = text.split()
    chunks = []
    string = ""
    while len(words) > 0:
        if string != "" and len(string + " " + words[0]) < charLimit:
            string = string + " " + words.pop(0)
        elif string == "" and len(words[0]) < charLimit:
            string = words.pop(0)
        else:
            chunks.append(string)
            string = ""
    if string != "":
        chunks.append(string)
    return chunks

'''
Draws a small image of the unit selected next to the cursor.
    screen = screen where the game is displayed
    playerClicks = an array of 2-D tuples that indicate the player's latest clicks
    mousePos = tuple that indicates the position of the mouse
    gameMap = the current game map of the game state
    sqSize = the dimensions of a game square
'''
def drawSelectedUnit(screen, playerClicks, mousePos, gameMap, sqSize):
    if len(playerClicks) < 1:
        return
    unit = gameMap.mapGetUnit(playerClicks[-1][0], playerClicks[-1][1])
    screen.blit(p.transform.scale(IMAGES[unit.image], (sqSize//4, sqSize//4)), p.Rect(mousePos[0], mousePos[1], sqSize//4, sqSize//4))

if __name__ == "__main__":
    main()
    