'''
Created on Apr 19, 2012

@author: samindaw
'''

from SearchCorpus import GoogleSearchCorpus

MAX_PHRASE=5
MAX_PATTERNS=4000

def get_pair_occurance_pattern_frequency(word_pair, phrase_size=MAX_PHRASE, max_patterns=MAX_PATTERNS):
    """
        return a frequency vector for word patterns possible for the given word pair
    """
    #here we are using google to search for word pair occurances
    gsc=GoogleSearchCorpus()
    pattern_vector={}
    
    #whats returned from teh search corpus is a set of tuples (pattern,frequency). convert
    #it to a dictionary of pattern:frequency 
    [pattern_vector.setdefault(pattern[0],pattern[1]) for pattern in gsc.search_pairs(word_pair,phrase_size)[:max_patterns]]
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
    print get_pattern_frequencies_matrix(("cat","dog"),max_patterns=10)

def main():
    run_test()
    
if __name__ == "__main__":
    main()