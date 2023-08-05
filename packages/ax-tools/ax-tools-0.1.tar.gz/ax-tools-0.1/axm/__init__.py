class MBuffer:
    def __init__(self,path,tags={}):
        self.path = path
        self.file = open(path,'a+')
        self.current = tags
        for line in self.file.read().splitlines():
            line = line.split('=')
            self.current[line[0]] = '='.join(line[1:])
            
    def gettag(self,tag_name):
        return self.current[tag_name]
    
    def rawtags(self):
        return self.current
    
    def settag(self,tag_name,tag_string):
        self.current[tag_name] = str(tag_string)
        
    def save(self,path):
        raw = ''
        for tag_name in self.current:
            raw += '%s=%s\n' % (tag_name,self.current[tag_name])
            
    def updatetags(self,new_tag_dict):
        self.current = new_tag_dict