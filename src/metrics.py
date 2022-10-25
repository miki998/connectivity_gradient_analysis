"""
@author: Chun Hei Michael Chan
@copyright: Private Copyright
@credits: [Chun Hei Michael Chan]
@maintainer: Chun Hei Michael Chan
@email: miki998chan@gmail.com
"""


import numpy as np
from scipy import stats
from scipy.spatial import ConvexHull




###################################################### 
################### METRICS - EVAL ###################
######################################################

def points_distance(pts1, pts2, pmethod="L1"):
    """
    Information:
    ------------
    Compute distance between two points

    Parameters
    ----------    
    pts1   ::[1darray<float>]
        Point would be of length the number of features
    pts2   ::[2darray<float>]

    pmethod::[string]
        The type of distance to implement for two points

    Returns
    -------
    dist::[float]
        Distance between the two points
    """

    assert pts1.shape == pts2.shape

    if pmethod == "L0":
        dist = max(np.abs(pts1-pts2))

    elif pmethod == "L1":
        dist = np.abs(pts1 - pts2).sum()
    
    elif pmethod == "L2":
        dist = np.linalg.norm(pts1-pts2)
    
    return dist 

def cluster_distance(clst1, clst2, method="closest", pmethod="L1"):
    """
    Information:
    ------------
    Compute distance between two clusters

    Parameters
    ----------
    clst1  ::[2darray<float>]
        Array of points, point would be of length the number of features (nb_points, nb_features)
    clst2  ::[2darray<float>]

    method ::[string]
        The type of distance to implement for two clusters
    pmethod::[string]
        The type of distance to implement for two points

    Returns
    -------
    dist::[float]
        Distance between the two clusters
    """

    if method == "closest":
        dist = min([points_distance(pts1, pts2, pmethod=pmethod) for pts1 in clst1 for pts2 in clst2])
            
                
    elif method == "centroid":
        centroid1 = clst1.mean(axis=0)
        centroid2 = clst2.mean(axis=0)
        dist = points_distance(centroid1, centroid2, pmethod=pmethod)
    
    return dist

def network_volume(grad, networkidx, method='distance', pmethod='L2'):
    """
    Information:
    ------------
    Remove mean and normalize by standard deviation on any array size

    Parameters
    ----------
    grad      ::[2darray<float>]
        Gradients with dimension (nb regions, nb features)
    
    networkidx::[array<int>]
        Indices in the 400 parcellations that belong to a certain network (e.g "Vis")
    
    method    ::[string]
        The type of distance to implement for volume computation

    pmethod   ::[string]
        The type of distance to implement for two points

    Returns
    -------
    dist::[float]
    """    
    if method == 'distance':
        centroid = np.asarray([np.mean(grad[networkidx,i]) for i in range(grad.shape[1])])
        dist = np.mean([points_distance(pts, centroid, pmethod=pmethod) for pts in grad])

    elif method == 'hull':
        hull = ConvexHull(grad)
        dist = hull.volume

    return dist


def correlation_search(arr1, arr2, tolshift, find=0):
    """
    Information:
    ------------
    On a large series 

    Parameters
    ----------
    arr1   ::[1darray<float>]
        First signal
    
    arr2   ::[1darray<float>]
        Second signal

    tolshift::[int]
        Number of timepoints we are allowed to shift

    find    ::[bool]
        Returning index of where the arrays have highest correlation

    Returns
    -------
    corr ::[float]
        Correlation value modulo shift with limited tolerance

    tup  ::[tuple<int, int>]
        Indexes for array1 and array2 to start with for the shift with best correlation

    p-val::[float]
        Significance of correlation

        
    """
    
    assert arr1.shape == arr2.shape
    # NOTE: we do not allow both to be shifted
    # shift 1st array then select max
    scores1 = [stats.pearsonr(arr1, arr2).statistic] + [stats.pearsonr(arr1[i:], arr2[:-i]).statistic for i in range(1,tolshift)]

    # shift 2nd array then select max
    scores2 = [stats.pearsonr(arr1[:-i], arr2[i:]).statistic for i in range(1,tolshift)]
    
    corr_pos = np.max(scores1 + scores2)
    corr_neg = np.min(scores1 + scores2)
    corr     = corr_pos * (np.abs(corr_pos) >= np.abs(corr_neg)) + corr_neg * (np.abs(corr_pos) < np.abs(corr_neg))
    if find:
        if corr in scores1: return corr, (scores1.index(corr), 0), stats.pearsonr(arr1[scores1.index(corr):], arr2).pvalue
        elif corr in scores2: return corr, (0, scores2.index(corr) + 1), stats.pearsonr(arr1, arr2[scores1.index(corr):]).pvalue

    return corr    



def procrustes_score(ref_gradient, aligned):
    """
    Information:
    ------------
    Read our formatted dataframes to obtain timeseries 
    in (time,voxels) format of a specific acquisition

    Parameters
    ----------
    ref_gradient::[2darray<float>]
        reference gradients with dimension (nb of region, nb of features) in our case most of times
        number of features would be the number of eigenvectors
    
    aligned     ::[2darray<float>]
        gradients that we aligned to reference with same dimension as reference gradients

    Returns
    -------
    error::[float]
        Score for the alignement process in comparison to the original reference
    """
        
    nbr, nbf = ref_gradient.shape
    error = np.square(ref_gradient - aligned).sum()
    error = error/nbr
    return error