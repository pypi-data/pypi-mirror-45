import time
class TagBuffer:
    'Provides .axm memory file manipulation buffer'
    def __init__(self,universal_buffer,tags={}):
        self.ubuf = universal_buffer
        self.current = tags
        for line in self.ubuf.readall().splitlines():
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
        ubuf.write(raw)
            
    def updatetags(self,new_tag_dict):
        self.current = new_tag_dict
        
class Item:
    'Provides a simple class for inventory items'
    def __init__(self,name,classification=0,rarity=0,damage=0,meta={}):
        self.n = name
        self.c = classification
        self.r = rarity
        self.d = damage
        self.meta = meta
        
    def getName(self):
        return self.n
    
    def getClass(self):
        return self.c
    
    def getDamage(self):
        return self.d
    
    def getRarity(self):
        return self.r
    
    def getMeta(self):
        return self.meta
    
    def setName(self,name):
        self.n = name
        
    def setClass(self,classification):
        self.c = classification
        
    def setDamage(self,damage):
        self.d = damage
        
    def setRarity(self,rarity):
        self.r = rarity
        
    def setEffects(self,meta):
        self.meta = meta
        
class Player:
    'Provides a simple class for making a player. Use meta to store metadata such as inventory'
    def __init__(self,name,max_health,defense=0,meta={}):
        self.n = name
        self.hp,self.mp = [int(max_health)]*2
        self.d = int(defense)
        self.meta = meta
        self.x = 0
        self.y = 0
        
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
    def __init__(self,universal_buffer):
        self.ubuf = universal_buffer
        self.log = []
        
    def log(self,line,importance=0):
        self.log.append(str(importance) + ' [' + time.time() + '] ' + line)
        
    def write(self):
        self.ubuf.writeLines(self.log)
        self.log = []
        
class Room:
    'Provides text adventure room class'
    def __init__(self,name,contents=[],meta={},doors={}):
        self.n = name
        self.c = contents
        self.meta = meta
        self.d = doors
        
    def moveOn(self,door_name):
        if door_name in self.d:
            return self.d[door_name]
        else:
            return 0
        
    def getContents(self):
        return self.c
    
    def setContents(self,contents):
        self.c = contents
        return 1
        
    def getName(self):
        return self.n
    
    def setName(self,name):
        self.n = name
        return 1
    
    def getMeta(self):
        return self.meta
    
    def setMeta(self,meta):
        self.meta = meta
        
    def enterRoom(self,return_meta=False):
        'Use: name, contents, doors[, meta] = Room.enterRoom()'
        if not return_meta:
            return self.n, self.c, self.d
        else:
            return self.n, self.c, self.d, self.meta