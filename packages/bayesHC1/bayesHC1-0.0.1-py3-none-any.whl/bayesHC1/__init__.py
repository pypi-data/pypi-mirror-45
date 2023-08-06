#Import necessary libraries
import numpy as np 
from scipy.special import gamma, factorial
from numba import jit, vectorize, float64, int64

def cluster_data_orig(init_clust):
    """
        This function will extract all the data for the given cluster

        Input is the cluster tuple.
    
    """
    d = [] #initialize data container
    if (len(init_clust)==7)&(isinstance(init_clust[3],list)):
        d.append(init_clust[3]) #if init_clust is a cluster, extract the data and append to the data container
    else:
        for x in init_clust:
            
            if isinstance(x,tuple): #search next level for cluster data
                if (len(x)==7) & (isinstance(x[3],list)):
                    d.append(x[3])
                    
                elif isinstance(x,tuple): #recursive to reach all branches of the tree
                    cluster_data_orig(x)
   
    e = [value for item in d for value in item]
    return e

def prob_dk_pi_orig(cluster1,cluster2,alpha): 
    """
    This is a function to calculate the prior probabilities. 
    
    Inputs- 
    data: a list 
    alpha: the learning hyperparameter 
    """
    n_k = cluster1[4]+cluster2[4]
    d_k = alpha * gamma(n_k) + cluster1[6]*cluster2[6]
    pi = alpha *  gamma(n_k)  / d_k
    
    return pi,d_k

def prob_dk_null_normal_orig(cluster1, cluster2, alpha0,beta,kappa,mu): 
    """
    This function is to calculate probabilities under the null hypothesis. 
    
    Inputs: data, and hyperparameters for likelihood and conjugate priors.
    
    """
    
    n = cluster1[4]+cluster2[4]
    x = cluster1[3]+cluster2[3]
    x_bar = np.mean(x)
    alpha_n = alpha0 + n/2
    beta_n = beta + 1/2*np.sum((x -  x_bar)**2) + (kappa*n*(x_bar - mu)**2)/(2*(kappa + n)) 
    kappa_n = kappa + n 
    
    return (gamma(alpha_n)/gamma(alpha0)) * (beta**alpha0/beta_n**alpha_n) * (kappa/kappa_n)**(1/2) * (2*np.pi)**(-n/2)

def prob_dl_orig(cluster): 
    """
    This function is to calculate the marginal likelihood of data.
    
    Inputs: 
    data: a list 
    
    """
    n = cluster[4]
    x = np.array(cluster[3])
    x_bar = np.repeat(np.mean(x),n)
    sigma = np.var(x)
    
    if sigma ==0:
        return 1
    else:
        return (sigma)**(-1/2) * np.exp(-sum((x - x_bar)**2)/(2*sigma))


    
def has_child_orig(init_clust):
    """Function that returns True if the cluster has children"""
    if isinstance(init_clust[1],tuple):
        return True
    return False

def kids_orig(init_clust):
    """Function to return the cluster numbers of the children"""
    z = (init_clust[1],init_clust[2])
    return z

def check_cluster_orig(clust_list,c_num):
    """This functions pulls the requested cluster from the hierarchy"""
    y=()
    for x in clust_list:
        if x[0]==c_num:
            return x
        elif has_child_orig(x)==False:
            continue
        else:
            y = y+(kids_orig(x)[0], kids_orig(x)[1])
            continue
    return check_cluster_orig(y,c_num)

def partition_orig(clust_list,c, m=[]):
    """This function enumerates all partitions of the given clusters"""
    ma = (sorted(c),len(c))
    if ma not in m: #check if list of tree consistent clusters is already recorded
        m.append(ma)

    #enumerate through all possible combinations of cluster kids
    for i in range(len(c)): 

        z=c

        y = z[i]

        new_clus =check_cluster_orig(clust_list,y)
        if has_child_orig(new_clus):
            
            v = kids_orig(new_clus)
            
            z = z[:i]+z[i+1:]+((v)[0][0],v[1][0])

            for p in range((len(z))):
                if i==p:
                    partition_orig(clust_list,z)
    return m

def p_d_t_orig (init_clust, alpha):
    """this functions calculates the probability of the data given the tree"""
    if has_child_orig(init_clust)==False: #return 1 if there is only one member in the cluster
        return 1
    
    d_t = 0
    clust_list = (init_clust[1],init_clust[2])
    c= (init_clust[1][0], init_clust[2][0])
    V = partition_orig(clust_list,c,m=[])
    for i in range(len(V)):
        mv = V[i] [1]
        gamma_mv=1
        p_dl = 1
        for x in V[i][0]:

            sub_clust = check_cluster_orig(clust_list,x)
            gamma_mv = gamma_mv*gamma(sub_clust[4])
            p_dl = p_dl * prob_dl_orig(sub_clust)
        d = init_clust[6]
        d_t += (((alpha**mv)*gamma_mv)/d)*p_dl
    
            
    return d_t

def p_dt_ij_orig(clust_i,clust_j,alpha):
    """This function calculates the probability of data from i and data from j given the tree structure for both."""
    p_i = p_d_t_orig(clust_i, alpha)
    p_j = p_d_t_orig(clust_j, alpha)
    pk, dk = prob_dk_pi_orig(clust_i, clust_j, alpha)
    return (p_i*p_j)/dk

def r_k_orig(cluster1, cluster2, alpha,alpha0, beta, kappa, mu):
    """calculate probability of the merged hypothesis"""
    
    
    pi, d_k = prob_dk_pi_orig(cluster1,cluster2,alpha)
    dh_k = prob_dk_null_normal_orig(cluster1, cluster2, alpha0,beta,kappa,mu)
    dt_k = p_dt_ij_orig(cluster1, cluster2, alpha)
    r_k = (pi*dh_k)/dt_k
    
    return r_k

def find_cluster_merge_orig(init_clust, alpha,alpha0, beta, kappa, mu, c):
    """function to merge all clusters into one"""
    
    if len(init_clust)==1:
        return init_clust
    
    max_p = 0
    
    merge_a = init_clust[0]
    merge_b = init_clust[1]

    for i in range(len(init_clust)):
        for j in range(len(init_clust)):
            if j>i:
                p=r_k_orig(init_clust[i], init_clust[j],alpha,alpha0, beta, kappa, mu)
                if p> max_p:
                    max_p = p
                    merge_a = init_clust[i]
                    merge_b = init_clust[j]
    init_clust.remove(merge_a)
    init_clust.remove(merge_b)
    values = cluster_data_orig(merge_a) + cluster_data_orig(merge_b)
    nk = merge_a[4]+merge_b[4]
    dk = 0.5

    merge_clust = (c, merge_a, merge_b,values, nk, max_p,dk)
    c +=1
    
    init_clust.append(merge_clust)

    if len(init_clust)>1:
        return find_cluster_merge_orig(init_clust, alpha,alpha0, beta, kappa, mu, c)
    else:
        return init_clust
    
    
def bayes_hier_clust_orig(data_vec,  alpha,alpha0,  beta,  kappa,  mu):
    """Main clustering function that formats the data and produces the cluster structure"""

    
    value = data_vec
    c_num = tuple(i for i in range(1,len(value)+1))
    n = len(value)
    n_k = [1] * n
    d_k = [alpha] * n
    p_k = [1] * n
    left = [0] * n
    right = [0] * n

    init_clust = list(zip(c_num,left,right,value,n_k,p_k,d_k))


    c = (len(init_clust)+1)

    return find_cluster_merge_orig(init_clust, alpha,alpha0,  beta,  kappa,  mu,c)
    