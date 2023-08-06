from anndata import AnnData as _AnnData
import scipy as _sp
from scipy.sparse import issparse as _issparse


def ftt(data, reversed=False, copy=False, correction=-1):
    """
    Freeman-Tukey transform (FTT), y = √(x) + √(x + 1) + correction

    reversed this is x = (y - correction)^2 - 1

    correction is default -1 to preserve sparse data.
    """

    if isinstance(data, _AnnData):
        adata = data.copy() if copy else data

        ftt(adata.X, reversed=reversed, copy=False)
        return adata if copy else None

    X = data.copy() if copy else data

    if _issparse(X):
        X.data = _sp.sqrt(X.data) + _sp.sqrt(X.data + 1) + correction

    else:
        nnz = _sp.nonzero(X)
        X[nnz] = _sp.sqrt(X[nnz]) + _sp.sqrt(X[nnz] + 1) + correction

    if reversed:
        raise NotImplementedError
        X[nnz] = _sp.square(X[nnz] - correction) - 1

    return X if copy else None
