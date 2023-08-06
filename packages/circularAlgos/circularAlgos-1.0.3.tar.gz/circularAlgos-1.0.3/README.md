
# Package Name: <font color=red>circularAlgos</font>


```python

```

# Functionalities of this package:

- <b>r_vonmises()</b>     : This function is used for generating random numbers for a von Mises circular distribution
- <b>q_vonmises()</b>     : This function is used used to calculate the quantiles for the given probabilities for a von Mises distribution
- <b>p_vonmises()</b>     : This function is  used to calculate the CDF value at the given points for a von Mises distribution
- <b>d_vonmises()</b>     : This function is for calculating the PDF at the given points for a von Mises circular distribution
- <b>angles_VMF_mix()</b> : This function is used to fit angular data in radians using the expectation maximization algorithm for maximum likelihood estimatation of the parameters of the different mixtures
- <b>vmf_clust()</b>      : This function is used to:  
    - fit the given data using the expectation maximization algorithm for maximum likelihood estimatation of the parameters of the different mixtures
    - Perform probabilistic clustering using the mixtures obtained above


```python

```

# Installation Instructions:

### option (a)


```python
pip install circularAlgos
```

### option (b)


```python
pip install git+git://github.com/karthik-sundaram/circularAlgos.git
```


```python

```

# Example


```python
from circularAlgos import circular_stat
```

## r_vonmises()

- <b>Parameters:</b>
    - n: int, Number of observations
    - mu: float/int, location parameter
    - kappa: float/int, scale parameter. Large values of kappa corresponds to lower variance
- <b>Returns:</b>
    - rv_ls: list, pdf function
    - <plot>: plot of random numbers


```python
circular_stat.r_vonmises(10,1,1)
```




    (array([1.90392643, 1.29698706, 3.70585937, 1.03560135, 2.9858808 ,
            2.00919377, 1.05110894, 5.60320916, 3.32389668, 2.7122503 ]),
     [<matplotlib.lines.Line2D at 0x25d89e9f6d8>])




![png](output_15_1.png)


## q_vonmises()

- <b>Parameters:</b>
    - p: float/int or list, vector containing the probabilities at which the quantiles are to be calculated
    - mu: float/int, location parameter
    - kappa: float/int, scale parameter. Large values of kappa corresponds to lower variance
- <b>Returns:</b>
    - value: list, quantiles for the given probabilities for a von Mises distribution


```python
circular_stat.q_vonmises(0.5,1,6)
```




    array([1.])



## d_vonmises()

- <b>Parameters:</b>
    - q: float/int or list, vector containing the points at which the CDF is to be calculated
    - mu: float/int, location parameter
    - kappa: float/int, scale parameter. Large values of kappa corresponds to lower variance
- <b>Returns:</b>
    - result: list, Cumulative Distribution Function (CDF) value at the given points for a von Mises distribution


```python
circular_stat.d_vonmises(1,1,6)
```




    array([0.95498257])



### p_vonmises()

- <b>Parameters:</b>
    - q: float/int or list, vector containing the points at which the CDF is to be calculated
    - mu: float/int, location parameter
    - kappa: float/int, scale parameter. Large values of kappa corresponds to lower variance
- <b>Returns:</b>
    - result: list, Cumulative Distribution Function (CDF) value at the given points for a von Mises distribution


```python
circular_stat.p_vonmises([2,0.8],2,6)
```




    array([0.5       , 0.00359546])



### angles_VMF_mix()

- <b>Parameters:</b>
    - x: float/int or list, vector containing the points at which the density is to be calculated
    - mu: float/int, location parameter
    - kappa: float/int, scale parameter. Large values of kappa corresponds to lower variance
- <b>Returns:</b>
    - pdf: list, Probability Distribution Function (PDF) value at the given points for a von Mises distribution


```python
## Sample simulated data for demo purposes for 'angles_VMF_mix'
ls = [10,15,20,25,100,110,120,130,140]
```


