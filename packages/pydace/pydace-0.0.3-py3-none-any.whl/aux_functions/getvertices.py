import itertools
import numpy as np


def get_vertices_index(n):
    return np.asarray(list(itertools.product('01', repeat=n))).astype(np.int)


def get_vertices(lb, ub):
    """ Returns all vertices of the hypercube.

    Parameters
    ----------
    lb : np.array
        Lower bound of the hypercube.
    ub : np.array
        Upper bound of the hypercube.

    Returns
    -------
    out : np.array
        2**n-by-n array containing all the vertices of the n-dimensional hypercube. Each line corresponds to a vertex
        of the hypercube

    Raises
    ------
    ValueError
        if the bounds ´lb´ or ´ub´ does not have same shape or number of elements in each

    """
    if lb.ndim == 1 or ub.ndim == 1:
        lb = lb.reshape(1, -1)
        ub = ub.reshape(1, -1)

    if lb.shape != ub.shape:
        raise ValueError(f"´lb´ and ´ub´ must have the same number of elements. ´lb´ = {lb.size} and ´ub´= {ub.size}")

    n = lb.shape[1]  # number of dimensions
    m = 2 ** n  # number of vertices
    vertices_index = get_vertices_index(n)

    cat_placeholder = np.vstack((lb, ub))

    vertices = np.zeros(vertices_index.shape)
    for j in np.arange(n):
        for i in np.arange(m):
            vertices[i, j] = cat_placeholder[vertices_index[i, j], j]

    return vertices