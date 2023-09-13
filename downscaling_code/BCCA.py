"""
BCCA.py

code for implementing the Bias-Corrected Constructed Analogues
statistical downscaling method (Werner & Cannon, 2016)
"""
import dask
import numpy as np 
import xarray as xr
import xclim.sdba as sdba
from xclim.core.calendar import convert_calendar
import xskillscore as xs
import pandas as pd
import xesmf as xe
from dask_ml.linear_model import LinearRegression



def coarsen_obs(obs, ds_coarse, method = 'bilinear', regridder = None, return_regridder = False):
    """
    re-grid  high-resolution observations to the coarser grid of the 
    GCM data that is to be downscaled. Optionally return the xesmf.Regridder object to 
    save time and re-use it if necessary.

    * obs (xr.Dataset or xr.DataArray) - the high-res obs to be coarsened
    * ds_coarse (xr.Dataset or xr.DataArray) - an xarray object which contains the latitude and longitude values
      for the GCM grid (destination grid for the regridding)
    * method ({'bilinear', 'conservative', 'conservative_normed', 'patch', 'nearest_s2d', 'nearest_d2s'}) -
      regridding method to be used, must be one implemented in xesmf.Regridder. Default is 'bilinear'.
    * regridder (Optional, xesmf.Regridder) - A previously generated Regridder object which maps the grid of obs to that of ds_coarse.
    * return_regridder (bool) - If True, return both the regridded obs data AND the xesmf.Regridder object. Default is False.
    """

     # generate the xe.Regridder object if it wasn't passed as an argument
    if regridder is None:
        lats = ds_coarse.lat.values
        lons = ds_coarse.lon.values
        ds_grid = xr.Dataset({'lat': (['lat'], lats), 'lon': (['lon'], lons)})
        regridder = xe.Regridder(obs, ds_grid, method)

    # re-grid the high-res obs to the coarse grid of the model data
    obs_coarse = regridder(obs)

    if return_regridder: # return both the coarsened observations AND the regridder object
        out = (obs_coarse, regridder)
    else: # return only the coarsened observations
        out = obs_coarse
    
    return out



def bias_correct_gcm(gcm_hist, gcm_future, obs_data, method = 'DQM', grouper = 'time.month', kind = '+', nquantiles = 20):
    """
    Apply a quantile mapping based bias correction to the raw GCM data using obs_data as the reference dataset. 
    Bias correction method is default Detrended Quantile Mapping, but can be any of the three quantile mapping methods 
    implemented in xclim.sdba

    * gcm_hist (xr.DataArray) - Raw GCM data for the historical baseline period. Must have an appropriate 'units' attribute.
    * gcm_future (xr.DataArray) - Raw GCM data for the future projection period. Must have the same units as gcm_hist.
    * obs_data (xr.DataArray) - Observational data coarsened to the raw GCM grid. Must have the same units as gcm_hist.
    * method ({'DQM', 'QDM', 'EQM'}) - Quantile mapping bias-correction method to be deployed. Default is 'DQM'.
    * grouper (Union[str, xclim.sdba.base.Grouper]). The grouping information. See xclim.sdba.base.Grouper for details. 
      Default is “time.month”, meaning data is grouped by the month of the year before applying the adjustments separately
      to each group.
    * kind ({'+', '*'}) - Type of adjustment to apply, additive or multaplicative. Default is "+".
    * nquantiles (int or 1d array of floats) - The number of quantiles to use. An array of quantiles [0, 1] can also be passed. 
      Defaults to 20 quantiles.
    
    """

    if method == "DQM":
        BiasAdjuster = sdba.DetrendedQuantileMapping
    elif method == "QDM":
        BiasAdjuster = sdba.QuantileDeltaMapping
    elif method == "EQM":
        BiasAdjuster = sdba.EmpiricalQuantileMapping

    TrainedBiasAdjuster = BiasAdjuster.train(obs_data, gcm_hist, group = grouper, kind = kind, nquantiles = nquantiles)

    gcm_hist_adjusted = TrainedBiasAdjuster.adjust(gcm_hist)
    gcm_future_adjusted = TrainedBiasAdjuster.adjust(gcm_future)

    return gcm_hist_adjusted, gcm_future_adjusted


