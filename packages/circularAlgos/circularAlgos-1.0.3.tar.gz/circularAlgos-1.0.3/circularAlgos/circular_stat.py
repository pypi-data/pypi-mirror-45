#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import math
import scipy.integrate as integrate
from scipy.special import iv
from scipy.optimize import brentq as root
import scipy.special as scp
import random
from math import exp, pi, log
from collections import Counter
from matplotlib import pyplot as plt


# In[2]:


def r_vonmises(n,mu,kappa):
    """
       This function is used for generating random numbers for a von Mises circular distribution
       
       Parameters:
            n: int, Number of observations
            mu: float/int, location parameter
            kappa: float/int, scale parameter. Large values of kappa corresponds to lower variance
        Returns:
            rv_ls: list, pdf function
            <plot>: plot of random numbers 
    """
    def q_vonmises(p, mu = 0 ,  kappa = None, from_ = None, tol = np.finfo(float).eps**0.6):

        if (type(p) != list):
            p = np.array([p])
        else:
            p = np.array(p)

        epsilon = 10 * np.finfo(float).eps  

        if (np.any(p > 1) or np.any(p < 0)): 
            raise ValueError("p must be between [0,1]")

        if (pd.isnull(from_)): 
            from_ = mu - np.pi

        n = len(p)
        mu = (mu - from_)%(2 * np.pi)      ## from is a keyword    

        if (len([mu]) != 1): 
            raise ValueError("is implemented only for scalar mean")   

        if (pd.isnull(kappa)): 
            raise ValueError("kappa should be provided")   


        def zeroPvonmisesRad(x, p, mu, kappa):
            if (np.isnan(x)):         
                y = np.nan              
            else: 
                integration = integrate.quad(lambda x: d_vonmises(x, mu, kappa), 0, x)
                y = integration[0] - p         ##integration[0] will give the value
            return(y);


        value = np.repeat(np.nan, p.size)
        for i in range(p.size):
            try:
                value[i] = root(lambda x: zeroPvonmisesRad(x, p[i], mu, kappa), 0, 2 * np.pi - epsilon)
            except:
                pass
                if(p[i] < (10 * epsilon)):
                    value[i] = 0
                elif (p[i] > (1 - 10 * epsilon)):
                    value[i] = 2 * np.pi - epsilon         
        value += from_
        return(value)

    def d_vonmises(x, mu, kappa, log = False):
        if (type(x) != list):
            x=[x]
        pdf = np.zeros(len(x))
        if (log):
            if (kappa < 100000):
                pdf = -(np.log(2*math.pi)+np.log(scp.ive(0, kappa)) + kappa) + kappa*(np.cos(np.subtract(x - mu)))
            else:
                if (((x-mu)%(2*math.pi))==0):
                    pdf = math.inf
                else:
                    pdf = -math.inf
        else:
            if (kappa == 0):
                pdf = np.repeat(1/(2*np.pi), len(x))
            elif (kappa < 100000):
                pdf = 1/(2 * np.pi * scp.ive(0, kappa)) * (np.exp(np.subtract(np.cos(np.subtract(x, mu)), 1)))**kappa
            else:
                if (np.mod(np.subtract(x, mu),(2*np.pi))==0):
                    pdf = math.inf
                else:
                    pdfm = 0
        return(pdf)

    
    a = np.random.uniform(0,1,n)
    b = [q_vonmises(x,mu,kappa) for x in a]
    c = np.squeeze([l.tolist() for l in b])
    rv_ls = np.array([a%(2*np.pi) for a in c])
    a = (np.cos(rv_ls)+ np.random.normal(scale=0.05,size=n))
    b = (np.sin(rv_ls)+ np.random.normal(scale=0.05,size=n))
    
    return(rv_ls,plt.plot(a, b,'o', color='black',alpha=0.3))


# In[3]:


