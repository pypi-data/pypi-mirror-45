%%cython 
cimport numpy as np
import numpy as np
from scipy.special import gamma, factorial
from numba import jit, vectorize, float64, int64

cimport libc.math as lm
import cython

from cython.parallel import parallel, prange

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)

cdef cluster_data(init_clust):
    """extract data values from cluster"""
    d = []
    cdef int init_len = len(init_clust)
    cdef int init_len2 
    
    if (init_len==7)&(isinstance(init_clust[3],list)):
        d.append(init_clust[3])
    else:
        for x in range(len(init_clust)):
            
            if isinstance(init_clust[x],tuple):
                init_len2 = len(init_clust[x])
                if (init_len2==7) & (isinstance(init_clust[x][3],list)):
                    d.append(init_clust[x][3])
                    
                elif isinstance(init_clust[x],tuple):
                    cluster_data(init_clust[x])
   
    e = [value for item in d for value in item] 
    return e

cdef prob_dk_pi(cluster1,cluster2,float alpha): 
    """
    This is a function to calculate the prior probabilities. 
    
    Inputs- 
    data: a list 
    alpha: the learning hyperparameter 
    """
    cdef int n_k, n1, n2
    cdef double d_k, pi, gamma_nk, d1, d2
    n1 = cluster1[4]
    n2 = cluster2[4]
    n_k = n1+n2
    
    gamma_nk = lm.tgamma(n_k)
    
    d1 = cluster1[6]
    d2 = cluster2[6]

    d_k = alpha * gamma_nk + d1*d2
    pi = alpha *  gamma_nk  / d_k
    
    return pi,d_k



cdef prob_dk_null_normal(cluster1, cluster2,float alpha0, float beta,float kappa, float mu): 
    """
    This function is to calculate probabilities under the null hypothesis. 
    
    Inputs: data, and hyperparameters for likelihood and conjugate priors.
    
    """
    cdef int n
    cdef float  beta_n, alpha_n, kappa_n, square, beta_1, beta_2, beta_3
    
    n = cluster1[4]+cluster2[4]
    x = cluster1[3]+cluster2[3]
    x_bar = np.mean(x)
    alpha_n = alpha0 + n/2
    
    cdef float ssr_x=0
    for i in range(len(x)):
        ssr_x +=lm.pow((x[i] - mu),2)
    
    beta_1=(1/2)*ssr_x
    beta_2=(kappa*n*lm.pow((x_bar - mu),2))
    beta_3=(2*(kappa + n)) 
    beta_n = beta  + beta_1 + (beta_2/beta_3)
    kappa_n = kappa + n 
    
    
    
    
    
    return (lm.tgamma(alpha_n)/lm.tgamma(alpha0)) * (lm.pow(beta,alpha0)/lm.pow(beta_n,alpha_n)) * (kappa/kappa_n)**(1/2) * (2*lm.M_PI)**(-n/2)



cdef prob_dl(cluster): 
    """
    This function is to calculate the marginal likelihood of data.
    
    Inputs: 
    data: a list 
    
    """
    cdef int n
    cdef float sigma, dl, x_bar
    cdef float ssr_x=0
    
    n = cluster[4]

    x = cluster[3]
    x_bar = np.sum(x)/n
    
    sigma = np.var(x)
    
    if sigma ==0:
        return 1
    else:
        
        
        for i in range(len(x)):
            ssr_x +=lm.pow((x[i] - x_bar),2)
        
        dl = (lm.pow((sigma),(-1/2))) * lm.exp((-ssr_x)/(2*sigma))
        return dl
    
cdef has_child(init_clust):
    """Function that returns True if the cluster has children"""
    if isinstance(init_clust[1],tuple):
        return True
    return False

cdef kids(init_clust):
    """Function to return the cluster numbers of the children"""
    
    z = (init_clust[1],init_clust[2])
    return z

cdef check_cluster(clust_list, int c_num):
    """This functions pulls the requested cluster from the hierarchy"""
    y=()
    cdef int x0
    for x in clust_list:
        x0 = x[0]
        if x0==c_num:
            return x
        elif has_child(x)==False:
            continue
        else:
            y = y+(kids(x)[0], kids(x)[1])
            continue
    return check_cluster(y,c_num)

