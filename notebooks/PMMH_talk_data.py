#!/usr/bin/env python
# coding: utf-8

# # Looking at topographical and meteorological data

# In[1]:


# %matplotlib widget

import os
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt


# In[2]:


def print_netcdf_structure(ds):
    print('----> General structure:')
    print(ds)
    print('----> Groups and variables:')
    for grp in sorted(ds.groups.keys()):
        print('--> {}:'.format(grp))
        for var in sorted(ds.groups[grp].variables.keys()):
            if hasattr(ds.groups[grp][var], 'comments'):
                print('. {} [{}], {}'.format(var, ds.groups[grp][var].unit,
                                             ds.groups[grp][var].comments))
            else:
                print('. {} [{}]'.format(var, ds.groups[grp][var].unit))


# In[3]:


test_file = "data/N22E045.SRTMGL1_NC.nc"

ds = Dataset(test_file)
print_netcdf_structure(ds)


# In[5]:


LON, LAT = np.meshgrid(ds.variables['lon'][:], ds.variables['lon'][:])

plt.figure()
plt.pcolormesh(LON, LAT, ds.variables['SRTMGL1_DEM'][:])
plt.show()


# In[4]:


LON, LAT = np.meshgrid(ds.variables['lon'][:], ds.variables['lon'][:])

plt.figure()
plt.imshow(ds.variables['SRTMGL1_DEM'][:])
plt.show()


# In[ ]:




