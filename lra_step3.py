'''
Created on May 3, 2012

@author: samindaw
'''
import math
from scipy import linalg, mat;

def get_probability_matrix(frequency_matrix):
    """
        normalize the each pattern (calculate probability of 
        each pattern for a word pair)
    """
    p={}
    total={}
    for row in frequency_matrix.keys():
        p[row]={}
        for pattern,frequency in frequency_matrix[row].items():
            if (not pattern in total.keys()):
                total[pattern]=sum([frequency_matrix[r].get(pattern,0) for r in frequency_matrix.keys()])
            p[row][pattern]=frequency/(1.0*total[pattern])
    return p

def get_entropy_vector(probability_matrix):
    """
        calculate pattern entropy of each pattern with the use 
        of probabilities of each pattern for given word pair 
    """
    entropy={}
    for row in probability_matrix.keys():
        for pattern in probability_matrix[row].keys():
            if (not pattern in entropy.keys()):
                sum([p*math.log(p)for p in [probability_matrix[r].get(pattern,0) for r in probability_matrix.keys()]])
    return entropy

def get_weight_vector(entropy_vector, num_rows):
    """
        calculate the weight for each pattern using the 
        pattern entropy
    """
    r_val=math.log(num_rows)
    weight_vector={}
    [weight_vector.setdefault(pattern,1-(entropy/r_val)) for pattern,entropy in entropy_vector.items()]
    return weight_vector

def update_to_log_frequency(frequency_matrix, weight_vector):
    """
        update the pattern frequency matrix with the 
        corresponding weighted log frequency values
    """
    for row,patterns in frequency_matrix.items():
        for pattern in patterns:
            frequency_matrix[row][pattern]=weight_vector[pattern]*math.log(frequency_matrix[row][pattern]+1)
    return frequency_matrix

def apply_svd(log_frequency_matrix,patterns):
    """
        factor the frequency matrix in to 3 matrices using 
        singular value decomposition method (SVD) 
    """
    matrix=mat([[log_frequency_matrix[row].get(pattern,0) for pattern in patterns] for row in log_frequency_matrix.keys()])
    u, z, v = linalg.svd(matrix)
    return u, z, v 
    
def get_svd_from_frequency_matrix(frequency_matrix):
    """
        for a given frequency matrix return SVD factor matrices
    """
    prob_matrix = get_probability_matrix(frequency_matrix)
    entropy_vector = get_entropy_vector(prob_matrix)
    weight_vector = get_weight_vector(entropy_vector, len(prob_matrix.keys()))
    log_frequency_matrix=update_to_log_frequency(frequency_matrix, weight_vector)
    return apply_svd(log_frequency_matrix, weight_vector.keys())
    
    
    