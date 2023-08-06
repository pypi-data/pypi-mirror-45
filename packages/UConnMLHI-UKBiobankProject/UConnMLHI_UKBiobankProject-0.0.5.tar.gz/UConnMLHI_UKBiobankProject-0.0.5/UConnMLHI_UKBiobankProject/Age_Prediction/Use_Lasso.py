__auther__ = 'Xinyu Wang'

from sklearn.linear_model import Lasso, LassoCV


def run_CrossValidation(X,y,cv=5,random_state=0,return_format='np'):
    # Build lasso and fit
    lasso = LassoCV(cv=cv, random_state=0)
    lasso.fit(X, y)

    # Read out attributes
    coeffs = lasso.coef_         # dense np.array
    # coeffs = lasso.sparse_coef_  # sparse matrix

    # coeffs = lasso.intercept_    # probably also relevant
    if return_format == 'np':
        return coeffs
    else:
        # TODO
        return coeffs


def measure_performance():
    pass
    # run 10 times , get linear model, average the coefficient
    # bagging boostraping aggregating
    # ddiction 5 abus
    # {value for  in variable}
    # take a look at fslnet

    # 1 for all correlation matrix
    # 2 for two column
    # 3

    # april june oct
    # all phenotypr in mental disease are questionnares
