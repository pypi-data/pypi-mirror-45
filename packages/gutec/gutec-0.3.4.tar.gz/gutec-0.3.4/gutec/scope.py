class gScope:
    
    def __init__(self):
        self.ids = {}

    # ID attributes: name, type, isInitialized?, isUsed?, line_number
    def new_id(self, name, type_, line_num):
        self.ids[name] = (type_, False, False,line_num)

    def getLineNum(self,name):
        return self.ids[name][3]

    def checkExists(self, name):
        if bool(self.ids):
            return name in self.ids.keys()
        return False

    def checkType(self, name):
        if bool(self.ids):
            return self.ids[name][0]
        return False

    def checkInit(self, name):
        if bool(self.ids):
            return self.ids[name][1]
        return False

    def checkUsed(self, name):
        if bool(self.ids):
            return self.ids[name][2]
        return False

    def init(self, name):
        update_var = (self.ids[name][0], True, self.ids[name][2],  self.ids[name][3])
        del self.ids[name]
        self.ids[name] = update_var

    def used(self, name):
        update_var = (self.ids[name][0], True,self.ids[name][2],  self.ids[name][3])
        del self.ids[name]
        self.ids[name] = update_var

    def getIDs(self):
        return self.ids

    def __repr__(self):
        s = ""
        for k, v in self.ids.items():
            s+= f'{k}:{v}\n'

        return s

    def _print(self):
        print(self.ids.items())
        
