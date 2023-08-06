class UniversalFileBuffer:
    '''Offers universal class for file buffers. All AX Systems use this'''
    def __init__(self,path,overwrite=False):
        self.path = path
        if not overwrite:
            self.mode = 'r+'
        else:
            self.mode = 'w+'
        self.file = open(path,self.mode)
        
    def readString(self):
        '''return the whole file as a string'''
        return self.file.read()
    
    def readLine(self):
        '''return the cursor line of the file & move the cursor forward'''
        return self.file.readLine()
    
    def readList(self):
        '''return the while file as a list of lines'''
        return self.file.readLines()
    
    def write(self,string_data):
        '''write raw string data to the file'''
        self.file.write(string_data)
        
    def writeLines(self,lines):
        '''write lines to a file from iterable'''
        self.file.wrtie('\n'.join(lines))
        
    def clear(self):
        '''empty the file'''
        self.file.truncate(0)