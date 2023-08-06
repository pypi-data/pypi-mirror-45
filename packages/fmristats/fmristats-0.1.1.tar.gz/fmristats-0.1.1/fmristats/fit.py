# Copyright 2016-2018 Thomas W. D. Möbius
#
# This file is part of fmristats.
#
# fmristats is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# fmristats is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# It is not allowed to remove this copy right statement.

"""

Fit signal model to signal data

"""

import time

from numba import jit, njit

import numpy as np

from numpy.linalg import solve, inv

from pandas import DataFrame

import statsmodels.api as sm

import statsmodels.formula.api as smf

from statsmodels.stats.stattools import durbin_watson

########################################################################

def design_AT(coordinate, data, design, scale:float, radius:float):
    r = radius**2
    s = -2*scale**2
    squared_distances = ((data[...,:3] - coordinate)**2).sum(axis=1)
    valid = np.where(squared_distances < r)
    weights = np.exp(squared_distances[valid] / s)
    data = data[valid]
    design = design[valid]
    return data, design, weights

def model_AT(hasconst, **kwargs):
    data, design, weights = design_AT(**kwargs)
    print('Design has constant: {}'.format(hasconst))
    return sm.WLS(
        endog    = data[...,3],
        exog     = design,
        weights  = weights,
        hasconst = hasconst)

def fit_AT(hasconst, **kwargs):
    return model_AT(hasconst=hasconst, **kwargs).fit()

########################################################################

def data_at(coordinate, data, epi_code:int, scale:float, radius:float):
    r = radius**2
    s = -2*scale**2
    squared_distances = ((data[...,:3] - coordinate)**2).sum(axis=1)
    valid = np.where(squared_distances < r)
    weights = np.exp(squared_distances[valid] / s)
    data = data[valid]

    df = DataFrame({
        'x'      : data[...,0],
        'y'      : data[...,1],
        'z'      : data[...,2],
        'signal' : data[...,3],
        'time'   : data[...,4],
        'task'   : data[...,5],
        'block'  : data[...,6],
        'cycle'  : data[...,7],
        'slice'  : data[...,8],
        'weight' : weights})

    if abs(epi_code) == 3:
        sortvar = ['time', 'z', 'x', 'y']
    elif abs(epi_code) == 2:
        sortvar = ['time', 'y', 'z', 'x']
    elif abs(epi_code) == 1:
        sortvar = ['time', 'x', 'y', 'z']

    df.sort_values(by=sortvar, inplace=True)

    return df

def model_at(formula, **kwargs):
    data = data_at(**kwargs)
    data.dropna(inplace=True)
    print(data)
    print(formula)
    model = smf.wls(formula, weights=data.weight, data=data)
    return model, data

def fit_at(formula, **kwargs):
    model, data = model_at(formula=formula, **kwargs)
    fit = model.fit()

    data['expected_signal'] = fit.predict()
    data['residual'] = fit.resid
    data['weighted_residual'] = data.weight * fit.resid
    fit.durbin_watson = durbin_watson(data.weighted_residual)

    return fit, model, data

########################################################################

def extract_field(field, param, value, parameter_dict, value_dict):
    return field[..., value_dict[value], parameter_dict[param]]

