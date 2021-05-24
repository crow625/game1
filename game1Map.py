#may 22 2021
#game1
'''
Defines how the game map is stored.
'''

import game1Data as gd

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
        return len(self.gameMap)
    
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
        self.paths = {} #map node to path data
        
    def compute(self, orig, unit):
        #orig: tile object, unit: unit object
        paths = {} #map destination tile to pathdata
        #frontier has value tile, and priority distance
        frontier = gd.MinHeap()
        frontier.add(orig, 0) #original tile has distance 0
        paths[orig] = self.PathData('-', None) #no previous node
        
        while frontier.size != 0:
            f = frontier.poll() #f is a tile
            neighbors = f.getNeighbors() #neighbors is a dictionary that maps coordinates to a tile
            
            for coord in list(neighbors): #for every neighbor
                dist = paths[f].distance[unit] + neighbors[coord].getCost(unit) #FUTURE PROBLEM: will count distances of -1
                
                if paths.get(neighbors[coord]) is None: #if tile does not have an entry in paths, it is not in frontier or seen
                    paths[neighbors[coord]] = self.PathData(neighbors[coord].getTerrain(), f) #add map from tile to pathdata
                    frontier.add(neighbors[coord], dist) #add tile to frontier
                    
                elif paths[f].distance[unit] < dist:
                    paths[neighbors[coord]] = self.PathData(neighbors[coord].getTerrain(), f)
                    
    def shortestPathLength(self, dest, unit):
        if self.paths.get(dest) is None:
            return 1000
        return self.paths[dest].distance[unit]
    
    def shortestPath(self, dest, unit):
        if self.paths[dest] is None:
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
        route.append(current)
        
        #route is in reverse order: destination -> origin
        route2 = []
        while len(route) > 0:
            route2.append(route.pop())
            
        return route2
                    
    #map terrain (distance dictionary) to previous node
    class PathData():
        def __init__(self, terr, prev):
            #distance: terrain dictionary
            #prev: tile
            self.distance = TERR_COST[terr]
            self.previous = prev          
       
def main():
    gm = MapArray(8)
    gm.construct('g')
    t0 = gm.getTile(0, 0)
    t1 = gm.getTile(1, 1)
    
    a = gd.AList()
    '''
    mh = gd.MinHeap()
    mh.add('a', 1)
    mh.add('c', 3)
    mh.add('b', 2)
    mh.add('j', 10)
    mh.add('g', 7)
    mh.add('e', 5)
    mh.add('d', 4)
    mh.add('f', 6)
    mh.add('h', 8)
    mh.add('i', 9)
    print(mh.peek())
    print(mh.peek())
    print(mh.poll())
    print(mh.poll())
    print(mh.poll())
    print(mh.poll())
    '''
    
    #sp = ShortestPaths()
    #sp.compute(t0, 'W')
    #print(sp.shortestPathLength(t1, 'W'))
        
def addPair(p1, p2):
    r = p1[0] + p2[0]
    c = p1[1] + p2[1]
    return (r, c)
    
if __name__ == "__main__":
    main()
    