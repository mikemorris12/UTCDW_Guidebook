"""
DBCCA.py

code for implementing the Double Bias-Corrected Constructed Analogues
statistical downscaling method (Werner & Cannon, 2016)

"""

import os
import numpy as np 
import xarray as xr
import xclim.sdba as sdba
from xclim.core.calendar import convert_calendar

from BCCA import BCCA, bias_correct_gcm


def DBCCA(data_gcm_hist, data_gcm_future, data_obs_fine, varname,
          units = 'mm/day', convert_obs_calendar = True,
          n_analogues = 30, window_size = 45, window_unit = 'days', 
          bc_method_bcca = 'DQM', bc_method_dbcca = "QDM", bc_grouper = 'time.month', bc_kind = '+', bc_nquantiles = 20,
          metric = 'RMSE', penalty = 'l2', jitter = False, jitter_thresh = '0.1 mm/d', transform = None,
          write_output = False, fout_hist_bcca = None, fout_future_bcca = None, 
          fout_hist_dbcca = None, fout_future_dbcca = None, 
          do_future = True):
    """
    Apply the DBCCA method do downscale data_gcm_hist and data_gcm_future: downscale with BCCA then apply
    quantile mapping bias correction to the output of BCCA.

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
    * bc_method_bcca ({'DQM', 'QDM', 'EQM'}) - Quantile mapping bias-correction method to be deployed in the first BC step. Default is 'DQM'.
    * bc_method_dbcca ({'DQM', 'QDM', 'EQM'}) - Quantile mapping bias-correction method to be deployed in the second BC step. Default is 'QDM'.
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
    * fout_hist_bcca (str): File path to write the BCCA output for the historical reference period (Optional).
    * fout_future_bcca (str) - File path to write the BCCA output for the future projection period (Optional).   
    * fout_hist_dbcca (str): File path to write the DBCCA output for the historical reference period (Optional).
    * fout_future_dbcca (str) - File path to write the DBCCA output for the future projection period (Optional).  
    * do_future (bool) - If True, downscale both data_gcm_hist and data_gcm_future. Otherwise, only do BCCA on data_gcm_hist. 
      BCCA will still return two xr.DataArrays, one being a copy of the downscaled historical data in place of the downscaled future data.
      Default is True.
      
    """

    # downscale with BCCA, unless it's already been done
    if (not os.path.exists(fout_hist_bcca)) or (not os.path.exists(fout_future_bcca)):
        data_gcm_hist_bcca, data_gcm_future_bcca = BCCA(data_gcm_hist, data_gcm_future, data_obs_fine,
                                                        units = units, convert_obs_calendar = convert_obs_calendar,
                                                        n_analogues = n_analogues, window_size = window_size, window_unit = window_unit, 
                                                        bc_method = bc_method_bcca, bc_grouper = bc_grouper, bc_kind = bc_kind, bc_nquantiles = bc_nquantiles,
                                                        metric = metric, penalty = penalty, jitter = jitter, jitter_thresh = jitter_thresh, transform = transform,
                                                        write_output = write_output, fout_hist = fout_hist_bcca, fout_future = fout_future_bcca, 
                                                        do_future = do_future
                                                        )
    
   
    if write_output: 
        # need to open files written from BCCA, since write_output makes it return None's
        ds_gcm_hist_bcca = xr.open_dataset(fout_hist_bcca)
        if do_future:
            ds_gcm_future_bcca = xr.open_dataset(fout_future_bcca)
        else:
            ds_gcm_future_bcca =  data_gcm_hist_bcca

        # get the data out in xr.DataArray format
        data_gcm_hist_bcca = ds_gcm_hist_bcca[varname]
        data_gcm_future_bcca = ds_gcm_future_bcca[varname]

    # otherwise the BCCA data was returned by the BCCA function call above

    # assign unit attribute to data
    data_gcm_hist_bcca.attrs['units'] = units
    data_gcm_future_bcca.attrs['units'] = units
    data_obs_fine.attrs['units'] = units

    # convert obs calendar to exclude leap years
    if convert_obs_calendar:
        data_obs_fine = convert_calendar(data_obs_fine, target = 'noleap')

     # do the second bias correction
    print(f'doing {bc_method_dbcca} bias correction to BCCA data')
    data_gcm_hist_dbcca, data_gcm_future_dbcca = bias_correct_gcm(data_gcm_hist_bcca, data_gcm_future_bcca, data_obs_fine,
                                                                  method = bc_method_dbcca, 
                                                                  kind = bc_kind,
                                                                  nquantiles = bc_nquantiles,
                                                                  grouper = bc_grouper)
    
    # re-name "scen" variable that xclim names the bias-corrected output to the obs variable name
    data_gcm_hist_dbcca = data_gcm_hist_dbcca.rename(varname)
    data_gcm_future_dbcca = data_gcm_future_dbcca.rename(varname)
    
    # write output
    if write_output:
        print("Writing Output")
        data_gcm_hist_dbcca.to_netcdf(fout_hist_dbcca)
        if do_future:
            data_gcm_future_dbcca.to_netcdf(fout_future_dbcca)
        # return None's if output has been written
        return None, None 

    # otherwise return the bias corrected downscaled data
    else: 
        return data_gcm_hist_dbcca, data_gcm_future_dbcca


    
    

