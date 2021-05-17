#May 16 2021
#game1
'''
Stores all information about the current state of the map.
Also responsible for determining all valid moves.
'''

class GameState():
    def __init__(self): #what executes on startup
        '''
        'g' = grass
        'w' = water
        'm' = mountain
        'd' = desert
        '''
        self.gameMap = [
            ['m','m','w','m','g','g','g','g'],
            ['g','m','w','g','g','g','g','g'],
            ['g','g','w','w','g','g','g','g'],
            ['g','g','g','w','w','w','g','g'],
            ['g','g','g','g','g','w','w','w'],
            ['g','g','g','g','g','g','g','g'],
            ['g','g','g','g','g','g','d','d'],
            ['g','g','g','g','g','d','d','d']]
            
        self.units = [
            ["--", "--", "--", "--", "--", "--", "--", "eW"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["uW", "--", "--", "--", "--", "--", "--", "--"]]
        
        self.classMoves = {'W': 4}
        
        self.turnCount = 0
                