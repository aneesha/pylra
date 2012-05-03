from nltk.corpus import wordnet as wn

def get_synonyms(word):
    """
        Given a word return all possible synonyms for that word
    """
    #TODO filter-out unrealistic synonyms
    synsets=wn.synsets(word) #@UndefinedVariable
    l=[]
    for s in synsets:
        if s.name.find(word)>=0: print str(s.lemma_names)
    [[l.append(synonym) for synonym in synset.lemma_names] for synset in synsets]
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
        Unit tests for LRA Step1
    """
    print get_synonyms("cat")

def main():
    run_test()
        
if __name__ == "__main__":
    main()
        