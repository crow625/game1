#may 22 2021
#game1
'''
Defines how the game map is stored.
'''

import game1Data as gd
import game1Units as gu

#should be deleted: cost library should be tied to unit. There will be many more units than terrain types.
'''
GRASS_COST = {'W': 1}
DESERT_COST = {'W': 2}
MOUNTAIN_COST = {'W': 3}
WATER_COST = {'W': -1}
VOID_COST = {'W': 0}

TERR_COST = {'g': GRASS_COST, 'd': DESERT_COST, 'm': MOUNTAIN_COST, 'w': WATER_COST, '-': VOID_COST}
'''

'''
An individual square on the map.
'''
class Tile():
    #constructs a tile at (r, c) with the given terrain type
    def __init__(self, r, c, terrain):
        self.coords = (r, c)
        self.neighbors = {} #map coords to tile
        self.terrain = terrain
        self.unit = None
        
    def getCoords(self):
        return self.coords
    
    def getTerrain(self):
        return self.terrain
        
    def getNeighbors(self):
        return self.neighbors
    
    #what it would cost for given unit to move to this tile
    def getCost(self, unit):
        return unit.moveCost[self.terrain]
    
    #adds a neighbor tile t
    def addNeighbor(self, t):
        if not isinstance(t, Tile):
            return
        self.neighbors[t.getCoords()] = t
        
    def addUnit(self, u):
        self.unit = u
    
    def getUnit(self):
        return self.unit
        
'''
Responsible for generating the map and keeping track of the layout.
'''
class MapArray():
    #read gamemap from txt file
    def __init__(self, filename):
        badMap = False
        try:
            file = open("maps/" + filename, 'r')
        except:
            print("Bad map: File not found. Opening map 1 instead.")
            file = open("maps/map1.txt")
        try:    
            self.unitsPerTeam = int(file.readline().strip('\n'))
        except:
            self.unitsPerTeam = 2
            print("Bad map: Units per team not specified. Defaulted to {}.".format(self.unitsPerTeam))
            badMap = True
        try:
            userStartSet = file.readline().strip('\n').split(';')
            enemyStartSet = file.readline().strip('\n').split(';')
            self.readStartTiles(userStartSet, enemyStartSet)
            badStarts = False
        except:
            print("Bad map: Start tiles not specified. Defaulted to top and bottom corners.")
            badStarts = True
            badMap = True
            
        if badMap:
            #open old method: no header at all, just terrain. Other
            file = open("maps/" + filename, 'r')
        
        self.gameMap = []
        r = 0
        for line in file:
            #ignore commented out lines
            if '#' in line:
                continue
            c = 0
            line = line.strip('\n')
            line_list = line.split(' ')

            row = []
            for terr in line_list:
                t = Tile(r, c, terr)
                row.append(t)
                c += 1
            self.gameMap.append(row)
            r += 1
            
        self.ydim = len(self.gameMap)
        self.xdim = len(self.gameMap[0])
        #if (self.y != self.ydim) or (self.x != self.xdim):
            #print("Incorrect dimensions specified by map (Not fatal).")
        
        #Add neighbors
        for r in range(self.ydim):
            for c in range(self.xdim):
                directions = ((0, -1), (-1, 0), (0, 1), (1, 0))
                for d in directions:
                    n_r = r + d[0]
                    n_c = c + d[1]
                    if 0 <= n_r < self.ydim and 0 <= n_c < self.xdim:
                        self.addEdge(self.getTile(r, c), self.getTile(n_r, n_c))
            
        if badStarts:
            self.userStart = [(self.ydim - 1, self.xdim - 1), (self.ydim - 1, 0)]
            self.enemyStart = [(0, 0), (0, self.xdim - 1)]
        self.numUnits = {'u': 0, 'e': 0}
        
    def readStartTiles(self, userSet, enemySet):
        self.userStart = []
        self.enemyStart = []
        for coords in userSet:
            if '(' in coords:
                coords = coords.strip("()")
            coords = coords.split(',')
            x = int(coords[0])
            y = int(coords[1])
            self.userStart.append((y,x))
        for coords in enemySet:
            if '(' in coords:
                coords = coords.strip("()")
            coords = coords.split(',')
            x = int(coords[0])
            y = int(coords[1])
            self.enemyStart.append((y,x))
        return
        
    def getTile(self, r, c):
        return self.gameMap[r][c]
    
    def getYdim(self): #r
        return self.ydim
    
    def getXdim(self): #c
        return self.xdim
    
    def getMap(self):
        return self.gameMap
    
    def mapAddUnit(self, u, r, c):
        t = self.getTile(r, c)
        #unit already exists on that tile, so decrement its team count
        if not (t.getUnit() is None):
            self.numUnits[t.getUnit().team] = self.numUnits[t.getUnit().team] - 1
            
        t.addUnit(u)
        #add None unit: don't increase number of units
        #when a unit moves, add it to the destination tile
        #and add None unit to the origin tile
        if u is None:
            return
        #first unit of this team to be added
        u.loc = (r, c)
        if not (u.team in self.numUnits.keys()):
            self.numUnits[u.team] = 1
        else:
            self.numUnits[u.team] = self.numUnits[u.team] + 1
        
    def mapGetUnit(self, r, c):
        return self.getTile(r, c).getUnit()
    
    def addEdge(self, orig, dest):
        if isinstance(orig, Tile) and isinstance(dest, Tile):
            orig.addNeighbor(dest)
            dest.addNeighbor(orig)
        
    #constructs a dimension x dimension map of a single terrain type
    def construct(self, dimension, terrain):
        self.dim = dimension
        self.gameMap = [["--" for x in range(self.dim)] for y in range(self.dim)]
        for r in range(dimension):
            for c in range(dimension):
                t = Tile(r, c, terrain)
                self.gameMap[r][c] = t
                directions = ((0, -1), (-1, 0), (0, 1), (1, 0))
                for d in directions:
                    n_r = r + d[0]
                    n_c = c + d[1]
                    if 0 <= n_r < self.dim and 0 <= n_c < self.dim:
                        self.addEdge(t, self.getTile(n_r, n_c))
                        
