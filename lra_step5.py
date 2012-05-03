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