def get_metric_func(metric = "RMSE"):
    """
    Return the function to be used to evaluate similarity between GCM data
    for a given timestep and the candidate analogue observations. 
    Currently only root mean-squared-error (RMSE) is supported.

    * metric ({'RMSE'}) - the metric to be used. Defaults to "RMSE".
    
    """

    if metric == "RMSE":
        func = xs.rmse
    else:
        print('not yet implemented')
        func = None
    return func



def get_time_mapper(window_size, window_unit = "days"):
    """
    * window_size (int) - The maximum number of timesteps away from the time of year of field_gcm
    that candidate analogues can be selected. 
    * window_unit ({'day'}) - the unit of time associated with window_size. 
    Currently only 'day' is supported, i.e. all obs candidates must be within +/- window_size number of days.
    """
    # initially only implement a window with units of days
    out = {}
    if window_unit == 'days':
        dayofyear = range(1, 366)
        for day in dayofyear:
            daymin = (day - window_size - 365) % 365
            daymax = (day + window_size + 365) % 365
             
            if daymin > daymax: # if the window size crosses over two years, the start day will be greater than the end day
                dayrange = np.append(np.arange(daymin, 366), np.arange(1, daymax + 1))
            else:
                dayrange = np.arange(daymin, daymax + 1)   
            out[day] = dayrange
    else:
        print('non-daily windows not supported')
        out = None

    return out                    


def get_obs_candidates(obs, gcm_time, time_mapper, window_unit):
    """
    select observed times within window_size number of window_units of gcm_time

    * obs (xr.DataArray): The data from which the observed analogues will be selected
    * gcm_time (datetime): The timestamp of the GCM pattern to be downscaled
    * time_mapper (dict) - Dictionary mapping the day of the year to the range of days from which analogues can be selected.
    * window_unit ({'day'}) - the unit of time associated with window_size. 
    Currently only 'day' is supported, i.e. all obs candidates must be within +/- window_size number of days.
    """

    if window_unit == 'days':
        timerange = time_mapper[int(gcm_time.dt.dayofyear)]
        out = obs.sel(time = obs.time.dt.dayofyear.isin(timerange))
    else:
        print('non-daily windows not supported')
        out = None

    return out


def find_analogues_onetime(field_gcm, obs_coarse, time_mapper, n_analogues = 30, 
                           window_unit = 'days', metric = 'RMSE', transform = None):
    """
    return the n_analogues observed days which best match field_gcm 
    as measured by metric

    * field_gcm (xr.DataArray) - The GCM data you're looking to find obs analogues for.
    * obs_coarse (xr.DataArray) - The library of all observational data from which analogues
      could be selected. Must have the same dimensions and size as field_gcm.
    * time_mapper (dict) - Dictionary mapping the day of the year to the range of days from which analogues can be selected.
    * n_analogues (int) - The number of analogues to be selected. Defaults to 30. 
    * window_unit ({'day'}) - the unit of time associated with window_size. 
      Currently only 'day' is supported, i.e. all obs candidates must be within +/- window_size number of days.
    * metric ({'RMSE'}) - The metric used to measure similarity between field_gcm and the candidate analogues.
      Currently only "RMSE" is supported.
    * transform ({'sqrt'}) - The name of a function to be used to transform field_gcm and obs_coarse before selecting
      analogues. Currently only 'sqrt' is supported. This is to be used to ensure positive semidefinite quantities
      such as precipitation do not yield negative values in the downscaled data (Optional).
    """
    
    # select observations within a similar part of the year to the simulated time
    gcm_time = field_gcm.time
    obs_candidates = get_obs_candidates(obs_coarse, gcm_time, time_mapper, window_unit)

    # transform the fields if necessary
    if transform == 'sqrt':
        field_gcm = np.sqrt(field_gcm)
        obs_coarse = np.sqrt(obs_coarse)

    # calculate the similarity metric between the candidate observations and the GCM time
    metric_func = get_metric_func(metric)
    measures = metric_func(field_gcm, obs_candidates, dim = ['lat', 'lon'])

    # sort the metrics and select the times with the n_analogues best scores
    measures_sorted = measures.sortby(measures, ascending = True)
    analogue_times = measures_sorted.isel(time = slice(0, n_analogues)).time#.to_dataset(name = 'atime')
    obs_analogues = obs_candidates.sel(time = analogue_times)

    # format the times into a way that they can be concattenated by the model time
    # and then return
    #analogue_times = analogue_times.rename({'time': 'analogue_index'})
    #analogue_times = analogue_times.reset_index('analogue_index')
    #analogue_times = analogue_times.assign_coords(time = gcm_time)

    #return analogue_times
    return obs_analogues


