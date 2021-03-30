from time import time

class CoolDown:
    def __init__(self, rate):
        self.cooling = {}
        self.rate = rate
    
    def add(self, id):
        self.cooling[id] = time() + self.rate
    def check(self, id):
        if id not in self.cooling.keys():
            return False
            
        elif self.cooling[id] < time():
            del self.cooling[id]
            return False
    
        else:
            return True
    
    def retry_after(self, id):
        resp = self.cooling[id] - time()
        return resp
    
    