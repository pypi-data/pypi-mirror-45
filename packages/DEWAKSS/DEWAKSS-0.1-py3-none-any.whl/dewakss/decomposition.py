import scanpy as _sc
import scipy as _sp
from sklearn.utils import check_X_y as _check_X_y, check_array as _check_array
from scipy.sparse import issparse as _issparse, csr as _csr
# from sklearn.utils.validation import _is_arraylike, check_is_fitted
from sklearn.model_selection import ShuffleSplit as _ShuffleSplit
# from sklearn.utils.extmath import safe_sparse_dot as _safe_sparse_dot
from sklearn.metrics import mean_squared_error as _mse, r2_score as _r2
from copy import deepcopy
from .utils import ftt


def _rescale(X, rescaler={_sc.pp.scale: {"zero_center": False}}):

    for scalefun, params in rescaler.items():
        if "sparse" in params and params['sparse']:
            P = params.copy()
            __ = P.pop('sparse', None)
            X.data = scalefun(X.data, **P).copy()
        else:
            X = scalefun(X, **params)

    return X


def _Xsplit(X, strategy):

    if strategy == 'uniform':
        X_masked, X_target = _uniform(X.copy())
    elif strategy == 'binomial':
        X_masked, X_target = _binomial(X.copy())

    return X_masked, X_target


def _binomial(X, p=0.5):
    """Split the data as in noise2self into one masked and one target data matrix using binomial probability splitting strategy.

    :param X: ndarray, csr_matrix
    :returns: X_masked, X_target
    :rtype: ndarray, csr_matrix

    """

    binom = _sp.random.binomial
    if _issparse(X):
        X_target = binom(X.data.astype(int), p)

        X_masked = X.data - X_target

        X_target = _csr.csr_matrix((X_target, X.nonzero()))
        X_masked = _csr.csr_matrix((X_masked, X.nonzero()))

        X_target.eliminate_zeros()
        X_masked.eliminate_zeros()
    else:
        X_target = _sp.array([])
        for x in X:
            y = (binom(x, p)).reshape((1, -1))
            if X_target.size == 0:
                X_target = y
            else:
                X_target = _sp.append(X_target, y, 0)

        X_masked = X - X_target

    X_masked.data = X_masked.data.astype(float)
    X_target.data = X_target.data.astype(float)

    return X_masked, X_target


def _uniform(X, **kwargs):
    """Split the data as in noise2self into one masked and one target data matrix using uniform probability splitting strategy.

    :param X: ndarray, csr_matrix
    :returns: X_masked, X_target
    :rtype: ndarray, csr_matrix

    """

    from scipy.stats import uniform

    gtn = uniform()

    if _issparse(X):
        rn = gtn.rvs(X.data.shape)
        X_target = X.data * rn
        X_masked = X.data - X_target

        X_target = _csr.csr_matrix((X_target, X.nonzero()))
        X_masked = _csr.csr_matrix((X_masked, X.nonzero()))

    else:
        X_target = _sp.array([])
        for x in X:
            rn = gtn.rvs(x.shape)
            y = (x * rn).reshape((1, -1))
            if X_target.size == 0:
                X_target = y
            else:
                X_target = _sp.append(X_target, y, 0)

        X_masked = X - X_target

    return X_masked, X_target


