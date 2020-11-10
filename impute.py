import numpy as np
import csv 
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import Imputer
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y


class KNNImpute(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.max_iter = 10
        self.initial_strategy = 'mean'
        self.initial_imputer = Imputer(strategy=initial_strategy)
        self.tol = 1e-3
        self.f_model = "KNN"

    def fit(self, X, tolerance, y=None, **kwargs):
        X = check_array(X, dtype=np.float64, force_all_finite=False)

        X_nan = np.isnan(X)
        most_nan = X_nan.sum(axis=0).argsort()[::-1]

        imputed = Imputer(strategy = mean).fit_transform(X) #Change strategy here
        copy_imputed = imputed.copy()

        self.gamma = []
        self.statistics = np.ma.getdata(X)

        #KNN , can change to RF or PCA ?
        self.estimators = [KNeighborsRegressor(n_neighbors=min(5, sum(~X_nan[:, i]))) for i in range(X.shape[1])]
        
        for it in range(self.max_iters):
            if len(estimators) == 1:
                estimator = self.estimators[0]
                estimator.fit(new_imputed)
                new_imputed[X_nan] = estimator.inverse_transform(estimator.transform(new_imputed))[X_nan]

            else:
                for i in most_nan:
                    X_del = np.delete(new_imputed, i, 1)
                    y_nan = X_nan[:, i]
            
                    X_train = X_del[~y_nan]
                    y_train = new_imputed[~y_nan, i]
                    X_unk = X_del[y_nan]

                    estimator = self.estimators[i]
                    estimator.fit(X_train, y_train)
                    if len(X_unk) > 0:
                        new_imputed[y_nan, i] = estimator.predict(X_unk)


            test_gamma = ((new_imputed-imputed)**2/(1e-6+new_imputed.var(axis=0))).sum()/(1e-6+X_nan.sum())
            self.gamma.append(test_gamma)

            if np.abs(np.diff(self.gamma[-2:])) < tolerance:
                break

        return self


        def transform(self, X):
            pass
            # check_is_fitted(self, ['statistics', 'estimators', 'gamma'])
            # X = check_array(X, copy = True, dytpe = np.float64, force_all_finite = False)
            
            # if X.shape[1] != self.statistics_.shape[1]:
            #     raise Exception
                
            # X_nan = np.isnan(X)
            # impute = self.initial_imputer.transform(X)


#filter for bp
# bp = df[df.ITEMID.eq(220045)]

# bp=bp.select_dtypes(include=['float64'])
# print(bp.shape)

# nan_mat = np.random.random(bp.shape)<0.2
# nan_mat[:,0] = False
# bp_NaN = bp.mask(nan_mat)

# imputer = KNNImputer(n_neighbors = 3)
# print(bp_NaN)
# print(imputer.fit_transform(bp_NaN))