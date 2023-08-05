# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 10:20:30 2018

@author: Felipe Souza Lima (felipe.lima@eq.ufcg.edu.br)
"""

import numpy as np
from pyDOE2 import lhs


def lhsdesign(n, min_range, max_range, k=5, include_vertices=False):
    """Returns the Latin Hypercube Sampling for a given range of values.

    Parameters
    ----------
    n : int
        Number of samples of the hypercube.
    min_range : np.array
        1-by-p or p-by-1 array containing the minimum values for each variable.
    max_range : np.array
        1-by-p or p-by-1 array containing the maximum values for each variable.
    k : int, optional
        Number of iterations to attempt to improve the design.
    include_vertices : bool
        To include or not the vertices of the hypercube in the sample.

    Returns
    -------
    out : np.array
        n-by-p array containing the Latin Hypercube Sampling.

    Raises
    ------
    ValueError
        If ndim of either `min_range` or `max_range` is not 2.

        If the `min_range` or `max_range` aren't vectors.


    """

    # check input ranges dimensions. If ndim != 2, raise error
    if min_range.ndim != 2 or max_range.ndim != 2:
        raise ValueError((f'Input ranges must be vectors (ndim = 2). Got ndim '
                          f'as min_range = {min_range.ndim} and max_range = '
                          f'{max_range.ndim}.'))
    else:
        # both have ndim == 2, check their shape
        min_shape = min_range.shape
        max_shape = max_range.shape

        if np.min(min_shape) != 1 or np.min(max_shape) != 1:
            raise ValueError(('Input ranges aren\'t vectors. Their shapes are '
                              f'min_range = {min_range.shape} and max_range '
                              f'= {max_range.shape}.'))

        else:
            # if everything is ok, reshape the vector to ensure they are rows
            min_range = min_range.reshape(1, -1)
            max_range = max_range.reshape(1, -1)

            p = min_range.shape[1]

    # proceed with normal calculations
    slope = np.tile(max_range - min_range, (n, 1))
    offset = np.tile(min_range, (n, 1))

    # create normalized LH
    x_normalized = lhs(p, samples=n, iterations=k, criterion='maximin')

    if include_vertices:
        from lhs.getvertices import get_vertices
        vertices = get_vertices(min_range, max_range)

        # scale and return the LH
        return np.vstack((x_normalized * slope + offset, vertices))
    else:
        # scale and return the LH
        return x_normalized * slope + offset