def get_analogue_weights(field_gcm, obs_analogues, #obs_coarse, analogue_times, 
                         penalty = 'l2', jitter = False, jitter_thresh = '0.1 mm/d', transform = None):
    """
    get the  weights to use in the linear combination of the obs patterns to construct the downscaled field, 
    using least squares regression (possibly with an L2 penalty, i.e. ridge regression).

    * field_gcm (xr.DataArray) - The GCM data you're looking to find obs analogues for.
    * obs_coarse (xr.DataArray) - The library of all observational data from which analogues
      could be selected. Must have the same dimensions and size as field_gcm.
    * analogue_times (array of datetime objects) - Timestamps of observed analogues to contribute to the
      downscaled constructed analogue.
    * penalty {'l1', 'l2', None} - Regularization to be applied in the regression which solves for the analogue weights.
    * jitter (bool) - If True, replace values below jitter_thresh with uniform random noise. Defaults to False.
    * jitter_thresh (str) - Threshold for applying jittering, with units included. Defaults to '0.1 mm/day'.
    * transform ({'sqrt'}) - The name of a function to be used to transform field_gcm and obs_coarse before selecting
      analogues. Currently only 'sqrt' is supported. This is to be used to ensure positive semidefinite quantities
      such as precipitation do not yield negative values in the downscaled data (Optional).
    """

    # select observations for the analogue times
    #obs_analogues = obs_coarse.sel(time = analogue_times.atime)

    # flatten data to 1D spatially for use with LinearRegression routine
    gcm_flat = field_gcm.stack(space = ('lat', 'lon'))
    obs_flat = obs_analogues.stack(space = ('lat', 'lon'))

    # fill NaN's with zeros so LinearRegression doesn't complain
    gcm_flat = gcm_flat.fillna(0)
    obs_flat = obs_flat.fillna(0)

    if jitter: # for precip data, replace small values with uniform random noise.
        gcm_flat = sdba.processing.jitter_under_thresh(gcm_flat, jitter_thresh)
        obs_flat = sdba.processing.jitter_under_thresh(obs_flat, jitter_thresh)

    if transform == 'sqrt': # apply square root transform to ensure positive valued output.
        gcm_flat = np.sqrt(gcm_flat)
        obs_flat = np.sqrt(obs_flat)

    # fit linear regression with the appropriate regularization, without any constant intercept offset.
    lr = LinearRegression(fit_intercept = False, penalty = penalty).fit(obs_flat.data.T, gcm_flat.data)

    # store weights in an xr.DataArray, with coords matching the times of the 
    # obs patterns to be combined
    weights = xr.DataArray(lr.coef_, dims = ['time'], coords = [obs_analogues.time])#coords = [analogue_times.atime])

    return weights


def apply_analogue_weights(obs_fine, weights, transform = None):
    """
    Calculate the linear combination of high-res observed patterns
    to produce the downscaled pattern

    * obs_fine (xr.DataArray) - High-resolution observations which will be used to produce the 
      downscaled output
    * weights (xr.DataArray) - Array of weights used to linearly combine the observed analogues
    * transform ({'sqrt'}) - The name of a function to be used to transform field_gcm and obs_coarse before selecting
      analogues. Currently only 'sqrt' is supported. This is to be used to ensure positive semidefinite quantities
      such as precipitation do not yield negative values in the downscaled data.
    """

    # apply transform if necessary
    if transform == 'sqrt':
        obs_fine = np.sqrt(obs_fine)

    # linearly combine the high-res obs analogues
    #out = obs_fine.sel(time = weights.time).weighted(weights).sum('time')
    out = obs_fine.weighted(weights).sum('time')

    # undo the transform, if it was applied
    if transform == 'sqrt':
        out = np.square(out)

    # re-mask where data should be missing, i.e. if obs are missing
    out = out.where(~obs_fine.isel(time = 0).isnull())

    # return the downscaled output
    return out

