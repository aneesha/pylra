from nltk.corpus import wordnet as wn

"""

Synonyms and Similar 


"""

def get_synonyms(word):
    """
        Given a word return all possible synonyms for that word
    """
    #TODO filter-out unrealistic synonyms
    synsets=wn.synsets(word) #@UndefinedVariable
    l=[]
    [[l.append(synonym) for synonym in synset.lemma_names] for synset in synsets if synset.name.find(word)>=0]
    #remove duplicates
    return set(l)

def get_similar_pairs(word_pair):
    """
        given a word pair generate alternative pairs
    """
    set1=get_synonyms(word_pair[0])
    set2=get_synonyms(word_pair[1])
    return list(set([(s1,s2) for s1 in set1 for s2 in set2]))
    
def run_test():
    """
        Unit tests for LRA Step 1
    """
    print
    print "Unit tests - LRA Step 1"
    print "======================="
    print
    
    word1="dog"
    print "Synonyms for "+word1+" : "
    print "\t"+str(get_synonyms(word1))
    print
    
    word2="work"
    print "Similar pairs for '"+word2+"' & '"+word1+"'"
    for pair in get_similar_pairs((word2,word1)): print "\t"+str(pair)
    print

def main():
    run_test()
    
        
if __name__ == "__main__":
    main()
        