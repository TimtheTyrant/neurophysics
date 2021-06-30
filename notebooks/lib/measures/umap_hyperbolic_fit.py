#Computes the first ndim coordinates resulting from a umap gaussian fit to data,
#Programmer: Tim Tyree
#Date: 6.24.2021
# from .. import *
import numpy as np,umap

def fit_hyperbolic_mapper(data,**kwargs):
    '''fits data to a hyperbolic mapper.
    data is a numpy array instance containing feature vectors'''
    hyperbolic_mapper = umap.UMAP(
    output_metric='hyperboloid',
    **kwargs).fit(data)
    return hyperbolic_mapper

def get_hyperbolic_umap_coordinates(data,**kwargs):
    try:
        hyperbolic_mapper=fit_hyperbolic_mapper(data,**kwargs)
    except ValueError as e:
        print(f"Warning: data.size={data.size} in call to get_hyperbolic_umap_coordinates. Returning None,None,None...")
        print(e)
        return None,None,None
    # hyperbolic_mapper = umap.UMAP(output_metric='hyperboloid',**kwargs).fit(data)
    x_values = hyperbolic_mapper.embedding_[:, 0]
    y_values = hyperbolic_mapper.embedding_[:, 1]
    z_values = np.sqrt(1 + np.sum(hyperbolic_mapper.embedding_**2, axis=1))
    disk_x = x_values / (1 + z_values)
    disk_y = y_values / (1 + z_values)
    disk_z = z_values
    return disk_x, disk_y, disk_z

def get_hyperbolic_umap_xycoordinates(data,**kwargs):
    disk_x, disk_y, disk_z = get_hyperbolic_umap_coordinates(data,**kwargs)
    x_values=disk_x
    y_values=disk_y
    return x_values,y_values

# # hyperbolic_mapper = umap.UMAP(output_metric='hyperboloid',**kwargs).fit(data)
# x_values = hyperbolic_mapper.embedding_[:, 0]
# y_values = hyperbolic_mapper.embedding_[:, 1]
# z_values = np.sqrt(1 + np.sum(hyperbolic_mapper.embedding_**2, axis=1))

# # subtract off the average umap coordinate for each trial
# # for each trial, subtract off the mean
# # for trialnum in sorted(set(trialnum_values)):
# #     boo=trialnum_values==trialnum
# #     x_origin=np.mean(x_values[boo])
# #     x_values[boo]=x_values[boo]-x_origin
# #     y_origin=np.mean(y_values[boo])
# #     y_values[boo]=y_values[boo]-y_origin
# #     z_origin=np.mean(z_values[boo])
# #     z_values[boo]=z_values[boo]-z_origin

# disk_x = x_values / (1 + z_values)
# disk_y = y_values / (1 + z_values)
