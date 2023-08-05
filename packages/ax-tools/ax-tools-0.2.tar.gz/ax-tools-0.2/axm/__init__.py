import time
class TagBuffer:
    'Provides .axm memory file manipulation buffer'
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
        open(path,'w').write(raw)
            
    def updatetags(self,new_tag_dict):
        self.current = new_tag_dict
        
class Item:
    'Provides a simple class for inventory items'
    def __init__(self,name,classification=0,rarity=0,damage=0,effects=[]):
        self.n = name
        self.c = classification
        self.r = rarity
        self.d = damage
        self.e = effects
        
    def getName(self):
        return self.n
    
    def getClass(self):
        return self.c
    
    def getDamage(self):
        return self.d
    
    def getRarity(self):
        return self.r
    
    def getEffects(self):
        return self.e
    
    def setName(self,name):
        self.n = name
        
    def setClass(self,classification):
        self.c = classification
        
    def setDamage(self,damage):
        self.d = damage
        
    def setRarity(self,rarity):
        self.r = rarity
        
    def setEffects(self,effects):
        self.e = effects
        
class Player:
    'Provides a simple class for making a player. Use meta to store metadata such as inventory'
    def __init__(self,name,max_health,defense=0,meta={}):
        self.n = name
        self.hp,self.mp = [int(max_health)]*2
        self.d = int(defense)
        self.meta = meta
        
    def damage(self,hp):
        if (int(hp) - defense) < 0:
            return 1
        else:
            self.hp -= int(hp) - defense
            if self.hp <= 0:
                return 0
            return 1
    
    def heal(self,hp):
        self.hp += int(hp)
        if self.hp > self.mp:
            self.hp = self.mp
            return 1
        return 0
    
    def getHP(self):
        return self.hp
    
    def setHP(self,hp):
        self.hp = int(hp)
        if self.hp > self.mp:
            self.hp = self.mp
            return 1
        return 0
    
    def getMeta(self):
        return self.meta
    
    def setMeta(self,meta):
        self.meta = meta
        
    def getDefense(self):
        return self.d
    
    def setDefense(self,defense):
        self.d = int(defense)

class LogBuffer:
    'Provides .axm log file manipulation buffer'
    def __init__(self,path):
        self.path = path
        self.file = open(path,'a')
        self.log = []
        
    def log(self,line,importance=0):
        self.log.append(str(importance) + ' [' + time.time() + '] ' + line)
        
    def write(self):
        self.file.write('\n'.join(self.log))
        self.log = []