```python
circular_stat.angles_VMF_mix(ls,2)
```




    ([2.094395100371017, 0.3054326188103176],
     [17.272339492503747, 105.9312216142795],
     [0.5555555566516756, 0.4444444433483244])



### vmf_clust()

- <b>Parameters:</b>
    - main_df: Data file with rows and features in a dataframe format
    - num_clusters: Number of clusters 
- <b>Returns:</b>
    - mu: list of the mixtures, location parameter
    - kappa: list of the mixtures, scale parameter. Large values of kappa corresponds to lower variance 
    - p_i: mixture proportions of each mixture/cluster summing to 1
    - final_df: final data table output with the cluster confidence % and a hard cluster assigned based on maximum PDF


```python
## Simulated data (or any dataset can be loaded in to the variable 'main_df' from outside)
## Sample simulated data for demo purposes for 'vmf_clust'
import numpy as np
import pandas as pd
c = [[x,y] for x,y in zip(list(np.random.normal(100,20,500)) , list(np.random.normal(50,10,500)))]
d = [[x,y] for x,y in zip(list(np.random.normal(50,10,1000)) , list(np.random.normal(0,10,1000)))]
e = [[x,y] for x,y in zip(list(np.random.normal(50,10,750)) , list(np.random.normal(100,20,750)))]
dat_raw = c+d+e
main_df = pd.DataFrame(dat_raw,columns=['feature-1','feature-2'])
```