def fit_field(coordinates, mask, data, design, epi_code:int,
        scale:float, radius:float, verbose=True, backend='numba'):
    """
    Parameters
    ----------
    coordinates : ndarray, shape (…,3)
        The coordinates at which the models shall be fitted. Must be a
        numpy array of which the last dimension must be 3.
    mask : None or ndarray, shape (…)
        A boolean array of the same »layout« as coordinates. The first
        dimensions must match the dimensions of coordinates. If None,
        the model is fitted at all coordinates.
    data : ndarray, shape (…,9), dtype: float
        The array of observations:
            - [...,:3] = coordinates of observation
            - [..., 3] = MR signal response
            - [..., 4] = time of observation
            - [..., 5] = task during time of observation
            - [..., 6] = block number during time of observation
            - [..., 7] = scan cycle
            - [..., 8] = slice number
    design : ndarray, shape (…,p), dtype: float
        The design matrix.
    epi_code : int
    scale : float
    radius : float
    verbose : bool
    """

    ###################################################################
    # Asserts
    ###################################################################

    assert coordinates.shape[:-1] == mask.shape, \
            'shapes of coordinates and mask do not match'
    assert data.shape[:-1] == design.shape[:-1], \
            'shapes of data and design do not match'
    assert epi_code in [-3,-2,-1,1,2,3], 'epi_code must be within [-3,3] but not 0'

    ###################################################################
    # In case you need the Durbin-Watson statistics
    ###################################################################

    if backend == 'statsmodels':
        if abs(epi_code) == 3:
            sortvar = ['time', 'z', 'x', 'y']
        elif abs(epi_code) == 2:
            sortvar = ['time', 'y', 'z', 'x']
        elif abs(epi_code) == 1:
            sortvar = ['time', 'x', 'y', 'z']

    ###################################################################
    # Hyperparameters
    ###################################################################

    r = radius**2
    s = -2*scale**2
    p = design.shape[-1]

    ###################################################################
    # Statistics field
    ###################################################################

    params     = np.zeros(coordinates.shape[:-1] + (p,))
    cov_params = np.zeros(coordinates.shape[:-1] + (p, p))
    mse        = np.zeros(coordinates.shape[:-1] + (2,))

    params     [...] = np.nan
    cov_params [...] = np.nan
    mse        [...] = np.nan

    ###################################################################
    # Reshape
    ###################################################################

    rcoordinates = coordinates.reshape((-1,3))
    rparams      = params.reshape((-1,p))
    rcov_params  = cov_params.reshape((-1,p,p))
    rmse         = mse.reshape((-1,2))

    if mask is None:
        to_fit = np.ones(rcoordinates.shape[0]).astype(bool)
    else:
        to_fit = mask.reshape((-1,))

    ###################################################################
    # Fit the model
    ###################################################################

    fit_nb(rcoordinates, rparams, rcov_params, rmse, to_fit, data,
            design, r, s)

    return params, cov_params, mse

###################################################################
# Backend
###################################################################

@jit(nopython=True)
def penrose_fit(endog, exog, weights):
    # set up
    w_half        = np.sqrt(weights)
    wendog        = w_half * endog
    wexog         = w_half.reshape((-1,1)) * exog
    # calculation
    pinv_wexog    = np.linalg.pinv(wexog)
    params        = pinv_wexog.dot(wendog)
    fitted_values = exog.dot(params)
    wresid        = wendog - wexog.dot(params)
    df_resid      = wexog.shape[0] - wexog.shape[1]
    mse           = np.dot(wresid, wresid) / df_resid
    # variances, covariances, and standard errors
    cov_params    = mse * np.dot(pinv_wexog, np.transpose(pinv_wexog))
    return params, cov_params, mse, df_resid

@jit(nopython=True, fastmath=True) #, parallel=True)
def fit_nb(rcoordinates:np.array, rparams:np.array,
        rcov_params:np.array, rmse:np.array, to_fit:np.array,
        data:np.array, design:np.array, r:float, s:float):
    for i in range(rcoordinates.shape[0]):
        if to_fit[i]:
            squared_distances = ((data[...,:3] - rcoordinates[i])**2).sum(axis=1)
            valid = np.where(squared_distances < r)
            weights = np.exp(squared_distances[valid] / s)
            endog   = data[valid][...,3]
            exog    = design[valid]
            n = exog.shape[0]
            p = exog.shape[1]
            if (p < n-1) and (np.linalg.matrix_rank(exog) == p):
                params, cov_params, mse, df_resid = penrose_fit(endog, exog, weights)
                rparams[i] = params
                rcov_params[i] = cov_params
                rmse[i] = mse, float(df_resid)
