from datetime import datetime

class Task():
    def __init__(self,name=None) -> None:
        self.task_name = name # type: str
        self.start_time = self.get_current_time() # type: datetime
        self.complete_time = None # type: datetime
        self.description = None # type: str
        self.stats = None # type: str
        self.tags = [] # type: list
        self.children = [] # type: list
        self.setStats('start')


    def get_current_time(self):
        return datetime.now()
    
    def setEndTime(self):
        self.complete_time = self.get_current_time()
    
    def setdescription(self,description):
        self.description = description
    
    def addTag(self,tag):
        self.tags.append(tag)
    
    def addTags(self,tags):
        self.tags.extend(tags)
    
    def getTags(self):
        return self.tags
    
    def addChild(self,child):
        self.children.append(child)
    
    def removeChild(self,child):
        self.children.remove(child)

    def getChildren(self):
        return self.children
    
    def setName(self,name):
        self.task_name = name
    def getName(self):
        return self.task_name

    def updatetime(self, type, time):
        if type == 'start':
            self.start_time = time
        elif type == 'end':
            self.complete_time = time

    def setStats(self,stats):
        if self.judgeStats(stats):
            self.stats = stats

    def judgeStats(self, stats):
        #stats have these alues: start, complete, waiver
        #need judge if the stats is included in these values
        if stats in ['start', 'complete', 'waiver']:
            return True
        else:
            return False
    
    def getStats(self):
        return self.stats