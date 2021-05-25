#May 22 2021
#game1

'''
ArrayList and Min Heap data structures
'''

'''
Obsolete because array length is not fixed in python.
'''
class AList():
    def __init__(self):
        #storage
        self.a = []
        #number of elements in the AList
        self.size = 0
        
    def getSize(self):
        #return number of elements in AList
        return self.size
    
    def get(self, i):
        #return the ith element of a
        if (i > self.size) or (i < 0):
            raise IndexError("Index " + str(i) + " out of bounds for array of size " + str(self.size))
        
        return self.a[i]
        
    def put(self, i, value):
        #set the ith value of a to value. Can only overwrite existing values, not add new ones
        if (i > self.size) or (i < 0):
            raise IndexError("Index " + str(i) + " out of bounds for array")
        
        self.a[i] = value
        
    def append(self, value):
        #add the value to the end of the list
        self.size += 1
        self.a.append(value)
        
    def pop(self):
        #remove and return last value
        self.size -= 1
        return self.a.pop()
        
    
'''
A min heap of distinct values and priorities.
The value with the smallest priority is always at the root of the heap.
c represents a complete binary tree in a list. c[0] is the root.
c[2i+1] is the left child of c[i] and c[2i+2] is the right child of c[i].
keyMap maps values with their actual location in the list, such that
keyMap[c[i]] = i
'''
class MinHeap():
    def __init__(self):
        #c is a list of Entries (values and priorities)
        self.c = []
        #keymap maps values to integers?
        #tiles to ints (distance)
        self.keyMap = {}
        
    #add entry with value and priority to heap
    def add(self, value, priority):
        if value in self.keyMap:
            raise ValueError("heap add: value already in heap")
        
        A = self.Entry(value, priority)
        self.c.append(A) #if this becomes the 3rd item in c
        self.keyMap[value] = len(self.c) - 1 #then keymap[v] = 2, its position in c
        self.bubbleUp(len(self.c) - 1)
        
    #return value with lowest priority
    def peek(self):
        if len(self.c) == 0:
            raise IndexError("heap peek: heap is empty")
        return self.c[0].value
    
    #return and remove value with lowest priority
    def poll(self):
        if len(self.c) == 0:
            raise IndexError("heap poll: heap is empty")
        val = self.peek()
        self.keyMap[val] = None
        popper = self.c.pop()
        self.c[0] = popper
        
        self.keyMap[popper.value] = 0
        self.bubbleDown(0)
        return val
        
    #return # of values in heap 
    def size(self):
        return len(self.c)
    
    #swap c[h] and c[k]
    
    def swap(self, h, k):
        temp = self.Entry(self.c[h].value, self.c[h].priority)
        
        self.c[h] = self.c[k]
        self.keyMap[self.c[k].value] = h
        
        self.c[k] =  temp
        self.keyMap[self.c[h].value] = k
        
    #bubble up c[k] to its right place in heap
    def bubbleUp(self, k):
        #k at root, finished bubbling
        if k == 0:
            return
        #k out of bounds, no need to bubble
        elif k >= len(self.c):
            return
        
        kP = (k-1)//2 #parent index
        if (self.c[k].priority > self.c[kP].priority): #if k's priority is > parent's, bubbling finished
            return
        self.swap(k, kP)
        self.bubbleUp(kP)
        return
        
    #bubble down c[k] to its right place in heap
    def bubbleDown(self, k):
        kR = 2*k + 2
        kL = 2*k + 1
        
        if kL >= len(self.c): #if left child doesn't exist, k has no children and bubbling is finished
            return
        #left child has higher priority and there is no right child, return
        #this check was not necessary in java because you can .compareTo(null)
        if (self.c[k].priority < self.c[kL].priority) and (kR >= len(self.c)):
            return
        if (self.c[k].priority < self.c[kL].priority) and (self.c[k].priority < self.c[kR].priority):
            #if k's priority is less than both its childrens', bubbling is finished
            return
        smaller = self.smallerChild(k)
        self.swap(k, smaller)
        self.bubbleDown(smaller)
        
    def smallerChild(self, k):
        kR = 2*k + 2
        kL = 2*k + 1
        if kR >= len(self.c): #if right child doesn't exist, return left child
            return kL
        pR = self.c[kR].priority
        pL = self.c[kL].priority
        if pL < pR:
            return kL
        return kR
        
        
    class Entry():
        def __init__(self, value, priority):
            self.value = value
            self.priority = priority
            
        
    
    
    
    
    