#@dask.delayed
def construct_analogue_onetime(field_gcm, obs_coarse, obs_fine, time_mapper,
                               n_analogues = 30, window_unit = 'days', metric = 'RMSE', 
                               penalty = 'l2', jitter = False, jitter_thresh = '0.1 mm/d', transform = None):
    """
    Apply the constructed analogues algorithm for a single model time step. This is basically a wrapper for the whole 
    constructed analogues method, but only for a single time step.

    * field_gcm (xr.DataArray) - The GCM data for a single timestep, to be downscaled using CA.
    * obs_coarse (xr.DataArray) - The training observations from which analogues will be selected,
      on the same coarse grid as field_gcm
    * obs_fine (xr.DataArray) - The original high-resolution observations, to be used to
      produce the high-res downscaled data.
    * time_mapper (dict) - Dictionary mapping the day of the year to the range of days from which analogues can be selected.
    * n_analogues (int) - The number of analogues that will contribute to the downscaled pattern. Defaults to 30.
    * window_unit ({'day'}) - the unit of time associated with window_size. 
      Currently only 'day' is supported, i.e. all obs candidates must be within +/- window_size number of days.
    * metric ({'RMSE'}) - The metric used to measure similarity between field_gcm and the candidate analogues.
      Currently only "RMSE" is supported.
    * penalty {'l1', 'l2', None} - Regularization to be applied in the regression which solves for the analogue weights.
    * jitter (bool) - If True, replace values below jitter_thresh with uniform random noise. Defaults to False.
    * jitter_thresh (str) - Threshold for applying jittering, with units included. Defaults to '0.1 mm/day'.
    * transform ({'sqrt'}) - The name of a function to be used to transform field_gcm and obs_coarse before selecting
      analogues. Currently only 'sqrt' is supported. This is to be used to ensure positive semidefinite quantities
      such as precipitation do not yield negative values in the downscaled data (Optional).
    """

    #analogue_times = find_analogues_onetime(field_gcm, obs_coarse, time_mapper,
    #                                        n_analogues = n_analogues, window_unit = window_unit,
    #                                        metric = metric, transform = transform)

    #weights = get_analogue_weights(field_gcm, obs_coarse, analogue_times, penalty = penalty, 
    #                               jitter = jitter, jitter_thresh = jitter_thresh, transform = transform)

    # new: return the actual coarse obs analogues instead of the timestamps
    obs_analogues = find_analogues_onetime(field_gcm, obs_coarse, time_mapper,
                                            n_analogues = n_analogues, window_unit = window_unit,
                                            metric = metric, transform = transform)

    weights = get_analogue_weights(field_gcm, obs_analogues, penalty = penalty, 
                                   jitter = jitter, jitter_thresh = jitter_thresh, transform = transform)

    constructed_analogue = apply_analogue_weights(obs_fine, weights, transform = transform)
    constructed_analogue['time'] = field_gcm.time

    return constructed_analogue


