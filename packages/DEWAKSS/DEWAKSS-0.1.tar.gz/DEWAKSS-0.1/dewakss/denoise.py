import scanpy as _sc
import scipy as _sp
from anndata import AnnData as _AnnData
from scipy.sparse import issparse as _issparse, csr as _csr
import scipy.sparse as _scs
# from sklearn.utils import check_X_y as _check_X_y, check_array as _check_array
# from sklearn.utils.validation import _is_arraylike, check_is_fitted
import warnings as _warnings
from sklearn.metrics import mean_squared_error as _mse, r2_score as _r2
from sklearn.base import BaseEstimator as _BaseEstimator, TransformerMixin as _TransformerMixin
from scvelo.preprocessing.neighbors import select_connectivities as _select_connectivities, select_distances as _select_distances
import time as _time
import matplotlib.pyplot as _plt
# from sklearn.utils.extmath import safe_sparse_dot as _safe_sparse_dot
from sklearn.model_selection import ShuffleSplit as _ShuffleSplit


def _matrixmult(A, B):
    """A wrapper for matrix mutiplication. Should handle most types of 2d arrays.

    :param A: A matrix
    :param B: A matrix
    :returns: A matrix
    :rtype: matrix

    """

    C = A @ B
    return C


class DEWAKSS(_BaseEstimator, _TransformerMixin):

    def __init__(self, data, use_layer='X', create_layer='Ms', mode='connectivities', iterations=10, weighted=True, init_thresholding=False, thresholding=False, keep0=False, init_diag=0, set_diag=0, n_neighbors=None, symmetrize=False, denoise_type='mean', run2best=True, verbose=True, memoryefficient=True, subset=False, random_state=42, max_dense=0.4, decay=1):
        """DEWAKSS does Denoising Expression data with
        Weighted Affinity based (X)Kernel and Self Supervision.

        DEWAKSS accepts an Affinity Kernal matrix to determine what
        datapoints should be averaged over and uses noise2self to
        determine what level of denoising most informative.

        Parameters marked with [*] will only affect the input if
        data is an AnnData object [pip insall anndata]

        :param data: an object containing the Affinity matrix [AnnData object, numpy.ndarray, scipy.csr_matrix].
        :param use_layer: [*] determine what layer should be used as the data. Default 'X'
        :param create_layer: [*] name of layer in AnnData object to be create. Default 'Ms'
        :param n_neighbors: if data is AnnData object will use the number used for calculating neighbours,
                            else will estimate median or use supplied if not None
        :param mode: [*] 'connectivities' or 'distances'. If data is AnnData will select the appropriate measure
                         for the Affinity graph. Default: 'connectivities'.
        :param iterations: Number of iterations to perform if run2best is False. Will be ignored if supplied in the fit function.
        :param weighted: [*] If False will use the initial Affintiy matrix with equally weighted neighbour influences. This may change during fitting.
        :param init_thresholding: Should the affinity matrix be thresholded on min influence in the initial step.
        :param thresholding: Should the affinity matrix be continually thresholded on min influence for all steps.
        :param keep0: Preserve 0 entries in the data matrix during iteration and transformation, Default False.
        :param init_diag: Explicitly set the diagonal entries of the initial affinity matrix to this value
                          before transforming to right stochastic matrix. Default 0
        :param set_diag: Explicitly set the diagonal entries of the affinity matrix at each step to this value
                         before transforming to right stochastic matrix. Default 0
        :param symmetrize: Transform the initial affinity matrix to a symmetric matrix by summing C + C.T. Default False
        :param denoise_type: what operation should be performed to denoise, Currently only option is mean. Default 'mean'.
        :param run2best: Should we stop as soon as optimal is reached. Default True.
        :param verbose: Should we print progress at each iteration step. Should we annotate the plot. Default True.
        :param memoryefficient: Should we try to be memory efficient by keeping data sparse. Default True
        :param subset: Should we select a subset of data to fit on. Accepts float or int or bool. Default False.
        :param random_state: For random operations what random state should be used, Default 42
        :param max_dense: At what density should we transform our Affinity matrix to dense. Default 0.4
        :param decay: Parameter that tries to mimic MAGIC decay parameter. However it is not the same. Set at own risk. Default 1
        :returns: self
        :rtype: DEWAKSS

        """

        super(DEWAKSS, self).__init__()

        self.random_state = random_state
        self.memoryefficient = memoryefficient
        self.subset = subset
        self.max_dense = max_dense
        self.use_layer = use_layer
        self.create_layer = create_layer
        self.mode = mode
        self.set_diag = set_diag
        self.init_diag = init_diag
        self.decay = decay
        self.weighted = weighted
        if denoise_type == 'median':
            raise NotImplementedError("Median smoothing is not implemented.")

        self.denoise_type = denoise_type
        self.run2best = run2best
        self.verbose = verbose

        self.iterations = iterations
        self.init_thresholding = init_thresholding
        self.thresholding = thresholding
        self.keep0 = keep0
        self.symmetrize = symmetrize

        self._parse_input_anndata(data, n_neighbors)

    def _parse_input_anndata(self, data, n_neighbors):

        if isinstance(data, _AnnData):
            # self._parse_input_anndata(data, n_neighbors)

            if n_neighbors is None:
                if 'neighbors' in data.uns_keys():
                    n_neighbors = data.uns['neighbors']['params']['n_neighbors']
                else:
                    _warnings.warn("neighborhood not computed, is now run with default parameters", UserWarning)
                    _sc.pp.neighbors(data)
                    n_neighbors = data.uns['neighbors']['params']['n_neighbors']

            self.n_neighbors = n_neighbors
            self.connectivities = self._make_dense(self.get_connectivities(data).copy())

        else:  # assume graph is supplied as sparse matrix
            if n_neighbors is None:
                nn = data.astype(bool).sum(1)
                nn[nn == 0] = 1
                n_neighbors == min(nn)

            self.n_neighbors = n_neighbors

            data = self._renormalize(data, set_diag=self.init_diag, thresholding=self.init_thresholding)
            self.connectivities = self._make_dense(data.copy())

    def _make_dense(self, X):

        if not self.memoryefficient and _issparse(X):
            X = X.A

        return X

    def _row_stochastic(self, C):

        cs = C.sum(1)
        cs[cs == 0] = 1
        if _issparse(C):
            C = C.multiply(1. / cs)
            C.eliminate_zeros()
            C = _csr.csr_matrix(C)
        else:
            # https://stackoverflow.com/questions/18522216/multiplying-across-in-a-numpy-array
            C = C * (1. / cs)[:, _sp.newaxis]

        return C

    def get_connectivities(self, adata):

        n_neighbors = self.n_neighbors
        mode = self.mode
        decay = self.decay
        symmetrize = self.symmetrize
        set_diag = self.init_diag
        thresholding = self.init_thresholding

        C = adata.uns['neighbors'][mode].copy()
        if n_neighbors is not None and n_neighbors < adata.uns['neighbors']['params']['n_neighbors']:
            C = _select_connectivities(C, n_neighbors) if mode == 'connectivities' else _select_distances(C, n_neighbors)

        if self.weighted:
            if mode == 'distances':
                # C.data = C.data / C.data.mean()
                meand = _sp.array([d.data.mean() for d in C])
                C = C.multiply(1. / meand)
                C.data = _sp.power(C.data, decay)  # TODO: Should this be below C.multiply above instead?
                C.data = _sp.exp(-1 * C.data)
                if set_diag is not None:
                    C.setdiag(set_diag)

                C = self._row_stochastic(C)
                C = self._threshold_knn(C, thresholding)
                # C = self._row_stochastic(C)

                if symmetrize:
                    C = C + C.T  # Symmetrize.

                    # C.data[C.data < thresholding] = 0
            else:
                if set_diag is not None:
                    C.setdiag(set_diag)

                C.data = _sp.power(C.data, decay)

                C = self._row_stochastic(C)
                C = self._threshold_knn(C, thresholding)
                if symmetrize:
                    C = C + C.T  # Symmetrize to get rid of complex eigenvalues.
                # C = self._row_stochastic(C)

            connectivities = C

        else:
            if symmetrize:
                C = C + C.T  # Symmetrize.
            C = self._threshold_knn(C, thresholding)
            connectivities = (C > 0).astype(float)

        connectivities = self._row_stochastic(connectivities)  # If this is failing, look at the solution I commented out above (cs = C.sum(1)....)
        connectivities.eliminate_zeros()

        if _issparse(connectivities):
            connectivities.tocsr().astype(_sp.float32)

        return connectivities

    def _threshold_knn(self, connectivities, thresholding=None):

        if isinstance(thresholding, bool) and (not thresholding):  # Do not threshold just pass by.
            return connectivities

        if thresholding is None:
            thresholding = self.thresholding

        knng = connectivities.copy()
        if isinstance(thresholding, bool) and thresholding:  # set to scale of contribution depending on number of total nodes
            threshold = 1 / knng.shape[0]
            if _issparse(knng):
                knng.data[knng.data < threshold] = 0
            else:
                knng[knng < threshold] = 0

        elif thresholding > 1:  # set to number of maximum neighbors
            thresholding = _sp.round(thresholding).astype(int)
            threshold = _sp.array([i.data[_sp.argsort(-i.data)][min(thresholding, i.size - 1)] for i in knng])

            C = []
            if _issparse(knng):
                for th, r in zip(threshold, knng):
                    r.data[r.data <= th] = 0
                    C.append(r)

                knng = _scs.vstack(C).copy()

            else:
                for th, r in zip(threshold, knng):
                    r[r <= th] = 0
                    C.append(r)

                knng = _sp.vstack(C)

        else:  # set to minimum contribution
            # threshold = 1 / thresholding
            if _issparse(knng):
                knng.data[knng.data < thresholding] = 0
            else:
                knng[knng < thresholding] = 0

        # cs = knng.sum(1)
        # cs[cs == 0] = 1

        # if _issparse(knng):
        #     knng = knng.multiply(1. / cs)
        #     knng = _csr.csr_matrix(knng)
        #     knng.eliminate_zeros()
        # else:
        #     knng = knng * (1. / cs)[:, _sp.newaxis]

        return knng

    def _apply_smoothing(self, X, connectivities=None):

        if connectivities is None:
            connectivities = self.opt_connectivities

        if self.keep0:
            Xtmp = _sp.abs(X).astype(bool).astype(float).copy()

        if self.denoise_type == 'mean':

            X_out = _matrixmult(connectivities, X.copy())
            # X_out = connectivities @ X

        elif self.denoise_type == 'median':
            D = []
            for r in connectivities:

                if _issparse(X):
                    rind = r.nonzero()[1]
                    D.append(_csr.csr_matrix(_sp.median(X[rind, :].A, 0)))

                else:
                    rind = r.nonzero()[1]
                    D.append(_sp.median(X[rind, :], 0))

            if _issparse(X):
                X_out = _scs.vstack(D)
            else:
                X_out = _sp.vstack(D)

        if self.keep0:
            X_out = _sp.multiply(X_out, Xtmp)

        return X_out

    def _renormalize(self, connectivities, set_diag=None, thresholding=None):

        if set_diag is None:
            set_diag = self.set_diag

        if set_diag is not None:
            if _issparse(connectivities):
                connectivities.setdiag(set_diag)
            else:
                _sp.fill_diagonal(connectivities, set_diag)

        if thresholding is None:
            thresholding = self.thresholding

        connectivities = self._threshold_knn(connectivities, thresholding=thresholding)

        connectivities = self._row_stochastic(connectivities)

        return connectivities

    def _iterate(self, X, iterations=None):

        prediction = {}
        fixed_iterations = True
        if iterations is None:
            fixed_iterations = False
            iterations = self.iterations

        connectivities = self.connectivities.copy()

        self.opt_connectivities = connectivities

        X_out = self._apply_smoothing(X, connectivities=connectivities)

        mse = _mse(X.A if _issparse(X) else X, X_out.A if _issparse(X_out) else X_out)
        r2 = _r2(X.A if _issparse(X) else X, X_out.A if _issparse(X_out) else X_out)
        prediction[0] = [mse, r2]

        old_mse = mse

        for i in _sp.arange(1, iterations):
            if self.verbose:
                print(f'Progress = {100*i/(iterations-1):.3f}%, i={i}, delta mse = {old_mse-mse:.2e}', end='\r')

            connectivities = _matrixmult(connectivities, self.connectivities.copy())

            connectivities = self._renormalize(connectivities)

            if _issparse(connectivities):
                if connectivities.nnz > _sp.prod(connectivities.shape) * self.max_dense:
                    connectivities = connectivities.toarray()

            X_out = self._apply_smoothing(X, connectivities=connectivities)
            mse = _mse(X.A if _issparse(X) else X, X_out.A if _issparse(X_out) else X_out)
            r2 = _r2(X.A if _issparse(X) else X, X_out.A if _issparse(X_out) else X_out)

            if (mse < old_mse) and not fixed_iterations:
                old_mse = mse
                self.opt_connectivities = connectivities

            elif fixed_iterations and i == iterations - 1:
                if self.verbose:
                    print(f"Run max iteration, i={i},  delta mse = {old_mse-mse:.2e}. Exiting.")
                self.opt_connectivities = connectivities

            elif self.run2best and (mse > old_mse) and not fixed_iterations:
                if self.verbose:
                    print(f"Found optimal, i={i}, delta mse = {old_mse-mse:.2e}. Exiting.")

                prediction[i] = [mse, r2]
                return prediction

            prediction[i] = [mse, r2]

        return prediction

    def _get_layer_data(self, data, copy=True):

        if isinstance(data, _AnnData):
            adata = data.copy() if copy else data
            if self.use_layer == 'X':
                X = adata.X
            elif self.use_layer == 'raw':
                X = adata.raw.X
            else:
                X = adata.layers[self.use_layer]

        else:
            X = data.copy()

        X = self._make_dense(X)

        return X

    def plot(self, ax=None, metric='mse', verbose=None):
        """Simple overview plot of fit performance

        :param ax: a figure axis, Default None
        :param metric: one of 'mse' or 'r2'
        :param verbose: Should we use annotation on plot. If None will use the DEWAKSS default. Default None
        :returns: (figure, ax) if ax is not None else (None, ax)
        :rtype: matplotlib axis

        """

        if ax is None:
            fig = _plt.figure(figsize=(5, 4), constrained_layout=True)
            axs = fig.subplots(1, 1)
        else:
            axs = ax

        iter = self.prediction_.keys()
        mse = [mse for mse, r2 in self.prediction_.values()]
        r2 = [r2 for mse, r2 in self.prediction_.values()]
        besti = _sp.argmin(mse)
        if metric == 'mse':
            axs.plot(iter, mse, label=self.decay)
            axs.set_ylabel('MSE')
        elif metric == 'r2':
            axs.plot(iter, r2, label=self.decay)
            axs.set_ylabel(r'$R^2$')

        axs.set_xlabel('iteration')
        axs.set_xticks(list(self.prediction_.keys()))
        axs.grid()

        if not self.run2best:
            ylims = _sp.array(axs.get_ylim())
            axs.vlines(besti, *(ylims), zorder=500, linestyle=':')

        if verbose is None:
            verbose = self.verbose

        if verbose:
            texttoshow = f"run t: {self._extime:10.3g} s\noptimal i: {besti:10d}"
            _plt.text(0.6, 0.9, texttoshow, fontsize=12, horizontalalignment='left', transform=axs.transAxes)

        return (fig, axs) if (ax is None) else (None, axs)

    def _subset(self, X):

        if self.subset:
            if isinstance(self.subset, bool):
                subset = 0.1
            else:
                subset = self.subset

            rs = _ShuffleSplit(1, test_size=None, train_size=subset, random_state=self.random_state)

            train_index, test_index = next(rs.split(X.T))

            return X[:, train_index]

        return X

    def fit(self, data, iterations=None):
        """Fit function for training DEWAKSS

        :param data: AnnData object or matrix
        :param iterations: If set hard sets the number of iterations ignoring DEWAKSS settings and stores the opt_connectivities as the final iteration instead of the best one. Default None.
        :returns: self
        :rtype: DEWAKSS object

        """

        X = self._get_layer_data(data, copy=True)

        X = self._subset(X)

        start_time = _time.time()

        prediction = self._iterate(X, iterations)
        self._extime = _time.time() - start_time

        self.prediction_ = prediction
        return self

    def transform(self, data, copy=True):
        """Transform function for DEWAKSS

        Will transform an input matrix with the fitted affinity kernal. If AnnData object will add the transformed data to the create_layer to layer.

        :param data: AnnData or matrix like data.
        :param copy: if the AnnData object should be handled in place or returned.
        :returns: matrix data or None
        :rtype: nparray, sparse, AnnData, None

        """

        if isinstance(data, _AnnData):
            adata = data.copy() if copy else data

            X_out = self.transform(self._get_layer_data(data, copy=True), copy=True)
            adata.layers[self.create_layer] = X_out
            return adata if copy else None

        X = self._get_layer_data(data, copy=copy)

        X_out = self._apply_smoothing(X)

        return X_out
