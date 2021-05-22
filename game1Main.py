#May 16 2021
#game1
'''
Responsible for handling user input and displaying the current game state.
'''

import pygame as p
import game1Engine

p.init()

WIDTH = HEIGHT = 512
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

'''
Load images
'''
def loadImages():
    units = ["uW", "eW"]
    for unit in units:
        IMAGES[unit] = p.transform.scale(p.image.load("./images/" + unit + ".png"), (SQ_SIZE, SQ_SIZE))
        
        
'''
The main driver for code.
'''
def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = game1Engine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    
    loadImages()
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
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                #sqSelected is always the most recent location
                sqSelected = (row, col)
                playerClicks.append(sqSelected)
                
                if len(playerClicks) == 1:
                    print("1 click")
                    firstUnit = gs.units[(playerClicks[0])[0]][(playerClicks[0])[1]]
                    #first click was empty: toss
                    if firstUnit == "--":
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
                    firstUnit = gs.units[(playerClicks[0])[0]][(playerClicks[0])[1]]
                    secondUnit = gs.units[(playerClicks[1])[0]][(playerClicks[1])[1]]
                    
                    #clicked same unit twice: toss last click
                    if playerClicks[1] == playerClicks[0]:
                        print("same unit")
                        sqSelected = ()
                        playerClicks.pop()
                    
                    #clicked on another unit
                    if secondUnit != "--":
                        #enemy unit: toss last click
                        if firstUnit.team != secondUnit.team:
                            print("enemy unit")
                            sqSelected = ()
                            playerClicks.pop()
                        #else team unit: make last click first click
                        else:
                            print("other team unit")
                            sqSelected = ()
                            playerClicks[0] = playerClicks[1]
                            playerClicks.pop()
                    #clicked empty square
                    else:
                        print("clicked empty square")
                        move = game1Engine.Move(playerClicks[0], playerClicks[1], gs.gameMap, 0)
                        print(move.moveID)
                        print(validMoves)
                        for m in validMoves:
                            print(m.moveID)
                            if m.moveID == move.moveID:
                                print("valid move")
                                gs.makeMove(move)
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                        if moveMade:
                            sqSelected = ()
                            playerClicks = []
                        else:
                            print("invalid move")
                            sqSelected = ()
                            playerClicks.pop()
                        
                            
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = false
            #restore moves at turn rollover
            for unit in gs.units:
                if unit == "--":
                    continue
                elif (unit.team == 'u' and gs.userToMove) or (unit.team == 'e' and (not gs.userToMove)):
                    unit.movesLeft = unit.maxMoves
                    
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        
def drawGameState(screen, gs):
    drawMap(screen, gs.gameMap)
    drawUnits(screen, gs.units)
    
    
def drawMap(screen, gameMap):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = COLORS[gameMap[r][c]]
            border_color = BORDER_COLORS[gameMap[r][c]]
            p.draw.rect(screen,border_color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            p.draw.rect(screen,color, p.Rect(c*SQ_SIZE + BORDER_WIDTH, r*SQ_SIZE + BORDER_WIDTH, SQ_SIZE - 2*BORDER_WIDTH, SQ_SIZE - 2*BORDER_WIDTH))

            
def drawUnits(screen, units):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            unit = units[r][c]
            if unit != "--":
                screen.blit(IMAGES[unit.image], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
    
    
if __name__ == "__main__":
    main()
    