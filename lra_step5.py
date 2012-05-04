'''
Created on May 3, 2012

@author: samindaw
'''

def calculate_average_similarity(word_pair1_list, word_pair2_list, word_pair_cosine_vector):
    """
        calcuate the average similarity between 2 sets of word pairs using a cosine vector 
        matrix assuming the 1st word pair in each set is the original word pair
    """
    base_value=word_pair_cosine_vector[word_pair1_list[0]][word_pair2_list[0]]
    cosines=[word_pair_cosine_vector[wp1][wp2] for wp1 in word_pair1_list for wp2 in word_pair2_list if word_pair_cosine_vector[wp1][wp2]>=base_value]
    return sum(cosines)/(1.0*len(cosines))

def run_test():
    """
        Unit tests for LRA Step 5
    """
    global ENABLE_CACHING
    ENABLE_CACHING=False
    print
    print "Unit tests - LRA Step 5"
    print "======================="
    print
    frequency_mat={("work", "dog"):{("the"):10,("like","a"):8,("like","*"):12,("*","a"):16,("*"):14},
                   ("office", "hound"):{("the"):10,("like","a"):8,("like","*"):12,("*","a"):16,("*"):14}}
    import lra_step3
    u,z,v=lra_step3.get_svd_from_frequency_matrix(frequency_mat)
    import lra_step4    
    projection_matrix=lra_step4.get_projection_matrix(u, z, v)
    cosine_vec_mat=lra_step4.calculate_word_pair_cosine_vector_matrix(projection_matrix,frequency_mat.keys())
    wp1=[frequency_mat.keys()[0]]
    wp2=[frequency_mat.keys()[1]]
    print "Average relational semantic similarity between "+str(wp1)+" & "+str(wp2)+" : "+str(calculate_average_similarity(wp1, wp2, cosine_vec_mat))

def main():
    run_test()
    
if __name__ == "__main__":
    main()     