def construct_analogues(data_gcm, obs_coarse, obs_fine,
                        n_analogues = 30, window_size = 45, window_unit = 'days', metric = 'RMSE', 
                        penalty = 'l2', jitter = False, jitter_thresh = '0.1 mm/d', transform = None,
                        fout = None, write_output = False):
    """
    Apply construct_analogue_onetime over many timesteps. Wrapper for construct_analogue_onetime.

    * data_gcm (xr.DataArray) - The GCM data to be downscaled using CA.
    * obs_coarse (xr.DataArray) - The training observations from which analogues will be selected,
      on the same coarse grid as field_gcm
    * obs_fine (xr.DataArray) - The original high-resolution observations, to be used to
      produce the high-res downscaled data.
    * n_analogues (int) - The number of analogues that will contribute to the downscaled pattern. Defaults to 30.
    * window_size (int) - The maximum number of timesteps away from the time of year of field_gcm
      that candidate analogues can be selected. 
    * window_unit ({'day'}) - the unit of time associated with window_size. 
      Currently only 'day' is supported, i.e. all obs candidates must be within +/- window_size number of days.
    * metric ({'RMSE'}) - The metric used to measure similarity between field_gcm and the candidate analogues.
      Currently only "RMSE" is supported.
    * penalty {'l1', 'l2', None} - Regularization to be applied in the regression which solves for the analogue weights.
    * jitter (bool) - If True, replace values below jitter_thresh with uniform random noise. Defaults to False.
    * jitter_thresh (str) - Threshold for applying jittering, with units included. Defaults to '0.1 mm/day'.
    * transform ({'sqrt'}) - The name of a function to be used to transform field_gcm and obs_coarse before selecting
      analogues. Currently only 'sqrt' is supported. This is to be used to ensure positive semidefinite quantities
      such as precipitation do not yield negative values in the downscaled data.
    * transform ({'sqrt'}) - The name of a function to be used to transform data_gcm and obs_coarse before selecting
      analogues. Currently only 'sqrt' is supported. This is to be used to ensure positive semidefinite quantities
      such as precipitation do not yield negative values in the downscaled data (Optional).
    * fout (str): File path to write output to (Optional)
    * write_output (bool) - If True, write output to fout and return None. Otherwise, return the downscaled data.

    """
    # create dict mapping dayofyear to the time window from which candidate obs can be selected
    time_mapper =  get_time_mapper(window_size, window_unit = "days")
    # time-step by time-step, make the constructed analogues (this could probably be optimized better than a for loop)
    da_list = []
    for t in data_gcm.time:
         CA_sample = construct_analogue_onetime(data_gcm.sel(time = t),
                                                obs_coarse,
                                                obs_fine,
                                                time_mapper,
                                                metric = metric,
                                                n_analogues = n_analogues,
                                                window_size = window_size,
                                                window_unit = window_unit,
                                                jitter = jitter,
                                                jitter_thresh = jitter_thresh, 
                                                transform = transform, 
                                                penalty = penalty)
         da_list.append(CA_sample)

   # concatenate all the downscaled data together over the time dimension
    data_CA = xr.concat(da_list, dim = 'time')

    if write_output:
        data_CA.to_netcdf(fout)
        return None
    else:
        return data_CA


