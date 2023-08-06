__auther__ = 'Xinyu Wang'

import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_validate, cross_val_score
from sklearn.model_selection import train_test_split

def run_CrossValidation(X,y,cv=5,return_format='np'):
    # Memo
    clf = svm.SVC(kernel='linear', C=1)
    clf = svm.SVC(kernel='rbf', C=1)
    clf = svm.SVC(kernel='poly’', C=1)
    clf = svm.SVC(kernel='precomputed', C=1)
    clf = svm.SVC(kernel='sigmoid', C=1)
    # scores = cross_validate(clf, X, y, cv=cv)

    # For debug:
    X_train = X_train.iloc[:100,:]
    y_train = y_train.iloc[:100,:]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
    # clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
    clf.score(X_test, y_test)


# def run_svr(X,y)
#
#     clf = SVR(gamma='scale', C=1.0, epsilon=0.2)
#     clf.fit(X, y)
#
#     # Read out attributes
#     coeffs = lasso.coef_         # dense np.array
#     # coeffs = lasso.sparse_coef_  # sparse matrix
#
#     # coeffs = lasso.intercept_    # probably also relevant
#     if return_format == 'np':
#         return coeffs
#     else:
#         # TODO
#         return coeffs
