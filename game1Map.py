#may 22 2021
#game1
'''
Defines how the game map is stored.
'''

import game1Data as gd
import game1Units as gu

GRASS_COST = {'W': 1}
DESERT_COST = {'W': 2}
MOUNTAIN_COST = {'W': 3}
WATER_COST = {'W': -1}
VOID_COST = {'W': 0}

TERR_COST = {'g': GRASS_COST, 'd': DESERT_COST, 'm': MOUNTAIN_COST, 'w': WATER_COST, '-': VOID_COST}

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
        return TERR_COST[self.terrain][unit]
    
    #adds a neighbor tile t
    def addNeighbor(self, t):
        if not isinstance(t, Tile):
            return
        self.neighbors[t.getCoords()] = t
        
    def addUnit(self, u):
        self.unit = u
    
    def getUnit(self):
        return self.unit
        
class MapArray():
    #read gamemap from txt file
    '''TODO: format first line of map.txt to specify dimensions to enable rectangular maps'''
    def __init__(self, filename):
        file = open("maps/" + filename, 'r')
        self.gameMap = []
        #Write contents of file to gameMap 2-D array
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
        
        #Add neighbors
        for r in range(self.ydim):
            for c in range(self.xdim):
                directions = ((0, -1), (-1, 0), (0, 1), (1, 0))
                for d in directions:
                    n_r = r + d[0]
                    n_c = c + d[1]
                    if 0 <= n_r < self.ydim and 0 <= n_c < self.xdim:
                        self.addEdge(self.getTile(r, c), self.getTile(n_r, n_c))
            
        self.numUnits = {}
        
        
    def getTile(self, r, c):
        return self.gameMap[r][c]
    
    def getYdim(self):
        return self.ydim
    
    def getXdim(self):
        return self.xdim
    
    def getMap(self):
        return self.gameMap
    
    def mapAddUnit(self, u, r, c):
        t = self.getTile(r, c)
        #unit already exists on that tile
        #so decrement its team count
        if not (t.getUnit() is None):
            self.numUnits[t.getUnit().team] = self.numUnits[t.getUnit().team] - 1
            
        t.addUnit(u)
        #add None unit: don't increase number of units
        #when a unit moves, add it to the destination tile
        #and add None unit to the origin tile
        if u is None:
            return
        #first unit of this team to be added
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
                if neighbors[coord].getCost(unit.name) < 0:
                    continue
                dist = self.paths[f].distance + neighbors[coord].getCost(unit.name)
                #if unit has used all movement getting to this point, don't check beyond it 
                if self.paths[f].distance >= unit.movesLeft:
                    continue
                
                #if tile does not have an entry in paths, it is new
                if self.paths.get(neighbors[coord]) is None:
                    #add map from tile to pathdata
                    self.paths[neighbors[coord]] = self.PathData(dist, f)
                    #add tile to frontier
                    frontier.add(neighbors[coord], dist) 
                    
                elif self.paths[f].distance + neighbors[coord].getCost(unit.name) < dist:
                    
                    self.paths[neighbors[coord]] = self.PathData(dist, f)
                    
                    #distance is not saving correctly, make it a real value, not a dictionary
                    
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
    