def decomposition_wrapper(cls):
    """A wrapper for decomposition methods following the format in scikit-learn. However due to different complexities of the inverse_transform and transform. It's unlikely that this is currently a general solution

    :param cls: The scikit-learn decomposition class to use as a base. Recommendend TruncatedSVD
    :returns: DEWAKSSDecomposition class.
    :rtype: class

    Example:
    ========
    from sklearn.decomposition import TruncatedSVD

    TruncatedSVD = decomposition_wrapper(TruncatedSVD)
    pca = TruncatedSVD()
    pca.fit(X)

    """

    class DEWAKSSDecomposition(cls):

        def __init__(self, strategy='binomial', rescaler={_sc.pp.normalize_per_cell: {"copy": True}, ftt: {'copy': True}}, subsample=None, random_state=42, n_components=50, layer='X', test_size=None, **super_params):
            """DEWAKSSDecomposition class. Self supervised optimal PCA selection.

            :param strategy: Only 'binomial' is supported.
            :param rescaler: A nested dictionary with functions as keys and arguments as sub dictionaries.
                             Will be applied to the data before decomposition is applied.
                             If set to None will select from the strategy (not implemented).
                             Default: {_sc.pp.normalize_per_cell: {}, ftt: {}}
            :param subsample: Use a subsample of data for optimal component selection. Default None.
            :param random_state: use this random state, Default 42.
            :param n_components: Number of components that should be tested (or computed).
            :param layer: Use this layer if input data is AnnData object.
            :param test_size: Should be 1-subsample. Default None.
            :returns: self.
            :rtype: DEWAKSSDecomposition class.

            Adds the
            :self.optimal_: property with the number of components that minimizes the MSE.
            :self.mse_: the MSE for all tests.
            :self.r2: the R2 of all tests.
            :self.rank_range: the PC order tested.

            Alternatives for the rescale could be e.g.
            with:
            import scanpy as sc
            rescaler={sc.pp.normalize_per_cell: {}, sc.pp.log1p: {}}
            rescaler={sc.pp.normalize_per_cell: {}, sc.pp.sqrt: {}}
            rescaler={sc.pp.normalize_per_cell: {}, sc.pp.log1p: {}, sc.pp.scale: {'copy': True, 'zero_center': False}}

            """

            super().__init__(n_components=n_components, random_state=random_state, **super_params)
            self.strategy = strategy

            if rescaler is None:
                if strategy == 'uniform':
                    rescaler = {_sc.pp.scale: {"zero_center": False}}
                elif strategy == 'binary':
                    rescaler = {_sc.pp.scale: {"zero_center": True}}
                elif strategy == 'binomial':
                    rescaler = {_sc.pp.normalize_per_cell: {"counts_per_cell_after": None, "copy": True}, ftt: {'copy': True}}
                else:
                    rescaler = {_sc.pp.scale: {"zero_center": False}}

            self.rescaler = rescaler

            self.layer_ = layer

            self.subsample = subsample
            if test_size is None and (subsample is not None):
                self.test_size = 1 - subsample
            else:
                self.test_size = test_size

        def extractX(self, data):

            if self.layer not in [None, 'X', 'raw']:
                if self.layer not in data.layers.keys():
                    raise KeyError('Selected layer: {} is not in the layers list. The list of '
                                   'valid layers is: {}'.format(self.layer, data.layers.keys()))
                matrix = data.layers[self.layer]
            elif self.layer == 'raw':
                matrix = data.raw.X
            else:
                matrix = data.X

            return matrix

        def fit(self, X_m, X_t=None):
            """Fit function

            :param X_m: Should be a count matrix
            :param X_t: if supplied will skip the split of X_m and assume these matrices are correctly split. Default None.
            :returns: self
            :rtype: DEWAKSSDecomposition

            """

            if X_t is not None:
                X_m, X_t = _check_X_y(X_m, X_t, accept_sparse=['csr', 'csc', 'coo'], force_all_finite=True, multi_output=True)
            else:
                X_m = _check_array(X_m, accept_sparse=['csr', 'csc', 'coo'], force_all_finite=True)

            if X_t is None:
                X_m, X_t = _Xsplit(X_m, self.strategy)
                X_m = _rescale(X_m, rescaler=self.rescaler)
                X_t = _rescale(X_t, rescaler=self.rescaler)

            if self.subsample is not None:
                rs = _ShuffleSplit(1, test_size=self.test_size, train_size=self.subsample, random_state=self.random_state)
                train_index, test_index = next(rs.split(X_m))
                super().fit(X_m[train_index, :])
            else:
                super().fit(X_m)

            decomper = deepcopy(self)

            mses = []
            r2s = []
            rank_range = _sp.arange(1, self.n_components)
            for k in rank_range:

                decomper.n_components = k
                decomper.components_ = self.components_[:k, :]

                if self.subsample is not None:
                    # prediction = _sp.dot(_safe_sparse_dot(X_m[test_index, :], self.components_[:k, :].T), self.components_[:k, :])
                    # prediction = _sp.dot(_safe_sparse_dot(X_m[test_index, :], decomper.components_.T), decomper.components_)
                    prediction = decomper.inverse_transform(decomper.transform(X_m[test_index, :]))
                    current_mse = _mse(X_t[test_index, :].toarray() if _issparse(X_t) else X_t[test_index, :], prediction)
                    current_r2 = _r2(X_t[test_index, :].toarray() if _issparse(X_t) else X_t[test_index, :], prediction)
                else:
                    # prediction = _sp.dot(_safe_sparse_dot(X_m, self.components_[:k, :].T), self.components_[:k, :])
                    prediction = decomper.inverse_transform(decomper.transform(X_m))
                    current_mse = _mse(X_t.toarray() if _issparse(X_t) else X_t, prediction)
                    current_r2 = _r2(X_t.toarray() if _issparse(X_t) else X_t, prediction)

                mses.append(current_mse)
                r2s.append(current_r2)

            self.mse_ = mses
            self.r2_ = r2s
            self.optimal_ = rank_range[_sp.argmin(mses)]
            self.rank_range = rank_range

            return self

    return DEWAKSSDecomposition