```python
circular_stat.vmf_clust(main_df,3)
```

    mean 0 is: [0.9009015831296102, 0.4340234296838846]
    kappa 0 is: 58.48335070293291
    proportion 0 is: 0.25442116320609176
    mean 1 is: [0.46354515641171923, 0.8860732971753719]
    kappa 1 is: 70.51463849221643
    proportion 1 is: 0.333793722508583
    mean 2 is: [0.9999287470357647, -0.01193737205106105]
    kappa 2 is: 29.211491475842852
    proportion 2 is: 0.4117851142853245
    




    ([array([0.90090158, 0.43402343]),
      array([0.46354516, 0.8860733 ]),
      array([ 0.99992875, -0.01193737])],
     [58.48335070293291, 70.51463849221643, 29.211491475842852],
     [0.25442116320609176, 0.333793722508583, 0.4117851142853245],
            feature-1   feature-2     cluster-0  cluster-1     cluster-2  \
     0      95.148757   51.105459  2.877231e+00   0.291471  1.990578e-03   
     1      98.268448   53.766641  2.815560e+00   0.330419  1.595392e-03   
     2      63.828991   46.969576  1.116943e+00   1.679967  2.189727e-05   
     3      94.214721   48.017710  3.000003e+00   0.202070  3.623388e-03   
     4      88.269702   46.832051  2.912968e+00   0.267886  2.298810e-03   
     5     139.714998   39.140206  1.235828e+00   0.002118  2.811759e-01   
     6     119.835839   55.987126  3.031758e+00   0.106956  8.942965e-03   
     7      91.211826   59.221671  1.902028e+00   0.935308  1.592344e-04   
     8     112.970110   38.681688  2.012256e+00   0.009677  1.006399e-01   
     9      84.292913   54.795820  1.894224e+00   0.941379  1.563912e-04   
     10    112.519747   42.326277  2.413247e+00   0.020130  5.452661e-02   
     11    108.936308   60.264141  2.774471e+00   0.355693  1.394763e-03   
     12    114.349706   43.290313  2.439595e+00   0.021160  5.212215e-02   
     13     97.122676   47.760799  3.038514e+00   0.156161  5.323456e-03   
     14     83.161835   62.906939  9.637410e-01   1.865714  1.368070e-05   
     15     95.198956   61.779869  1.905207e+00   0.932841  1.604068e-04   
     16     91.176150   37.270620  2.731470e+00   0.038495  2.921826e-02   
     17    100.026459   58.968337  2.480336e+00   0.535298  6.188306e-04   
     18    101.170963   53.705338  2.911513e+00   0.268868  2.284685e-03   
     19     90.219575   56.564351  2.123357e+00   0.771491  2.649384e-04   
     20     93.657559   44.560778  3.042210e+00   0.122495  7.469090e-03   
     21    103.082300   27.835696  1.119702e+00   0.001620  3.275923e-01   
     22     91.627424   44.810123  3.041227e+00   0.149987  5.640094e-03   
     23    109.569675   51.068821  3.029757e+00   0.105064  9.153292e-03   
     24    124.147941   43.141757  2.075687e+00   0.010852  9.196067e-02   
     25    113.858974   51.914342  3.004717e+00   0.089053  1.129745e-02   
     26     83.269695   44.642551  2.882874e+00   0.287811  2.034457e-03   
     27    102.913149   54.038950  2.939803e+00   0.249324  2.590789e-03   
     28    121.021417   44.894051  2.355058e+00   0.018053  6.007121e-02   
     29     96.129633   43.350156  2.987842e+00   0.081923  1.252361e-02   
     ...          ...         ...           ...        ...           ...   
     2220   53.355890  108.659405  1.162186e-05   0.112920  9.472563e-15   
     2221   51.113087  121.681453  1.287250e-06   0.032938  4.072049e-16   
     2222   66.227356   79.272902  1.640195e-02   2.303136  1.285331e-09   
     2223   48.439613  103.572059  5.807596e-06   0.077430  3.458726e-15   
     2224   44.991144  111.946790  7.014078e-07   0.023050  1.749469e-16   
     2225   44.403296   91.861653  9.284083e-06   0.100055  6.824893e-15   
     2226   50.888723  134.869189  2.994971e-07   0.013822  5.436697e-17   
     2227   49.898923  108.187603  4.768069e-06   0.069418  2.604301e-15   
     2228   37.207546  120.011071  2.453751e-08   0.002872  1.922109e-18   
     2229   55.212332   94.170633  1.470725e-04   0.404967  4.358778e-13   
     2230   46.173333  108.467653  1.548198e-06   0.036663  5.274439e-16   
     2231   39.189977   73.037238  4.140838e-05   0.218736  6.249293e-14   
     2232   42.268645  118.310477  1.459053e-07   0.008887  2.051733e-17   
     2233   36.274521  106.762159  7.647532e-08   0.005935  8.633423e-18   
     2234   51.599422   83.921164  2.884726e-04   0.550545  1.258661e-12   
     2235   50.028484  119.431949  1.238562e-06   0.032206  3.858255e-16   
     2236   52.448763  104.692734  1.547850e-05   0.131538  1.442654e-14   
     2237   61.895923   73.650534  1.759563e-02   2.341212  1.467002e-09   
     2238   55.736282   89.113921  3.668096e-04   0.611958  1.846743e-12   
     2239   61.801826   98.068237  4.077765e-04   0.640732  2.188666e-12   
     2240   47.929808  123.950154  4.158764e-07   0.016862  8.516212e-17   
     2241   55.762212   72.619338  5.805172e-03   1.733903  1.927706e-10   
     2242   28.543186   76.928298  2.396475e-07   0.012064  4.014151e-17   
     2243   32.564768  122.848658  4.011478e-09   0.000871  1.847751e-19   
     2244   46.725910  119.543497  4.807859e-07   0.018398  1.039229e-16   
     2245   49.017079   89.170157  5.855790e-05   0.260052  1.056067e-13   
     2246   50.841559   81.558389  3.501024e-04   0.599625  1.713965e-12   
     2247   52.944674   86.873809  2.546412e-04   0.520710  1.032612e-12   
     2248   47.479082   96.967170  1.115839e-05   0.110482  8.925179e-15   
     2249   51.536405   86.283466  1.914810e-04   0.457550  6.586742e-13   
     
             cluster   max-pdf  total_pdf  %confidence  
     0     cluster-0  2.877231   3.170692    90.744555  
     1     cluster-0  2.815560   3.147574    89.451742  
     2     cluster-1  1.679967   2.796932    60.064648  
     3     cluster-0  3.000003   3.205696    93.583512  
     4     cluster-0  2.912968   3.183152    91.512045  
     5     cluster-0  1.235828   1.519121    81.351490  
     6     cluster-0  3.031758   3.147657    96.317921  
     7     cluster-0  1.902028   2.837496    67.031943  
     8     cluster-0  2.012256   2.122573    94.802704  
     9     cluster-0  1.894224   2.835760    66.797778  
     10    cluster-0  2.413247   2.487903    96.999208  
     11    cluster-0  2.774471   3.131559    88.597122  
     12    cluster-0  2.439595   2.512878    97.083729  
     13    cluster-0  3.038514   3.199998    94.953604  
     14    cluster-1  1.865714   2.829469    65.938672  
     15    cluster-0  1.905207   2.838209    67.127095  
     16    cluster-0  2.731470   2.799184    97.580965  
     17    cluster-0  2.480336   3.016253    82.232352  
     18    cluster-0  2.911513   3.182665    91.480341  
     19    cluster-0  2.123357   2.895112    73.342808  
     20    cluster-0  3.042210   3.172173    95.903009  
     21    cluster-0  1.119702   1.448915    77.278685  
     22    cluster-0  3.041227   3.196855    95.131854  
     23    cluster-0  3.029757   3.143974    96.367115  
     24    cluster-0  2.075687   2.178500    95.280578  
     25    cluster-0  3.004717   3.105068    96.768177  
     26    cluster-0  2.882874   3.172720    90.864441  
     27    cluster-0  2.939803   3.191717    92.107230  
     28    cluster-0  2.355058   2.433183    96.789201  
     29    cluster-0  2.987842   3.082289    96.935818  
     ...         ...       ...        ...          ...  
     2220  cluster-1  0.112920   0.112932    99.989709  
     2221  cluster-1  0.032938   0.032939    99.996092  
     2222  cluster-1  2.303136   2.319538    99.292879  
     2223  cluster-1  0.077430   0.077435    99.992500  
     2224  cluster-1  0.023050   0.023051    99.996957  
     2225  cluster-1  0.100055   0.100065    99.990722  
     2226  cluster-1  0.013822   0.013822    99.997833  
     2227  cluster-1  0.069418   0.069423    99.993132  
     2228  cluster-1  0.002872   0.002872    99.999146  
     2229  cluster-1  0.404967   0.405114    99.963696  
     2230  cluster-1  0.036663   0.036665    99.995777  
     2231  cluster-1  0.218736   0.218778    99.981073  
     2232  cluster-1  0.008887   0.008887    99.998358  
     2233  cluster-1  0.005935   0.005935    99.998711  
     2234  cluster-1  0.550545   0.550833    99.947630  
     2235  cluster-1  0.032206   0.032208    99.996154  
     2236  cluster-1  0.131538   0.131554    99.988234  
     2237  cluster-1  2.341212   2.358807    99.254046  
     2238  cluster-1  0.611958   0.612325    99.940096  
     2239  cluster-1  0.640732   0.641140    99.936398  
     2240  cluster-1  0.016862   0.016862    99.997534  
     2241  cluster-1  1.733903   1.739708    99.666314  
     2242  cluster-1  0.012064   0.012065    99.998014  
     2243  cluster-1  0.000871   0.000871    99.999539  
     2244  cluster-1  0.018398   0.018399    99.997387  
     2245  cluster-1  0.260052   0.260111    99.977487  
     2246  cluster-1  0.599625   0.599975    99.941647  
     2247  cluster-1  0.520710   0.520965    99.951121  
     2248  cluster-1  0.110482   0.110493    99.989901  
     2249  cluster-1  0.457550   0.457741    99.958168  
     
     [2250 rows x 9 columns])




```python

```