def q_vonmises(p, mu = 0 ,  kappa = None, from_ = None, tol = np.finfo(float).eps**0.6):
    """
       This function is used used to calculate the quantiles for the given probabilities for a von Mises distribution
       
       Parameters:
            p: float/int or list, vector containing the probabilities at which the quantiles are to be calculated
            mu: float/int, location parameter
            kappa: float/int, scale parameter. Large values of kappa corresponds to lower variance
        Returns:
            value: list, quantiles for the given probabilities for a von Mises distribution
    """
    def d_vonmises(x, mu, kappa, log = False):
        if (type(x) != list):
            x=[x]
        pdf = np.zeros(len(x))
        if (log):
            if (kappa < 100000):
                pdf = -(np.log(2*math.pi)+np.log(scp.ive(0, kappa)) + kappa) + kappa*(np.cos(np.subtract(x - mu)))
            else:
                if (((x-mu)%(2*math.pi))==0):
                    pdf = math.inf
                else:
                    pdf = -math.inf
        else:
            if (kappa == 0):
                pdf = np.repeat(1/(2*np.pi), len(x))
            elif (kappa < 100000):
                pdf = 1/(2 * np.pi * scp.ive(0, kappa)) * (np.exp(np.subtract(np.cos(np.subtract(x, mu)), 1)))**kappa
            else:
                if (np.mod(np.subtract(x, mu),(2*np.pi))==0):
                    pdf = math.inf
                else:
                    pdfm = 0
        return(pdf)

    if (type(p) != list):
        p = np.array([p])
    else:
        p = np.array(p)
        
    epsilon = 10 * np.finfo(float).eps  
    
    if (np.any(p > 1) or np.any(p < 0)): 
        raise ValueError("p must be between [0,1]")
        
    if (pd.isnull(from_)): 
        from_ = mu - np.pi
   
    n = len(p)
    mu = (mu - from_)%(2 * np.pi)      ## from is a keyword    
    
    if (len([mu]) != 1): 
        raise ValueError("is implemented only for scalar mean")   
        
    if (pd.isnull(kappa)): 
        raise ValueError("kappa should be provided")   
        
        
    def zeroPvonmisesRad(x, p, mu, kappa):
        if (np.isnan(x)):         
            y = np.nan              
        else: 
            integration = integrate.quad(lambda x: d_vonmises(x, mu, kappa), 0, x)
            y = integration[0] - p         ##integration[0] will give the value
        return(y);
    
    
    value = np.repeat(np.nan, p.size)
    for i in range(p.size):
        try:
            value[i] = root(lambda x: zeroPvonmisesRad(x, p[i], mu, kappa), 0, 2 * np.pi - epsilon)
        except:
            pass
            if(p[i] < (10 * epsilon)):
                value[i] = 0
            elif (p[i] > (1 - 10 * epsilon)):
                value[i] = 2 * np.pi - epsilon         
    value += from_
    return(value)


# In[4]:


def p_vonmises(q, mu, kappa, tol = 1e-020):
    """
       This function is  used to calculate the CDF value at the given points for a von Mises distribution.
       
       Parameters:
            q: float/int or list, vector containing the points at which the CDF is to be calculated
            mu: float/int, location parameter
            kappa: float/int, scale parameter. Large values of kappa corresponds to lower variance
        Returns:
            result: list, Cumulative Distribution Function (CDF) value at the given points for a von Mises distribution
    """
    from_ = mu - np.pi
    mu = (mu - from_) % (2 * np.pi)
    
    
    if (type(q) != list):
        q = [q]
    q = np.mod(np.subtract(q, from_), (2 * np.pi))
    q = np.mod(q,(2 * np.pi))
    n = len(q)
    mu = mu % (2 * np.pi)
    def fn_mu0(q,kappa,tol):
        flag = 1
        p = 1
        sum_ = 0
        while(flag):
            term = (iv(p, kappa) * np.sin(np.multiply(q, p)))/p
            sum_ = sum_ + term
            p = p + 1
            if (abs(term) < tol):
                flag = 0
        return(np.divide(q,(2 * np.pi)) + sum_/(np.pi * iv(0, kappa)))
    result = np.repeat(np.nan, n)
    if (mu == 0):
        for i in range(0,n):
            result[i] = fn_mu0(q[i], kappa, tol)
    else:
        for i in range(0,n):
            if (q[i] <= mu):
                upper = (q[i] - mu) % (2 * np.pi)
                if (upper == 0):
                    upper = 2 * np.pi
                lower = (-mu) % (2 * np.pi)
                result[i] = fn_mu0(upper, kappa, tol) - fn_mu0(lower, kappa, tol)
            else:
                upper = q[i] - mu
                lower = mu % (2 * np.pi)
                result[i] = fn_mu0(upper, kappa, tol) + fn_mu0(lower, kappa, tol)
    return(result)


# In[5]:


def d_vonmises(x, mu, kappa, log = False):
    """
       This function is for calculating the PDF at the given points for a von Mises circular distribution.
       
       Parameters:
            x: float/int or list, vector containing the points at which the density is to be calculated
            mu: float/int, location parameter
            kappa: float/int, scale parameter. Large values of kappa corresponds to lower variance
        Returns:
            pdf: list, Probability Distribution Function (PDF) value at the given points for a von Mises distribution
    """
    if (type(x) != list):
        x=[x]
    pdf = np.zeros(len(x))
    if (log):
        if (kappa < 100000):
            pdf = -(np.log(2*math.pi)+np.log(scp.ive(0, kappa)) + kappa) + kappa*(np.cos(np.subtract(x - mu)))
        else:
            if (((x-mu)%(2*math.pi))==0):
                pdf = math.inf
            else:
                pdf = -math.inf
    else:
        if (kappa == 0):
            pdf = np.repeat(1/(2*np.pi), len(x))
        elif (kappa < 100000):
            pdf = 1/(2 * np.pi * scp.ive(0, kappa)) * (np.exp(np.subtract(np.cos(np.subtract(x, mu)), 1)))**kappa
        else:
            if (np.mod(np.subtract(x, mu),(2*np.pi))==0):
                pdf = math.inf
            else:
                pdfm = 0
    return(pdf)


# In[6]:


def angles_VMF_mix(list_angles,num_mixtures):
    """
       This function is used to fit angular data in radians using the expectation maximization algorithm for
       maximum likelihood estimatation of the parameters of the different mixtures.
       
       Parameters:
            list_angles: list, angles in degrees
            num_mixtures: Number of mixtures 
        Returns:
            mu: list of the mixtures, location parameter
            kappa: list of the mixtures, scale parameter. Large values of kappa corresponds to lower variance 
            p_i: mixture proportions of each mixture/cluster summing to 1
    """
    dat_ls = [x*pi/180 for x in list_angles]
    dat_vector = [[math.cos(x),math.sin(x)] for x in dat_ls]
    p=len(dat_vector[0])
    knum = num_mixtures
    n = len(dat_ls)
    
    #Initializations
    mu = []
    kappa = list(np.repeat(1,num_mixtures))
    if(num_mixtures!=1):
        p_i = list(np.squeeze(np.random.dirichlet(np.ones(num_mixtures),size=1)))
    else:
        p_i = [1]
    for i in range(0,num_mixtures):
        mu.append(list(np.random.uniform(0,1,size = 1))) 
        
    def vmf_pdf(x, mu, kappa, log = False):
        if (type(x) == int):
            x = [x]
        if (type(x) == float):
            x = [x]
        vm = np.zeros(len(x))
        if (log):
            if (kappa == 0):
                vm = np.log(np.repreat(1/(2*pi), len(x)))
            elif (kappa < 100000):
                vm = -(np.log(2*math.pi)+np.log(scp.ive(0, kappa)) + kappa) + kappa*(np.cos(np.subtract(x - mu)))
            else:
                if (((x-mu)%(2*math.pi))==0):
                    vm = math.inf
                else:
                    vm = -math.inf
        else:
            if (kappa == 0):
                vm = np.repeat(1/(2*np.pi), len(x))
            elif (kappa < 100000):
                vm = 1/(2 * np.pi * scp.ive(0, kappa)) * (np.exp(np.subtract(np.cos(np.subtract(x, mu)), 1)))**kappa
            else:
                if (np.mod(np.subtract(x, mu),(2*np.pi))==0):
                    vm = math.inf
                else:
                    vm = 0
        return(vm)

    def comp_fn(mu,p_i,x,k,kappa):
        return p_i[k]*vmf_pdf(x,mu[k],kappa[k])

    def Ez_fun(mu,p_i,x,k,kappa):
        return comp_fn(mu,p_i,x,k,kappa)/sum(list(map(lambda k:comp_fn(mu,p_i,x,k,kappa) ,list(range(0,knum)) )))

    Ez_vals = np.full([n,knum], np.nan) 
    for iter in range(1,100):
      # E-step
        for k in range(0,knum):
            Ez_vals[:,k] = list(map(lambda x:Ez_fun(mu,p_i,x,k,kappa) ,dat_ls )) #P(pi of which fn dat came from/parameters)

      # M-step
        for k in range(0,knum):

            #alpha
            nk = sum(Ez_vals[:,k]) 
            p_i[k] = nk/n

            sum_norm = np.linalg.norm(sum(map(lambda x,y:np.dot(x,y),Ez_vals[:,k],dat_vector)))
            mu_vector = sum(map(lambda x,y:np.dot(x,y),Ez_vals[:,k],dat_vector))/sum_norm 
            mu[k] = math.acos(mu_vector[0])
            R = sum_norm / nk
            mle_kappa = (R * (p - R**2)) / (1 - R**2)
            kappa[k] = mle_kappa 
    return(mu,kappa,p_i)