def BCCA(data_gcm_hist, data_gcm_future, data_obs_fine,
         units = "mm/day",
         convert_obs_calendar = True,
         n_analogues = 30, window_size = 45, window_unit = 'days', 
         bc_method = 'DQM', bc_grouper = 'time.month', bc_kind = '+', bc_nquantiles = 20,
         metric = 'RMSE', penalty = 'l2', jitter = False, jitter_thresh = '0.1 mm/d', transform = None,
         write_output = False, fout_hist = None, fout_future = None, do_future = True):
    """
    Apply the BCCA algorithm to downscale data_gcm_hist and data_gcm_future.

    * data_gcm_hist (xr.DataArray) - The GCM data to be downscaled, for the historical baseline period.
    * data_gcm_future (xr.DataArray) - The GCM data to be downscaled, for the future projection period.
    * data_obs_fine (xr.DataArray) - The high-resolution observational data to be used for downscaling.
    * units (str) - The units of the variable being downscaled, must be physically consistent with the 
      units of the three input DataArrays. Default: 'mm/day'.
    * convert_obs_calendar (bool) - If True, convert the calendar of the observational data timestamps
      (likely Gregorian) to exclude leap days, like most GCM calendars. Default: True.
    * n_analogues (int) - The number of analogues that will contribute to the downscaled pattern. Defaults to 30.
    * window_size (int) - The maximum number of timesteps away from the time of year of field_gcm
      that candidate analogues can be selected. 
    * window_unit ({'day'}) - the unit of time associated with window_size. 
      Currently only 'day' is supported, i.e. all obs candidates must be within +/- window_size number of days.
    * bc_method ({'DQM', 'QDM', 'EQM'}) - Quantile mapping bias-correction method to be deployed. Default is 'DQM'.
    * bc_grouper (Union[str, xclim.sdba.base.Grouper]). The grouping information for bias-correction. See xclim.sdba.base.Grouper for details. 
      Default is “time.month”, meaning data is grouped by the month of the year before applying the adjustments separately
      to each group.
    * bc_kind ({'+', '*'}) - Type of adjustment to apply in the bias-correction step, additive or multaplicative. Default is "+".
    * bc_nquantiles (int or 1d array of floats) - The number of quantiles to use. An array of quantiles [0, 1] can also be passed. 
      Defaults to 20 quantiles.
    * metric ({'RMSE'}) - The metric used to measure similarity between field_gcm and the candidate analogues.
      Currently only "RMSE" is supported.
    * penalty {'l1', 'l2', None} - Regularization to be applied in the regression which solves for the analogue weights.
    * jitter (bool) - If True, replace values below jitter_thresh with uniform random noise. Defaults to False.
    * jitter_thresh (str) - Threshold for applying jittering, with units included. Defaults to '0.1 mm/day'.
    * transform ({'sqrt'}) - The name of a function to be used to transform the data before selecting
      analogues. Currently only 'sqrt' is supported. This is to be used to ensure positive semidefinite quantities
      such as precipitation do not yield negative values in the downscaled data (Optional).
    * write_output (bool) - If True, write output to netCDF files and return None. Otherwise, return the downscaled data.
    * fout_hist (str): File path to write downscaled data for the historical reference period (Optional).
    * fout_future (str) - File path to write downscaled data for the future projection period (Optional).   
    * do_future (bool) - If True, downscale both data_gcm_hist and data_gcm_future. Otherwise, only do BCCA on data_gcm_hist. 
      BCCA will still return two xr.DataArrays, one being a copy of the downscaled historical data in place of the downscaled future data.
      Default is True.
      
    """
    # assign unit attribute to data
    data_gcm_hist.attrs['units'] = units
    data_gcm_future.attrs['units'] = units
    data_obs_fine.attrs['units'] = units

    # convert obs calendar to exclude leap years
    if convert_obs_calendar:
        data_obs_fine = convert_calendar(data_obs_fine, target = 'noleap')

    # coarsen obs to GCM grid
    print('coarsening obs')
    data_obs_coarse = coarsen_obs(data_obs_fine, data_gcm_hist)

    # add back units to obs
    data_obs_coarse.attrs['units'] = data_gcm_hist.units

    # mask GCM where obs are missing
    data_gcm_hist = data_gcm_hist.where(~np.isnan(data_obs_coarse.isel(time = 0)))
    data_gcm_future = data_gcm_future.where(~np.isnan(data_obs_coarse.isel(time = 0)))

    # bias-correct the GCM data
    print(f'doing {bc_method} bias correction to coarse GCM data')
    data_gcm_hist_bc, data_gcm_future_bc = bias_correct_gcm(data_gcm_hist, data_gcm_future, data_obs_coarse,
                                                            method = bc_method, 
                                                            kind = bc_kind,
                                                            nquantiles = bc_nquantiles,
                                                            grouper = bc_grouper)
    
    # get the downscaled data
    print('constructing analogues for historical period')
    data_gcm_hist_CA = construct_analogues(data_gcm_hist_bc, data_obs_coarse, data_obs_fine,
                                            n_analogues = n_analogues,
                                            window_size = window_size,
                                            window_unit = window_unit,
                                            metric = metric,
                                            jitter = jitter,
                                            jitter_thresh = jitter_thresh, 
                                            transform = transform, 
                                            penalty = penalty,
                                            write_output = write_output,
                                            fout = fout_hist)
    if do_future:
        print('constructing analogues for future period')
        data_gcm_future_CA = construct_analogues(data_gcm_future_bc, data_obs_coarse, data_obs_fine,
                                                 n_analogues = n_analogues,
                                                 window_size = window_size,
                                                 window_unit = window_unit,
                                                 metric = metric,
                                                 jitter = jitter,
                                                 jitter_thresh = jitter_thresh, 
                                                 transform = transform, 
                                                 write_output = write_output,
                                                 fout = fout_future)
    else:
        data_gcm_future_CA = data_gcm_future
    
    print('done')
    return data_gcm_hist_CA, data_gcm_future_CA







