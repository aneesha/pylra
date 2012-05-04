'''
Created on Apr 19, 2012

@author: samindaw
'''

from search_corpus import GoogleSearchCorpus

MAX_PHRASE=5
MAX_PATTERNS=4000
ENABLE_CACHING=True
def get_pair_occurance_pattern_frequency(word_pair, phrase_size=MAX_PHRASE, max_patterns=MAX_PATTERNS):
    """
        return a frequency vector for word patterns possible for the given word pair
    """
    global ENABLE_CACHING
    #here we are using google to search for word pair occurances
    gsc=GoogleSearchCorpus(enable_caching=ENABLE_CACHING)
    pattern_vector={}
    
    #whats returned from teh search corpus is a set of tuples (pattern,frequency). convert
    #it to a dictionary of pattern:frequency 
    [pattern_vector.setdefault(pattern[0],pattern[1]) for pattern in gsc.search_pairs(word_pair,phrase_size=phrase_size)[:max_patterns]]
    return pattern_vector

def get_pattern_frequencies_matrix(word_pairs,phrase_size=MAX_PHRASE, max_patterns=MAX_PATTERNS):
    """
        Return a pattern frequency matrix for the given set of word_pairs
    """
    pattern_matrix={}
    for word_pair in word_pairs:
        pattern_matrix[word_pair]=get_pair_occurance_pattern_frequency(word_pair,phrase_size,max_patterns)
        #reverse pair
        #pattern_matrix[(word_pair[1],word_pair[0])]=pattern_matrix[word_pair]
    return pattern_matrix

def run_test():
    """
        Unit tests for LRA Step 2
    """
    global ENABLE_CACHING
    ENABLE_CACHING=False
    print
    print "Unit tests - LRA Step 2"
    print "======================="
    print
    word_pair = ("work", "dog")
    print "Pattern frequencies for word pair : "+str(word_pair)
    for pair,value in get_pattern_frequencies_matrix([word_pair],max_patterns=10).items():
        print "\t"+str(pair) 
        for pattern,f in value.items():
            print "\t\t"+str(pattern)+":"+str(f)

def main():
    run_test()
    
if __name__ == "__main__":
    main()