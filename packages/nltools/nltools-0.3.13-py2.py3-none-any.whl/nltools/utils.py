'''
NeuroLearn Utilities
====================

handy utilities.

'''
__all__ = ['get_resource_path',
           'get_anatomical',
           'set_algorithm',
           'attempt_to_import',
           'all_same',
           'concatenate',
           '_bootstrap_apply_func',
           'set_decomposition_algorithm'
           ]
__author__ = ["Luke Chang"]
__license__ = "MIT"

from os.path import dirname, join, sep as pathsep
import nibabel as nib
import importlib
import os
from sklearn.pipeline import Pipeline
from sklearn.utils import check_random_state
from scipy.spatial.distance import squareform
import numpy as np
import pandas as pd
import collections
from types import GeneratorType


def get_resource_path():
    """ Get path to nltools resource directory. """
    return join(dirname(__file__), 'resources') + pathsep


def get_anatomical():
    """ Get nltools default anatomical image.
        DEPRECATED. See MNI_Template and resolve_mni_path from nltools.prefs
    """
    return nib.load(os.path.join(get_resource_path(), 'MNI152_T1_2mm.nii.gz'))


def set_algorithm(algorithm, *args, **kwargs):
    """ Setup the algorithm to use in subsequent prediction analyses.

    Args:
        algorithm: The prediction algorithm to use. Either a string or an
                    (uninitialized) scikit-learn prediction object. If string,
                    must be one of 'svm','svr', linear','logistic','lasso',
                    'lassopcr','lassoCV','ridge','ridgeCV','ridgeClassifier',
                    'randomforest', or 'randomforestClassifier'
        kwargs: Additional keyword arguments to pass onto the scikit-learn
                clustering object.

    Returns:
        predictor_settings: dictionary of settings for prediction

    """

    # NOTE: function currently located here instead of analysis.py to avoid circular imports

    predictor_settings = {}
    predictor_settings['algorithm'] = algorithm

    def load_class(import_string):
        class_data = import_string.split(".")
        module_path = '.'.join(class_data[:-1])
        class_str = class_data[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_str)

    algs_classify = {
        'svm': 'sklearn.svm.SVC',
        'logistic': 'sklearn.linear_model.LogisticRegression',
        'ridgeClassifier': 'sklearn.linear_model.RidgeClassifier',
        'ridgeClassifierCV': 'sklearn.linear_model.RidgeClassifierCV',
        'randomforestClassifier': 'sklearn.ensemble.RandomForestClassifier'
        }
    algs_predict = {
        'svr': 'sklearn.svm.SVR',
        'linear': 'sklearn.linear_model.LinearRegression',
        'lasso': 'sklearn.linear_model.Lasso',
        'lassoCV': 'sklearn.linear_model.LassoCV',
        'ridge': 'sklearn.linear_model.Ridge',
        'ridgeCV': 'sklearn.linear_model.RidgeCV',
        'randomforest': 'sklearn.ensemble.RandomForest'
        }

    if algorithm in algs_classify.keys():
        predictor_settings['prediction_type'] = 'classification'
        alg = load_class(algs_classify[algorithm])
        predictor_settings['predictor'] = alg(*args, **kwargs)
    elif algorithm in algs_predict:
        predictor_settings['prediction_type'] = 'prediction'
        alg = load_class(algs_predict[algorithm])
        predictor_settings['predictor'] = alg(*args, **kwargs)
    elif algorithm == 'lassopcr':
        predictor_settings['prediction_type'] = 'prediction'
        from sklearn.linear_model import Lasso
        from sklearn.decomposition import PCA
        predictor_settings['_lasso'] = Lasso()
        predictor_settings['_pca'] = PCA()
        predictor_settings['predictor'] = Pipeline(
                            steps=[('pca', predictor_settings['_pca']),
                                   ('lasso', predictor_settings['_lasso'])])
    elif algorithm == 'pcr':
        predictor_settings['prediction_type'] = 'prediction'
        from sklearn.linear_model import LinearRegression
        from sklearn.decomposition import PCA
        predictor_settings['_regress'] = LinearRegression()
        predictor_settings['_pca'] = PCA()
        predictor_settings['predictor'] = Pipeline(
                            steps=[('pca', predictor_settings['_pca']),
                                   ('regress', predictor_settings['_regress'])])
    else:
        raise ValueError("""Invalid prediction/classification algorithm name.
            Valid options are 'svm','svr', 'linear', 'logistic', 'lasso',
            'lassopcr','lassoCV','ridge','ridgeCV','ridgeClassifier',
            'randomforest', or 'randomforestClassifier'.""")

    return predictor_settings


