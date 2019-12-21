class stack:
    '''This is a last in first out data strucuture
    
    ''' 
    def __init__(self, depth):
        self.size = depth
        self.items = ["0"] * depth
        self.pointer = 0 #points to top of stack
    
    def push(self, item):
        self.items[self.pointer] = item
        self.pointer += 1

        #add to top of stack
        #pointer +1
        return
    
    def pop(self):
        '''This function is not necessary for connect4.
        '''
        #remove top item
        #pointer -1 
        return
    
    def isfull(self):
        if self.pointer-1 == self.size: #pointer-1 becasue index start at 0
            return True
        else:
            return False
    
    def returnstack(self):
        return self #return the stack as an object
    
    def returnlist(self):
        return self.items #return stack as a list

    

