'''
Created on Apr 19, 2012

@author: samindaw
'''
from xgoogle.search import GoogleSearch
import nltk
import re
from persistence import PersistanceManager

cache_file="lra_step2_cache.txt"

def is_garbage(word):
    return word=="\xc2\xb7"

def filter_garbage(words):
    return [word for word in words if not is_garbage(word)]
    
class SearchCorpus:
    """
        An abstract class to do the searching of word pairs in a corpus
        Users should not instantiate this class. Instead use child
        classes of this class.
    """
    cache_manager=PersistanceManager(cache_file)
    
    def search_pairs_cache(self,wordpair):
        return self.cache_manager.get_from_cache((wordpair,"search_pair"))
    
    def search_pairs_cache_save(self,wordpair, data):
        return self.cache_manager.update_cache((wordpair,"search_pair"),data)
    
    def get_occurances(self, wordpair):
        #Child class must implement this
        pass
    
    def get_patterns(self,word_list):
        patterns=[]
        if (len(word_list)>0):
            sub_patterns = self.get_patterns(word_list[1:])
            if (len(sub_patterns)>0):
                patterns.extend([[word_list[0]]+p for p in sub_patterns])
                patterns.extend([["*"]+p for p in sub_patterns])
            else:
                patterns.append([word_list[0]])
                patterns.append(["*"])
        return patterns
            
    
    def search_pairs(self, wordpair,use_cache=True, phrase_size=None):
        """
            search & return frequencies of different word patterns of 
            which the word pairs occur in the corpus
        """
        if (self.enable_caching and use_cache):
            search_pairs_v=self.search_pairs_cache(wordpair)
            if (search_pairs_v):
                return search_pairs_v
        #get the occurances in the corpus
        occurances=self.get_occurances(wordpair,use_cache=use_cache)
        
        #remove occurances larger than a given window of words
        if (phrase_size):
            occurances=[occurance for occurance in occurances if len(occurance)<=phrase_size]
        
        #extract all possible patterns using wild cards
        patterns=[]
        for occurance in occurances:
            word_set=occurance
            inside_w=word_set[1:-1]
            patterns.extend(self.get_patterns(inside_w))
        #remove duplicates
        [patterns.remove(p) for p in list(patterns) if patterns.count(p)>1]
        
        #count the frequency of each pattern occurring
        pattern_count=[]
        for pattern in patterns:
            matches=0
            for occurance in occurances:
                o=occurance[1:-1]
                if (len(o)==len(pattern)):
                    found=True
                    for i in range(len(pattern)):
                        if (pattern[i]!="*" and pattern[i]!=o[i]):
                            found=False
                            break;
                    if found:
                        matches+=1
            pattern_count.append((tuple(pattern),matches))
        
        #sort in desc the pattern list by frequency of each pattern occurrence in the corpus
        pattern_count=list(reversed(sorted(pattern_count,key=lambda x:x[1])))
        if self.enable_caching:
            self.search_pairs_cache_save(wordpair, pattern_count)
        return pattern_count;

class GoogleSearchCorpus(SearchCorpus):
    """
        Google as a corpus of search base 
    """
    def __init__(self,enable_caching=True):
        self.gs=GoogleSearch(None)
        self.enable_caching=enable_caching
    
    def get_occurances_cache(self, wordpair):
        return self.cache_manager.get_from_cache((wordpair,"get_occurances"))
    
    def get_occurances_save(self, wordpair,data):
        self.cache_manager.update_cache((wordpair,"get_occurances"), data)
        
    def get_occurances(self, wordpair, use_cache=True):
        if (self.enable_caching and use_cache):
            c=self.get_occurances_cache(wordpair)
            if c:
                return c
        w1=wordpair[0].lower()
        w2=wordpair[1].lower()
        
        #define the search query
        self.gs.query=w1+" * "+w2
        allresults=[]
        results=self.gs.get_results()
        
        #until there is no more results keep query the search engine
        while (len(results)>0):
            allresults.extend(results)
            results=self.gs.get_results()
        
        #among the results search for the word pair phrases
        phrases=[]
        [phrases.extend(re.findall(r""+w1+" .*? "+w2+"",result.desc.encode('utf8').lower())) for result in allresults]
        phrases=[filter_garbage(phrase.split()) for phrase in phrases]
        if self.enable_caching:
            self.get_occurances_save(wordpair, phrases)
        return phrases

class FileSearchCorpus(SearchCorpus):
    """
        File as a corpus of search base 
    """
    
    #keep track of all the files opened as a corpus
    #in order to avoid reopening them
    CORPUS={}
        
    def get_corpus(self):
        if not self.filename in self.CORPUS.keys(): self.CORPUS[self.filename]=nltk.data.load("file:"+self.filename, format="raw", cache=False)[:self.limit].lower().split()
        return self.CORPUS[self.filename]

    def __init__(self,filename=None, limit=None, enable_caching=True):
        self.filename=filename
        self.limit=limit
        self.enable_caching=enable_caching
    
    def get_occurances_cache(self, wordpair):
        return self.cache_manager.get_from_cache((wordpair,"get_occurances"))
    
    def get_occurances_save(self, wordpair,data):
        self.cache_manager.update_cache((wordpair,"get_occurances"), data)
        
    def get_occurances(self, wordpair, use_cache=True):
        if (self.enable_caching and use_cache):
            c=self.get_occurances_cache(wordpair)
            if c:
                return c
        #TODO
        #corpus=self.get_corpus()