def set_decomposition_algorithm(algorithm, n_components=None, *args, **kwargs):
    """ Setup the algorithm to use in subsequent decomposition analyses.

    Args:
        algorithm: The decomposition algorithm to use. Either a string or an
                    (uninitialized) scikit-learn decomposition object.
                    If string must be one of 'pca','nnmf', ica','fa'
        kwargs: Additional keyword arguments to pass onto the scikit-learn
                clustering object.

    Returns:
        predictor_settings: dictionary of settings for prediction

    """

    # NOTE: function currently located here instead of analysis.py to avoid circular imports

    def load_class(import_string):
        class_data = import_string.split(".")
        module_path = '.'.join(class_data[:-1])
        class_str = class_data[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_str)

    algs = {
        'pca': 'sklearn.decomposition.PCA',
        'ica': 'sklearn.decomposition.FastICA',
        'nnmf': 'sklearn.decomposition.NMF',
        'fa': 'sklearn.decomposition.FactorAnalysis'
        }

    if algorithm in algs.keys():
        alg = load_class(algs[algorithm])
        alg = alg(n_components, *args, **kwargs)
    else:
        raise ValueError("""Invalid prediction/classification algorithm name.
            Valid options are 'pca','ica', 'nnmf', 'fa'""")
    return alg


def isiterable(obj):
    ''' Returns True if the object is one of allowable iterable types. '''
    return isinstance(obj, (list, tuple, GeneratorType))


module_names = {}
Dependency = collections.namedtuple('Dependency', 'package value')


def attempt_to_import(dependency, name=None, fromlist=None):
    if name is None:
        name = dependency
    try:
        mod = __import__(dependency, fromlist=fromlist)
    except ImportError:
        mod = None
    module_names[name] = Dependency(dependency, mod)
    return mod


def all_same(items):
    return np.all(x == items[0] for x in items)


def concatenate(data):
    '''Concatenate a list of Brain_Data() or Adjacency() objects'''

    if not isinstance(data, list):
        raise ValueError('Make sure you are passing a list of objects.')

    if all([isinstance(x, data[0].__class__) for x in data]):
        # Temporarily Removing this for circular imports (LC)
        # if not isinstance(data[0], (Brain_Data, Adjacency)):
        #     raise ValueError('Make sure you are passing a list of Brain_Data'
        #                     ' or Adjacency objects.')

        out = data[0].__class__()
        for i in data:
            out = out.append(i)
    else:
        raise ValueError('Make sure all objects in the list are the same type.')
    return out


def _bootstrap_apply_func(data, function, random_state=None, *args, **kwargs):
    '''Bootstrap helper function. Sample with replacement and apply function'''
    random_state = check_random_state(random_state)
    data_row_id = range(data.shape()[0])
    new_dat = data[random_state.choice(data_row_id,
                                       size=len(data_row_id),
                                       replace=True)]
    return getattr(new_dat, function)(*args, **kwargs)


def check_square_numpy_matrix(data):
    '''Helper function to make sure matrix is square and numpy array'''

    from nltools.data import Adjacency

    if isinstance(data, Adjacency):
        data = data.squareform()
    elif isinstance(data, pd.DataFrame):
        data = data.values
    else:
        data = np.array(data)

    if len(data.shape) != 2:
        try:
            data = squareform(data)
        except ValueError:
            raise ValueError("Array does not contain the correct number of elements to be square")
    return data


def check_brain_data(data):
    '''Check if data is a Brain_Data Instance.'''
    from nltools.data import Brain_Data

    if not isinstance(data, Brain_Data):
        if isinstance(data, nib.Nifti1Image):
            data = Brain_Data(data)
        else:
            raise ValueError("Make sure data is a Brain_Data instance.")
    return data


def _roi_func(brain, roi, algorithm, cv_dict, **kwargs):
    '''Brain_Data.predict_multi() helper function'''
    return brain.apply_mask(roi).predict(algorithm=algorithm, cv_dict=cv_dict, plot=False, **kwargs)


class AmbiguityError(Exception):
    pass
