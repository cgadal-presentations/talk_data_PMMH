#!/usr/bin/env python
# coding: utf-8

# <h1 style='text-align:center'>Looking at topographical and meteorological data<h1>

# In[9]:


import os
import numpy as np
from netCDF4 import Dataset

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource

import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ### A-) Topographical data
# 
# <br>
# 
# #### 1-) Looking at file structure

# In[2]:


topo_file = "data/N26E006.SRTMGL1_NC.nc"

ds = Dataset(topo_file) 
print(ds)


# #### 2-) Plotting data

# In[3]:


lon, lat, DEM = ds.variables['lon'][:].data, ds.variables['lat'][:].data, ds.variables['SRTMGL1_DEM'][:].data

extent = [lon.min(), lon.max(), lat.min(), lat.max()]
zoom = [2500, 3000, 1500, 2000] # [left, right, bottom, top]
ind_transect = 1500

ls = LightSource(270, 45)
rgb = ls.shade(DEM, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')

fig, axarr  = plt.subplots(2, 2, constrained_layout=True, 
                           sharex='col', sharey ='row', height_ratios=[0.2, 1],
                          figsize=(5.5, 6.5))
axarr[0, 0].plot(lon, DEM[ind_transect, :], color='tab:orange')
axarr[0, 0].set_ylabel('height [m]')

im = axarr[1, 0].imshow(rgb, extent=extent)
axarr[1, 0].axhline(lat[ind_transect], color='tab:orange')
axarr[1, 0].set_xlabel('lon [deg.]')
axarr[1, 0].set_ylabel('lat [deg.]')

axarr[0, 0].plot(lon, DEM[ind_transect, :], color='tab:orange')
axarr[0, 0].set_ylabel('height [m]')

im = axarr[1, 0].imshow(rgb, extent=extent)
axarr[1, 0].axhline(lat[ind_transect], color='tab:orange')
axarr[1, 0].set_xlabel('lon [deg.]')
axarr[1, 0].set_ylabel('lat [deg.]')

plt.show()


# In[10]:


LON, LAT = np.meshgrid(lon, lat)
region = np.s_[::5, ::5]

fig = go.Figure(go.Surface(x=LON[region],y=LAT[region],z=DEM[region]))
fig.update_layout(height=600, width=800,
                  margin=dict(l=5, r=50, b=5, t=5))
fig.update_scenes(aspectmode='manual', aspectratio=dict(x=1, y=1, z=0.1))
fig.show()


# ### B-) Meteorological data
# 
# 
# #### B.1 Surface quantities

# In[5]:


wind_file = 'data/adaptor.mars.internal-1675099370.7887764-14315-8-262515c1-1605-461d-a45b-708ab30fbf0b.nc'

ds = Dataset(wind_file) 
print(ds)


# In[6]:


lon_w = np.around(ds.variables['longitude'][:].data.astype('float64'), 1) 
lat_w = np.around(ds.variables['latitude'][:].data[::-1].astype('float64'), 1)
u10, v10 = ds.variables['u10'][:].data.squeeze(), ds.variables['v10'][:].data.squeeze()
U = np.sqrt(u10**2 + v10**2)


# ### figure
fig, ax  = plt.subplots(1, 1, constrained_layout=True,  sharex=True, figsize=(6.1,6))

im = ax.imshow(DEM, extent=extent, alpha=0.7, cmap='gray')
strm = ax.streamplot(lon_w, lat_w, u10, v10, color=U, cmap='viridis')


ax.set_xlabel('lon [deg.]')
ax.set_ylabel('lat [deg.]')
plt.colorbar(im, label='height [m]')
plt.colorbar(strm.lines, label='U [m/s]', location='top')
plt.show()


# #### B.2 vertical profiles

# In[7]:


wind_file = 'data/adaptor.mars.internal-1675177009.4463217-21782-15-592c31db-6078-402e-90b9-9e080b20c24f.nc'

ds = Dataset(wind_file) 
print(ds)


# In[8]:


g = 9.81 # [m/s-2]
Rt = 6356766  # Average Earth radius [m]
Kelvin_to_degree = - 273.15
P0 = 1000 # Standard pressure [hPa
Pc = 0.2854  # Poisson coefficient for dry air R/Cp

geopotential = ds.variables['z'][:].data.squeeze()
z_coordinate = geopotential*Rt/(g*Rt - geopotential)/1000
pressure_levels = ds.variables['level'][:].data.squeeze()
temperature = ds.variables['t'][:].data.squeeze()

fig, axarr = plt.subplots(1, 2, constrained_layout=True, sharey=True)

axarr[0].plot(pressure_levels, z_coordinate, '.')
axarr[1].plot(temperature, z_coordinate, '.')

axarr[0].set_xlabel('Pressure [hPa]')
axarr[0].set_ylabel('Vertical coordinate [km]')
axarr[1].set_xlabel('Temperature [deg.]')

plt.show()

