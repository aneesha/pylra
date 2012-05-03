'''
Created on May 3, 2012

@author: samindaw
'''
import os.path
import pickle

class PersistanceManager:
    def __init__(self, cache_file):
        self.cache_file=cache_file
        self.cache=None
        
    def load_cache(self):
        global cache
        if os.path.exists(self.cache_file):
            f=open(self.cache_file,"r")
            self.cache=pickle.load(f)
            f.close()
        else:
            self.cache={}
        return True
    
    def get_cache(self):
        if (not self.cache):
            self.load_cache()
        return self.cache
    
    def save_cache(self):
        if (self.cache):
            f=open(self.cache_file,"wb")
            pickle.dump(self.cache, f)
        return True
    
    def get_from_cache(self,key):
        c=self.get_cache()
        if (c and key in c.keys()):
            return c[key]
        else:
            return None
        
    def update_cache(self,key,data):
        self.get_cache()[key]=data
        self.save_cache()
