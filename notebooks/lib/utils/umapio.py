#Performs input and output on umap results
#Programmer: Tim Tyree
#Date: 6.24.2021
import pandas as pd

def save_umap_xycoords_to_csv(output_dir,x_values,y_values,targ,t_values_out):
    '''saves umap coordinates to .csv'''
    df_out=pd.DataFrame({'phase':targ,'t':t_values_out,'x':x_values,'y':y_values})
    df_out.to_csv(output_dir,index=False)
    return True

def load_umap_xycoords_from_csv(input_dir):
    '''loads umap coordinates from .csv
    Example Usage:
    x_values,y_values,targ,t_values_out=load_umap_xycoords_from_csv(input_dir)
    '''
    df_in=pd.read_csv(input_dir)
    x_values=df_in['x']
    y_values=df_in['y']
    targ=df_in['phase']
    t_values_out=df_in['t']
    return x_values,y_values,targ,t_values_out
