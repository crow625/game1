#May 22 2021
#game1

'''
ArrayList and Min Heap data structures
'''

class AList():
    def __init__(self):
        #map index to item
        self.a = {}
        #how many elements are in it
        self.size = 0
        
    def size(self):
        return self.size
    
    def get(self, i):
        #return the ith element of a
        if (i > self.size) or (i < 0):
            raise IndexError("Index " + str(i) + " out of bounds for array of size " + str(self.size))
        return self.a.get(i)
        
    def put(self, i, value):
        #set the ith value of a to value
        if (i < 0):
            raise IndexError("Index " + str(i) + " out of bounds for array")
        self.a[i] = value
        #if (self.a.get(i) is None):
        #    self.size += 1
        
    def append(self, value):
        #add the value to the end of the list
        self.size += 1
        print("Value " + value.v + " was added in position " + str(self.size))
        self.a[self.size] = value
        
    def pop(self):
        #remove and return last value
        
        val = self.a[self.size]
        self.a[self.size] = None
        self.size -= 1
        return val
    
    
class MinHeap():
    def __init__(self):
        #c is an array list of Entries (values and priorities)
        self.c = AList()
        #keymap maps values to integers?
        self.keyMap = {}
        
    #add entry with value and priority to heap
    def add(self, value, priority):
        A = self.Entry(value, priority)
        self.c.append(A)
        self.keyMap[value] = self.c.size()
        
    #return value with lowest priority
    def peek(self):
        return self.c.get(1).v
    
    #return and remove value with lowest priority
    def poll(self):
        val = self.peek() #minheap
        self.keyMap[val] = None
        popper = self.c.pop() #alist
        self.c.put(1, popper)
        
        self.keyMap[popper.v] = 1
        self.bubbleDown(1)
        return val
        
    #return # of values in heap 
    def size(self):
        return self.c.size()
    
    #swap c[h] and c[k]
    
    def swap(self, h, k):
        temp = self.Entry(self.c.get(h).v, self.c.get(h).p)
        
        self.c.put(h, self.c.get(k))
        self.keyMap[self.c.get(k).v] = h
        
        self.c.put(k, temp)
        self.keyMap[self.c.get(h).v] = k
        
    #bubble up c[k] to its right place in heap
    def bubbleUp(self, k):
        #k at root, finished bubbling
        if k == 1:
            return
        #k out of bounds, no need to bubble
        elif k >= c.aSize():
            return
        
        kP = k//2 #parent index
        if (self.c.get(k).p > self.c.get(kP).p): #if k's priority is > parent's, bubbling finished
            return
        swap(k, kP)
        self.bubbleUp(kP)
        
    #bubble down c[k] to its right place in heap
    def bubbleDown(self, k):
        kR = 2*k + 1
        kL = 2*k
        
        if kL >= self.c.size(): #if left child doesn't exist, k has no children and bubbling is finished
            return
        #left child has higher priority and there is no right child, return
        #this check was not necessary in java because you can .compareTo(null)
        if (self.c.get(k).p < self.c.get(kL).p) and (self.c.get(kR) is None):
            return
        if (self.c.get(k).p < self.c.get(kL).p) and (self.c.get(k).p < self.c.get(kR).p):
            #if k's priority is less than both its childrens', bubbling is finished
            return
        smaller = self.smallerChild(k)
        self.swap(k, smaller)
        self.bubbleDown(smaller)
        
    def smallerChild(self, k):
        kR = 2*k + 1
        kL = 2*k
        if self.keyMap.get(kR) is None: #if right child doesn't exist, return left child
            return kL
        pR = self.c.get(kR).p
        pL = self.c.get(kL).p
        if pL < pR:
            return kL
        return kR
        
        
    class Entry():
        def __init__(self, value, priority):
            self.v = value
            self.p = priority
            
        
    
    
    
    
    