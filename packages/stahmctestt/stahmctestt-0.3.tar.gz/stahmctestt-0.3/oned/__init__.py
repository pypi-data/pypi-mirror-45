
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from numba import jit, vectorize, float64, int64




@jit([float64[:](float64,float64,float64,float64,float64,int64)],cache=True)
def hmc_1dnb(grad,theta0,M,C,epsilon,iter=1000):
    """
    This function outputs the 1 dimiension Hamilton Monte Carlo samples without M-H correction.
    
    Args: 
        theta0: the initial point of theta, the parameter of interest
        grad: the gradient of the potential
        M: the mass
        C: the C term, where C*M^{-1} is the friction
        epsilon: stepsize
        iter: iteration number, 1000 by default
    """
    r=np.random.normal(0,np.sqrt(M))
    theta=theta0
    theta_save=np.zeros(iter)
    r_save=np.zeros(iter)
    for t in range(iter):
        theta=theta+epsilon*r/M
        r=r-grad(theta)*epsilon-epsilon*C*r/M+np.random.normal(0,np.sqrt(2*epsilon*C))
        theta_save[t]=theta
        r_save[t]=r
    return np.c_[theta_save,r_save]






