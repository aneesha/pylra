'''
Created on May 3, 2012

@author: samindaw
'''

from lra_step1 import get_similar_pairs
from lra_step2 import get_pattern_frequencies_matrix
from lra_step3 import get_svd_from_frequency_matrix
from lra_step4 import get_projection_matrix, \
    calculate_word_pair_cosine_vector_matrix
from lra_step5 import calculate_average_similarity

def calculate_latent_relational_similarity(word_pair1,word_pair2):
    """
        calculate analogical similarity between 2 word pairs using
        latent relational similarity calculations 
    """
    #build the alternative pairs
    set1=list(set([word_pair1]+get_similar_pairs(word_pair1)))
    set2=list(set([word_pair2]+get_similar_pairs(word_pair2)))
    
    word_pairs=set1+set2
    
    #generate sparse matrix
    pattern_matrix=get_pattern_frequencies_matrix(word_pairs)
    
    #factor the pattern frequency matrix using SVD
    u, z, v=get_svd_from_frequency_matrix(pattern_matrix)
    
    #derive the projection matrix
    projection_matrix=get_projection_matrix(u, z, v)
    
    #calculate the cosine vector matrix for the word pairs
    word_pair_cosine_vector=calculate_word_pair_cosine_vector_matrix(projection_matrix,word_pairs)
    
    #return the average cosine value for a given 2 word pair sets
    return calculate_average_similarity(set1,set2,word_pair_cosine_vector)

def run_tests():
    import lra_step1
    import lra_step2
    import lra_step3
    import lra_step4
    import lra_step5
    lra_step1.run_test()
    lra_step2.run_test()
    lra_step3.run_test()
    lra_step4.run_test()
    lra_step5.run_test()          
    
def main():
    run_tests()
    
if __name__ == "__main__":
    main()    