cdef partition(clust_list,c,dl, m=[]):
    """This function enumerates all partitions of the given clusters"""
    
    cdef float dl_prod, gamma_n
    
    cdef int y, z_len
    
    cdef int c_len = len(c)
    
    ma = (sorted(c),c_len)

    if ma not in m:
        dl_prod = 1
        gamma_n = 1
        for i in range(c_len):
            dl_prod = dl_prod*dl[c[i]-1]
            gamma_n = gamma_n*lm.tgamma(check_cluster(clust_list,c[i])[4])
        dz = (sorted(c),c_len,gamma_n, dl_prod)
        
        m.append(dz)
    
    
    for i in range(c_len):

        z=c
     
       
        y = z[i]
     
        new_clus =check_cluster(clust_list,y)
        
        if has_child(new_clus):    
            v = kids(new_clus)
            
            z = (z[:i]+z[i+1:]+[v[0][0]]+[v[1][0]])


            z_len = len(z)
            for p in range(z_len):
                if i==p:
                    partition(clust_list,z,dl)               
    return m
    

cdef p_d_t (init_clust,float alpha,dl):
    """this functions calculates the probability of the data given the tree"""
    cdef float mv, gamma_mv, p_dl, d, d_t
    
    if has_child(init_clust)==False:
        return 1
    
    d_t = 0
    clust_list = [init_clust[1],init_clust[2]]
    c= [init_clust[1][0], init_clust[2][0]]

    V = partition(clust_list,c,dl,m=[])
    
    
    for i in range(len(V)):
        mv = V[i][1]
        gamma_mv = V[i][2]
        
        p_dl = V[i][3]
        d = init_clust[6]
           
        d_t += ((lm.pow(alpha,mv)*gamma_mv)/d)*p_dl
    
            
    return d_t

cdef p_dt_ij(clust_i,clust_j, float alpha,dl):
    """This function calculates the probability of data from i and data from j given the tree structure for both."""
    
    cdef float pi_pj_dk, p_i, p_j, pk, dk
    p_i = p_d_t(clust_i, alpha,dl)
    p_j = p_d_t(clust_j, alpha,dl)
    pk, dk = prob_dk_pi(clust_i, clust_j, alpha)
    pi_pj_dk=(p_i*p_j)/dk
    return pi_pj_dk

cdef r_k(cluster1, cluster2,  float alpha, float alpha0, float beta, float  kappa, float  mu, dl):
    """calculate probability of the merged hypothesis"""
    
    cdef float pi, d_k, dh_k, dt_k, r_k
    
    pi, d_k = prob_dk_pi(cluster1,cluster2,alpha)
    dh_k = prob_dk_null_normal(cluster1, cluster2, alpha0,beta,kappa,mu)
    dt_k = p_dt_ij(cluster1, cluster2, alpha,dl)
    r_k = (pi*dh_k)/dt_k
    
    return r_k

cdef find_cluster_merge(init_clust, float alpha,float alpha0,float  beta,float  kappa,float  mu,dl,int  c = 0):
    """function to merge all clusters into one"""
    cdef int clust_len = len(init_clust)
    cdef float p, pk, dk
    
    if c == 0:
        c = clust_len+1
    
    if clust_len==1:
        return init_clust
    
    max_p = 0
    
    merge_a = init_clust[0]
    merge_b = init_clust[1]
    
    for i in range(clust_len):
        for j in range(clust_len):
            if j>i:
                p=r_k(init_clust[i], init_clust[j],alpha,alpha0, beta, kappa, mu,dl)
                if p> max_p:
                    max_p = p
                    merge_a = init_clust[i]
                    merge_b = init_clust[j]
                    
    init_clust.remove(merge_a)
    init_clust.remove(merge_b)
    values = cluster_data(merge_a) + cluster_data(merge_b)
    nk = merge_a[4]+merge_b[4]
    pk, dk = prob_dk_pi(merge_a, merge_b, alpha)

    merge_clust = (c, merge_a, merge_b,values, nk, pk,dk )
    
    dl.append(prob_dl(merge_clust))
    
    c +=1
    
    init_clust.append(merge_clust)

    if len(init_clust)>1:
        return find_cluster_merge(init_clust, alpha,alpha0, beta, kappa, mu,dl, c)
    
    else:
        return init_clust

def bayes_hier_clust(data_vec, float alpha,float alpha0,float  beta,float  kappa,float  mu):
    """Main clustering function that formats the data and produces the cluster structure"""
    
    cdef int n

    value = data_vec
    c_num = tuple(i for i in range(1,len(value)+1))
    n = len(value)
    n_k = [1] * n
    d_k = [alpha] * n
    p_k = [1] * n
    left = [0] * n
    right = [0] * n
    dl=[1]*n

    init_clust = list(zip(c_num,left,right,value,n_k,p_k,d_k))

    return find_cluster_merge(init_clust, alpha,alpha0,  beta,  kappa,  mu,dl)
    
    
    
    