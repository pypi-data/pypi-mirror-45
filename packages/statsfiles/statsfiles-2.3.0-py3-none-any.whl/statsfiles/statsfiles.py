# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:03:34 2016

@author: Charles-David Hebert
"""

import time
import os
import sys
import pkg_resources
import yaml

from . import statsobs
from . import statsarrays
from . import statsparams
from . import copy_essential


yy_params_default = yaml.load(
        pkg_resources.resource_string(__name__, "data/cdh_params.yml"),  Loader=yaml.FullLoader)

def run_statsfiles(iter_start: int, yy_params=yy_params_default) -> None:

    out_dir = time.strftime("Stats" + "-%Y-%m-%d--%Hh%M")
    os.mkdir(out_dir)

    obs_files = yy_params["obs_files"]

    array_files = yy_params["array_files"]["names"]
    array_files_middles = yy_params["array_files"]["middles"]
    array_files_exts = yy_params["array_files"]["exts"]

    params_files = yy_params["param_files"]["names"]

    # One list per element in param_files: parameters
    params_names_l = yy_params["param_files"]["parameters"]

    # do the stats for arrays
    if any(array_files):
        starr = statsarrays.StatsArrays(array_files=array_files,
                                        middle_files=array_files_middles,
                                        ext_files=array_files_exts, iter_start=iter_start,
                                        ignore_col=None, in_dir=os.getcwd(),
                                        warning_only=True)

        starr.mean()
        starr.std()
        starr.write_results(out_dir=out_dir, file_out="statsobs.json")

    # do the stats for observables files
    if any(obs_files):
        stobs = statsobs.StatsObs(obs_files=obs_files, iter_start=iter_start, ignore_col=0, in_dir=os.getcwd(),
                                  warning_only=True)

        stobs.mean()
        stobs.std()
        stobs.write_results(out_dir=out_dir, file_out="statsobs.json")

    # do the stats for the parameter files
    if any(params_files):
        stparams = statsparams.StatsParams(params_files=params_files, params_names_l=params_names_l,
                                           ext="", iter_start=iter_start, in_dir=os.getcwd(),
                                           warning_only=True)

        stparams.mean()
        stparams.std()
        stparams.write_results(out_dir, "statsparams.json")

    # copy the essential files
    ce = copy_essential.CopyEssential(out_dir)
    ce.run()
