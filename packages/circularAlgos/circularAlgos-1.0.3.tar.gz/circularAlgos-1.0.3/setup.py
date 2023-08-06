#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:



from setuptools import setup 
  
# reading long description from file 
with open('DESCRIPTION.txt') as file: 
    long_description = file.read() 
  
  
# specify requirements of your package here
REQUIREMENTS = ['numpy']
  
# some more details 
CLASSIFIERS = [ 
    'Development Status :: 4 - Beta', 
    'Intended Audience :: Developers', 
    'Topic :: Internet', 
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python', 
    'Programming Language :: Python :: 2', 
    'Programming Language :: Python :: 2.6', 
    'Programming Language :: Python :: 2.7', 
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.3', 
    'Programming Language :: Python :: 3.4', 
    'Programming Language :: Python :: 3.5', 
    ] 
  
# calling the setup function  
setup(name='circularAlgos', 
      version='1.0.3', 
      description='Package with many functions for circular distributions', 
      long_description=long_description, 
      url='https://github.com/karthik-sundaram/circularAlgos', 
      author='Karthik Sundaram', 
      author_email='karthik.sun95@gmail.com', 
      license='MIT', 
      packages=['circularAlgos'], 
      classifiers=CLASSIFIERS, 
      install_requires=REQUIREMENTS, 
      keywords='mixture models circular distributions clustering'
      ) 


# In[ ]:

