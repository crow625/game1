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
        
class MapArray():
    def __init__(self, dimension):
        self.gameMap = [["--" for x in range(dimension)] for y in range(dimension)]
        self.dim = dimension
        
    def getTile(self, r, c):
        return self.gameMap[r][c]
    
    def getDim(self):
        return self.dim
    
    def getMap(self):
        return self.gameMap
    
    def addEdge(self, orig, dest):
        if isinstance(orig, Tile) and isinstance(dest, Tile):
            orig.addNeighbor(dest)
            dest.addNeighbor(orig)
        
    #constructs a dimension x dimension map of a single terrain type
    def construct(self, terrain):
        for r in range(self.dim):
            for c in range(self.dim):
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
                #move cost of -1 means invalid tile
                if neighbors[coord].getCost(unit.name) < 0:
                    continue
                dist = self.paths[f].distance + neighbors[coord].getCost(unit.name) #FUTURE PROBLEM: will count distances of -1
                #if unit has used all movement getting to this point, don't check
                if self.paths[f].distance >= unit.maxMoves:
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
            return 1000
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
    ma = MapArray(8)
    ma.construct('g')
    t0 = ma.getTile(0, 0)
    t1 = ma.getTile(0, 1)
    t2 = ma.getTile(1, 1)
    t3 = ma.getTile(2, 2)
    t4 = ma.getTile(4, 4)
    
    mu1 = gu.Warrior('u')
    
    sp = ShortestPaths()
    sp.compute(t0, mu1)
    for n in sp.shortestPath(t2):
        print(n.getCoords())
    print("Should be 0: " + str(sp.shortestPathLength(t0)))
    print("Should be 1: " + str(sp.shortestPathLength(t1)))
    print("Should be 2: " + str(sp.shortestPathLength(t2)))
    print("Should be 4: " + str(sp.shortestPathLength(t3)))
    print("Should be 1000: " + str(sp.shortestPathLength(t4)))
    
    
    '''
    mh = gd.MinHeap()
    mh.add('a', 1)
    mh.add('b', 2)
    mh.add('e', 5)
    mh.add('f', 6)
    mh.add('d', 4)
    mh.add('c', 3)
    print(mh.peek())
    while mh.size() != 0:
        print(mh.poll())
    '''
        
def addPair(p1, p2):
    r = p1[0] + p2[0]
    c = p1[1] + p2[1]
    return (r, c)
    
if __name__ == "__main__":
    main()
    