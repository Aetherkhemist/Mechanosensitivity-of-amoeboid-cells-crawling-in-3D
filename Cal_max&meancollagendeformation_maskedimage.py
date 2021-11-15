#Script for finding local max Intensity values
#Import libraries
import pandas as pd
import os
import seaborn as sns
import numpy as np
import math 
import matplotlib.pyplot as plt
from scipy import interpolate
from PIL import Image
from matplotlib import cm

#set pixel_size to convert pixel in um
pixel_size = 0.1084

def interpolateGrid(x,y,vals,X,Y):
    vals = interpolate.griddata((x,y),vals,(X.ravel(),Y.ravel()))
    return(vals)

#set path for directory for PIV results exported as .dat from Lavision Davis
path = 'C:\\Users\\examplepath_raw'
dir_list = os.listdir(path)
#get all files in directory
cur_dir = dir_list[0]
file_list = np.sort(os.listdir(path + '/' + cur_dir))

#set path for directory with masked files 
path_1 = 'C\\Users\\examplepath_raw_mask'
dir_list_1 = os.listdir(path_1)
#get all files in directory
cur_dir_1 = dir_list_1[0]
file_list_1 = np.sort(os.listdir(path_1 + '/' + cur_dir_1))

#time points
t=len(file_list)
#z points
z=len(dir_list)
#create matrix
max_vals = np.zeros([z,t])
mean_vals = np.zeros([z,t])

for j in np.arange(z):

    #deformation from PIV
    cur_dir = dir_list[j]
    file_list = np.sort(os.listdir((path + '/' + cur_dir)))
    #masks
    cur_dir_1 = dir_list_1[j]
    file_list_1 = np.sort(os.listdir((path_1 + '/' + cur_dir_1)))

    for i in np.arange(t):
        
        print(str(j) + ',' +  str(i))
        cur_file = path + '/'  + cur_dir + '/'  + file_list[i]
        
        #reading PIV
        dat = np.loadtxt(cur_file, skiprows=3)
        x   = dat[:,0]*pixel_size
        y   = dat[:,1]*pixel_size
        ux  = dat[:,2]*pixel_size
        uy  = dat[:,3]*pixel_size
        
        #masked image
        im_mask = Image.open(path_1 + '/'  + cur_dir_1 + '/' + file_list_1[0])
        im_mask = np.array(im_mask)
        
        #creating a matrix for the deformation values using the mask
        x_grid = np.unique(x) 
        y_grid = np.unique(y)      
        x_grid_new = np.linspace(x_grid.min(),x_grid.max(),np.shape(im_mask)[1]) 
        y_grid_new = np.linspace(y_grid.min(),y_grid.max(),np.shape(im_mask)[0]) 
        X,Y = np.meshgrid(x_grid_new,y_grid_new)
        
        Ux = interpolateGrid(x,y,ux,X,Y)
        Ux = np.reshape(Ux,np.shape(X))
        Uy = interpolateGrid(x,y,uy,X,Y)
        Uy = np.reshape(Uy,np.shape(X))
        U_mag = np.sqrt(Ux**2+Uy**2)
                
        #creating a matrix for the masked image
        x_grid = np.linspace(X.min(),X.max(),np.shape(im_mask)[1]) 
        y_grid = np.linspace(Y.min(),Y.max(),np.shape(im_mask)[0]) 
        X_im_mask,Y_im_mask = np.meshgrid(x_grid,y_grid)
                
        #masking the deformation values and actin image
        m = np.ma.masked_where(im_mask <255, im_mask)
        masked_Umag = np.ma.masked_array(U_mag, m.mask)
        
        #creating new matrices for the masked deformation values
        #U_mag matrix
        x_grid = np.linspace(X.min(),X.max(),np.shape(masked_Umag)[1]) 
        y_grid = np.linspace(Y.min(),Y.max(),np.shape(masked_Umag)[0]) 
        X_masked_Umag,Y_masked_Umag = np.meshgrid(x_grid,y_grid)

        #quiver plot represenation
        fig,ax = plt.subplots(ncols=3,figsize=[12,4])
        NR =15
        ax[0].quiver(X_masked_Umag[::NR,::NR],Y_masked_Umag[::NR,::NR],masked_Ux[::NR,::NR]/masked_Umag[::NR,::NR],masked_Uy[::NR,::NR]/masked_Umag[::NR,::NR],masked_Umag[::NR,::NR],units='width',  scale=30, zorder=2,cmap=cm.plasma)

#write to CSV
#max value
maxvals=pd.DataFrame(max_vals)
maxvals=maxvals.T
maxvals=maxvals.add_prefix('stack_')
maxvals.to_csv(os.path.join(save_path, 'max_deform.csv'))

#mean and sd  deformation
meanvals=pd.DataFrame(mean_vals)
meanvals=meanvals.T
meanvals=meanvals.add_prefix('stack_')
meanvals.to_csv(os.path.join(save_path, 'mean_deform.csv'))