class ShortestPaths():
    def __init__(self):
        self.paths = {} #map node (tile) to path data
        
    def compute(self, orig, unit):
        #orig: tile object, unit: unit object
        #frontier has value tile, and priority distance
        frontier = gd.MinHeap()
        frontier.add(orig, 0) #original tile has distance 0
        self.paths[orig] = self.PathData(0, None) #no previous node, give it terrain type with 0 movement cost
        
        while frontier.size() != 0:
            
            f = frontier.poll() #f is a tile, THE CLOSEST tile to the origin that has not been determined yet
            
            neighbors = f.getNeighbors() #neighbors is a dictionary that maps coordinates to a tile
            
            for coord in list(neighbors): #for every neighbor
                #add the current distance to the cost of the tile we're currently checking
                #move cost of -1 means invalid tile, so skip
                if neighbors[coord].getCost(unit) < 0:
                    continue
                #cannot walk through enemy units
                if (not (neighbors[coord].getUnit() is None)) and (neighbors[coord].getUnit().team != unit.team):
                    continue
                dist = self.paths[f].distance + neighbors[coord].getCost(unit)
                #if unit has used all movement getting to this point, don't check beyond it 
                if self.paths[f].distance >= unit.movesLeft:
                    continue
                
                #if tile does not have an entry in paths, it is new
                if self.paths.get(neighbors[coord]) is None:
                    #add map from tile to pathdata
                    self.paths[neighbors[coord]] = self.PathData(dist, f)
                    #add tile to frontier
                    frontier.add(neighbors[coord], dist) 
                    
                elif self.paths[f].distance + neighbors[coord].getCost(unit) < dist:
                    
                    self.paths[neighbors[coord]] = self.PathData(dist, f)
                    
    def shortestPathLength(self, dest):
        if self.paths.get(dest) is None:
            return -1
        return self.paths[dest].distance
    
    def shortestPath(self, dest):
        if self.paths.get(dest) is None:
            return None
        route = []
        route.append(dest)
        current = dest
        
        while not (self.paths[current].previous is None):
            route.append(self.paths[current].previous)
            current = self.paths[current].previous
            #keep going until you reach the origin, because its backpointer is None
            #current = origin
            
        if current == dest: #if origin is destination, just return the one node
            return route
        #route.append(current) - origin was included twice so throw that out?
        
        #route is in reverse order: destination -> origin
        route2 = []
        while len(route) > 0:
            route2.append(route.pop())
            
        return route2
                    
    #map terrain (distance dictionary) to previous node
    class PathData():
        def __init__(self, dist, prev):
            #distance: terrain dictionary
            #prev: tile
            self.distance = dist
            self.previous = prev          
       
def main():
    ma = MapArray("map1.txt")
    mu1 = gu.Warrior('u')
    t0 = ma.getTile(0, 0)
    t1 = ma.getTile(4, 0)
    
    sp = ShortestPaths()
    sp.compute(t0, mu1)
    print(sp.shortestPathLength(t1))
    
    
        
def addPair(p1, p2):
    r = p1[0] + p2[0]
    c = p1[1] + p2[1]
    return (r, c)
    
if __name__ == "__main__":
    main()
    