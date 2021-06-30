#Computes the first ndim coordinates resulting from a umap gaussian fit to data,
#Programmer: Tim Tyree
#Date: 6.24.2021
# from .. import *
import numpy as np,umap

def fit_gaussian_mapper(data,n_components=2,**kwargs):
    '''fits data to a gaussian mapper.
    data is a numpy array instance containing feature vectors.'''
    gaussian_mapper = umap.UMAP(
    output_metric='gaussian_energy',
    n_components=n_components,#n_components=40,
    **kwargs).fit(data)
    return gaussian_mapper

def get_gaussian_umap_coordinates(data,numdim=2,n_components=2,**kwargs):
    gaussian_mapper=fit_gaussian_mapper(data,n_components=n_components,**kwargs)
    array=gaussian_mapper.embedding_.T[:numdim]
    return array

def get_gaussian_umap_xycoordinates(data,**kwargs):
    try:
        array=get_gaussian_umap_coordinates(data,numdim=2,**kwargs)
    except ValueError as e:
        print(f"Warning: data.size={data.size} in call to get_gaussian_umap_coordinates. Returning None,None...")
        print(e)
        return None,None
    x_values=array[0]
    y_values=array[1]
    return x_values,y_values

# x_values=gaussian_mapper.embedding_.T[0]
# y_values=gaussian_mapper.embedding_.T[1]
# # z_values=gaussian_mapper.embedding_.T[2]

# # subtract off the average umap coordinate for each trial
# # for each trial, subtract off the mean
# for trialnum in sorted(set(trialnum_values)):
#     boo=trialnum_values==trialnum
#     x_origin=np.mean(x_values[boo])
#     x_values[boo]=x_values[boo]-x_origin
#     y_origin=np.mean(y_values[boo])
#     y_values[boo]=y_values[boo]-y_origin