# In[7]:


def vmf_clust(main_df, num_clusters,is_angles=0):
    """
       This function is used to 
       1) fit the given data using the expectation maximization algorithm for
       maximum likelihood estimatation of the parameters of the differnt mixtures
       2) Perform probabilistic clustering using the mixtures obtained above.
       
       Parameters:
            main_df: Data file with rows and features in a dataframe format
            num_clusters: Number of clusters 
        Returns:
            mu: list of the mixtures, location parameter
            kappa: list of the mixtures, scale parameter. Large values of kappa corresponds to lower variance 
            p_i: mixture proportions of each mixture/cluster summing to 1
            final_df: final data table output with the cluster confidence % and a hard cluster assigned based on maximum PDF
    """
    
    def unit_vec_fn(ls):
        """Convert the list of raw n-dimensional data into
        a list of set of unit vectors 
        """    
        magnitude  = pow(sum([a**2 for a in ls]),0.5)
        unit_vector  = [c/magnitude for c in ls]
        return(unit_vector)
    ######################################################################

    dat_raw = main_df.values.tolist()
    dat_ls = [unit_vec_fn(a) for a in dat_raw]   
    p = len(dat_ls[0])
    ######################################################################    
    
    def _get_vmf_likelihood_term(x, mu, kappa):
        """returns the likelihood back to the function 'vmf_pdf2()' that calculates the pdf"""
        return exp(kappa * np.dot(mu, x))
    ######################################################################
    
    def _get_vmf_normalization_numerator(p, kappa): 
        """returns a part of the numerator of the pdf back to the function 'vmf_pdf2()' that calculates the pdf"""
        return kappa ** (0.5*p - 1)
    ######################################################################
    
    def _get_vmf_normalization_denom(p, kappa):
        """returns a part of the denominator of the pdf back to the function 'vmf_pdf2()' that calculates the pdf"""
        return (2 * pi) ** (0.5*p) * iv(0.5*p-1, kappa)
    ######################################################################

    def vmf_pdf2(x, mu, kappa):
        """
        Pdf of the von Mises-Fisher distribution for a list of inputs at a time(unit vectors)
        Parameters:
            mu: list, location parameter
            kappa: float/int, scale parameter. Large values of kappa corresponds to lower variance
        Returns:
            list, pdf function
        """
        p=len(dat_ls[0])
        likelihood = _get_vmf_likelihood_term(x, mu, kappa)
        normalization_numerator = _get_vmf_normalization_numerator(p, kappa)
        normalization_denominator = _get_vmf_normalization_denom(p, kappa)
        return likelihood * (normalization_numerator / normalization_denominator)
    ######################################################################

    def vmf_pdf(x, mu, kappa, log = False):
        """
        Pdf of the von Mises-Fisher distribution for one input
        Parameters:
            mu: list, location parameter
            kappa: float/int, scale parameter. Large values of kappa corresponds to lower variance
        Returns:
            list, pdf function
        """
        if (type(x) == int):
            x = [x]
        if (type(x) == float):
            x = [x]
        vm = np.zeros(len(x))
        if (log):
            if (kappa == 0):
                vm = np.log(np.repreat(1/(2*pi), len(x)))
            elif (kappa < 100000):
                vm = -(np.log(2*math.pi)+np.log(scp.ive(0, kappa)) + kappa) + kappa*(np.cos(np.subtract(x - mu)))
            else:
                if (((x-mu)%(2*math.pi))==0):
                    vm = math.inf
                else:
                    vm = -math.inf
        else:
            if (kappa == 0):
                vm = np.repeat(1/(2*np.pi), len(x))
            elif (kappa < 100000):
                vm = 1/(2 * np.pi * scp.ive(0, kappa)) * (np.exp(np.subtract(np.cos(np.subtract(x, mu)), 1)))**kappa
            else:
                if (np.mod(np.subtract(x, mu),(2*np.pi))==0):
                    vm = math.inf
                else:
                    vm = 0
        return(vm)
    ######################################################################    
    
    def comp_fn(mu,p_i,x,k,kappa):
        """Numerator of the Expectation step in the algorithm and thiis function
        returns to the call from 'Ez_fun()' """
        return p_i[k]*vmf_pdf2(x,mu[k],kappa[k])
    
    ######################################################################  
    
    def Ez_fun(mu,p_i,x,k,kappa):
        """Performs the Expectation step in the EM algorithm"""
        return comp_fn(mu,p_i,x,k,kappa)/sum(list(map(lambda k:comp_fn(mu,p_i,x,k,kappa) ,list(range(0,knum)) )))
    ######################################################################  
    
    knum = num_clusters
    n = len(dat_ls)
    mu = []
    kappa = list(np.repeat(1,num_clusters))
    p_i = list(np.squeeze(np.random.dirichlet(np.ones(num_clusters),size=1)))
    for i in range(0,num_clusters):
        mu.append(list(np.random.uniform(0,1,size = p)))
        
    ######################################################################  
    
    mu_list=[]
    pi_list=[]
    kappa_list=[]
    Ez_vals = np.full([n,knum], np.nan) 
    
    for iter in range(1,500):
        
      # Expectation (E-step)
    
        for k in range(0,knum):
            """Performs the Expectation step in the EM algorithm for each data set of points"""
            Ez_vals[:,k] = list(map(lambda x:Ez_fun(mu,p_i,x,k,kappa) ,dat_ls )) #P(pi of which fn dat came from/parameters)
  
      # Maximization Step (M-step)
    
        for k in range(0,knum):
            """Performs the Maximization step in the EM algorithm for each data set of points"""
            
            # alpha update
            nk = sum(Ez_vals[:,k]) 
            p_i[k] = nk/n
            
            # mean update
            sum_norm = np.linalg.norm(sum(map(lambda x,y:np.dot(x,y),Ez_vals[:,k],dat_ls)))
            mu[k]= sum(map(lambda x,y:np.dot(x,y),Ez_vals[:,k],dat_ls))/sum_norm 
            if (is_angles==1): mu[k] = math.acos(mu[k][0])
            # kappa update
            R = sum_norm / nk
            mle_kappa = (R * (p - R**2)) / (1 - R**2)
            kappa[k] = mle_kappa  
            
        mu_copy = []
        mu_copy = mu.copy()
        mu_list.append(mu_copy)

        pi_copy = []
        pi_copy = p_i.copy()
        pi_list.append(pi_copy)

        kappa_copy = []
        kappa_copy = kappa.copy()
        kappa_list.append(kappa_copy)

        
        """Convergence/Termination Condition"""
        if(iter!=1):
            summ = 0
            for i in range(0,knum):
                summ = summ + sum([abs(a-b) for a,b in zip(np.squeeze(mu_list).tolist()[-1][i],np.squeeze(mu_list).tolist()[-1][i])]) +abs(pi_list[-1][i]-pi_list[-2][i]) +abs(kappa_list[-1][i]-kappa_list[-2][i])
            if(summ < 0.00001):
                break    
    ###################################################################### 
    
    """Clustering"""
    
    list_pdf = []
    for i in range(0,num_clusters):
        list_pdf.append(list(np.squeeze([vmf_pdf(y,np.arctan(mu[i][1]/mu[0][0]),kappa[0]) for y in [float(np.arctan(x[1]/x[0])) for x in dat_ls]])))
    
    df1 = pd.DataFrame(list_pdf).T
    df1.columns=['cluster-'+str(x) for x in range(0,num_clusters)]
    df1['cluster'] = df1.idxmax(1)
    df1['max-pdf'] = df1.max(axis=1)
    df1["total_pdf"] = df1.sum(axis=1) - df1['max-pdf'] 
    df1['%confidence'] = df1['max-pdf']*100/df1['total_pdf']
    final_df = main_df.join(df1)
    ######################################################################     
    
    for i in range(0,knum):
        print("mean %s is:"%(i),list(mu[i]))
        print("kappa %s is: %s"%(i,kappa[i]))
        print("proportion %s is: %s"%(i,p_i[i]))
    return(mu,kappa,p_i,final_df)  
        


# In[ ]:




