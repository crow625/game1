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
          'm': p.Color("gray"), 'd': p.Color("yellow")}
BORDER_COLORS = {'g': p.Color("dark green"), 'w': p.Color("blue"),
                 'm': p.Color("dim gray"), 'd': p.Color("goldenrod")}
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
    moveMade = False
    
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col): #clicking same square twice to cancel input
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                    
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
                screen.blit(IMAGES[unit], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
    
    
if __name__ == "__main__":
    main()
    