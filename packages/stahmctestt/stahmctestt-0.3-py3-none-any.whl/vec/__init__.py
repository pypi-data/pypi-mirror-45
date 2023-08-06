
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from numba import jit, vectorize, float64, int64



# In[2]:


@jit(cache=True)
def hmc_nbvec(gradlogistic,X,y,theta0,M,C,epsilon,batchsize=50,iter=1000):
    """
    This function outputs the p dimiension Hamilton Monte Carlo samples without M-H correction.    
    Args: 
        X:n.p-2d array
        y n.1-1d array
        theta0: the initial point of theta, the parameter of interest
        grad: the gradient of the potential
        M: the mass
        C: the C term, where C*M^{-1} is the friction
        epsilon: stepsize
        p: the dimension of theta
        batchsize: the number of minibatch used
        iter: iteration number, 1000 by default
    """
    n=y.size
    p=theta0.shape[0]
    r=np.random.multivariate_normal(np.zeros(p),M)
    theta=theta0
    theta_save=np.zeros([iter,p])
    r_save=np.zeros([iter,p])
    for t in range(iter):    
        mr=np.linalg.solve(M,r)
        theta=theta+epsilon*mr
        batch=np.random.choice(n,batchsize,replace=False)
        r=r-gradlogistic(theta,X[batch,:],y[batch])*epsilon-epsilon*np.dot(C,mr)+np.random.multivariate_normal(np.zeros(p),2*epsilon*C,1).ravel()
        theta_save[t,:]=theta
        r_save[t,:]=r
    return np.c_[theta_save,r_save]






