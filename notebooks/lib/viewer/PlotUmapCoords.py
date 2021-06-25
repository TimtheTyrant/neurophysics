#Performs plotting on umap results
#Programmer: Tim Tyree
#Date: 6.24.2021
import numpy as np, matplotlib.pyplot as plt

def PlotUmapCoordsGaussian(x_values,y_values,c_values,
                           cmap='Spectral',
                           fontsize=22,
                           figsize=(6,6),
                           s=100,
                           marker='.',
                           alpha=0.7,
                           **kwargs):
    fig,ax=plt.subplots(ncols=1,figsize=figsize)
    ax.scatter(x_values, y_values,
                c=c_values, cmap=cmap, s=s, marker=marker,alpha=alpha,**kwargs)
    # ax.scatter(x_values, y_values,
    #             c=target, cmap=cmap, s=1000, marker='.',alpha=0.7)
    # ax.scatter(x_values, y_values,
    #             c='k', s=10, marker='.')
    ax.tick_params(axis='both',labelsize=fontsize)
    # ax.tick_params(axis='both', which='major', labelsize=fontsize)
    # ax.tick_params(axis='both', which='minor', labelsize=0)
    ax.set_xlabel('UMAP1',fontsize=fontsize)
    ax.set_ylabel('UMAP2',fontsize=fontsize)    # ax.set_xlabel('UMAP1 (seconds)',fontsize=fontsize)
    # ax.set_ylabel('UMAP2 (seconds)',fontsize=fontsize)
    # title='A Single Trial'
    # ax.set_title(title,fontsize=fontsize+4)
    return fig

def PlotUmapCoordsHyperbolic(x_values,y_values,c_values,
                           cmap='Spectral',
                           fontsize=22,
                           figsize=(6,6),
                           s=100,
                           marker='.',
                           alpha=0.7,
                           **kwargs):
    fig,ax=plt.subplots(ncols=1,figsize=figsize)
    ax.scatter(x_values, y_values, c=c_values, cmap=cmap, s=s, marker=marker,alpha=alpha,**kwargs)
    # ax.scatter(x_values, y_values,
    #             c=target, cmap=cmap, s=1000, marker='.',alpha=0.7)
    # ax.scatter(x_values, y_values,
    #             c='k', s=10, marker='.')
    ax.tick_params(axis='both',labelsize=fontsize)
    # ax.tick_params(axis='both', which='major', labelsize=fontsize)
    # ax.tick_params(axis='both', which='minor', labelsize=0)
    #     ax.set_xlabel('UMAP1 (seconds)',fontsize=fontsize)
    #     ax.set_ylabel('UMAP2 (seconds)',fontsize=fontsize)
    # title='A Single Trial'
    # ax.set_title(title,fontsize=fontsize+4)

    #circular formatting
    boundary = plt.Circle((0,0), 1.05, fc='none', ec='k')
    ax.add_artist(boundary)
    ax.axis('off');
    ax.set_xlim([-1.1,1.1])
    ax.set_ylim([-1.1,1.1])
    return fig
