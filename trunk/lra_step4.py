'''
Created on May 3, 2012

@author: samindaw
'''
from scipy import mat,transpose;
import numpy

TOP_NUM_SINGULAR_VALUES=300

def get_top_k_column_indexes(zigma_matrix,k=TOP_NUM_SINGULAR_VALUES):
    """
        look at the zigma matrix diagnal values for best k number of 
        singular values & record the column indexes
    """
    l=[]
    [l.append((i,zigma_matrix[i])) for i in range(len(zigma_matrix))]
    return [v[0] for v in list(reversed(sorted(l, key=lambda x:x[1])))[:k]]  

def get_projection_matrix(u,z,v,k=TOP_NUM_SINGULAR_VALUES):
    """
        generate the projection matrix which contains a 
        score vector for the patterns for each word pair 
    """ 
    #determine the best patterns for comparison   
    column_indexes=get_top_k_column_indexes(z)
    
    #using the column indexes of the best patterns recreate the 
    #u & z matrices containing only those correspoding columns
    
    #creating the uk matrix
    uk=[]
    for r in range(len(u)):
        uk.append([])
        for index in column_indexes:
            uk[r].append(u[r][index])
        r+=1

    #creating the zk matrix
    zk=[]
    for index in column_indexes:
        zk.append([])
        for col in range(len(v)):
            if (col==index):
                zk[len(zk)-1].append(z[index])
            else: 
                zk[len(zk)-1].append(0)
    
    #calcualte the projecttion matrix by u.z
    return mat(uk)*mat(zk)

def get_cosine_vector_matrix(projection_mat):
    """
        Calculate the cosine matrix for a given projection matrix
    """
    return projection_mat*transpose(projection_mat)

def get_word_pair_cosine_vector_matrix(cosine_vector,word_pairs):
    """
        match the word pairs to the cosine vector matrix and return a cosine 
        vector matrix having the word pairs as rows
    """
    cosine_vector=numpy.squeeze(numpy.asarray(cosine_vector))
    result={}
    for row in range(len(cosine_vector)):
        result[word_pairs[row]]={}
        for col in range(len(cosine_vector[row])):
            result[word_pairs[row]][word_pairs[col]]=cosine_vector[row][col]
    
    return result

def calculate_word_pair_cosine_vector_matrix(projection_mat,word_pairs):
    """
        calculate the word pair cosine vector matrix from the projection matrix
    """
    return get_word_pair_cosine_vector_matrix(get_cosine_vector_matrix(projection_mat),word_pairs)

def run_test():
    """
        Unit tests for LRA Step 4
    """
    print
    print "Unit tests - LRA Step 4"
    print "======================="
    print
    frequency_mat={("work", "dog"):{("the"):10,("like","a"):8,("like","*"):12,("*","a"):16,("*"):14},
                   ("office", "hound"):{("the"):10,("like","a"):8,("like","*"):12,("*","a"):16,("*"):14}}
    import lra_step3
    u,z,v=lra_step3.get_svd_from_frequency_matrix(frequency_mat)    
    print "SVD values"
    print "\t U = "+str(u)
    print "\t Z = "+str(z)
    print "\t V = "+str(v)
    print
    projection_matrix=get_projection_matrix(u, z, v)
    print "Projection matrix"
    for row in projection_matrix: print "\t"+str(row)
    
    print
    cosine_vec_mat=calculate_word_pair_cosine_vector_matrix(projection_matrix,frequency_mat.keys())
    print "Word pair cosine matrix"
    for pair,features in cosine_vec_mat.items(): print "\t"+str(pair)+":"+str(features)

def main():
    run_test()
    
if __name__ == "__main__":
    main()