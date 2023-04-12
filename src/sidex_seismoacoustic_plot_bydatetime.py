# ###############################################################
# plot_seismoacousticdata_bydatetime
# Purpose: example code for plotting geophone and hydrophone data using a date string
# April 1, 2023
# Author:
# Erin Fischell, PhD
# Senior Scientist
# JPAnalytics
#
#
# This work was supported by the US Office of Naval Research
#
# questions? contact: efischell@gmail.com
#
# ###############################################################

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import glob

import sidex_utils

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
datestruse='0305T2300'

filelist_rawcsv_geophones = sorted(glob.glob('/kaggle/input/*/geophones_' + datestruse + '*.csv'))
# plot GPS and relative locations as example:
sidex_utils.plot_rel_locations(outfile='/kaggle/working/cabled_array_locations.png')
sidex_utils.plot_GPS_v_time(outfile='/kaggle/working/SIDEx_GPS_vtime.png')
for filen in filelist_rawcsv_geophones:
    print('plotting ' + str(filen) + ' geophone data')
    
    fileroot = filen.split('.csv')[0].split('/')[-1]
    directory = filen.split(fileroot)[0]
    root_hydrophones = 'hydrophones_'+fileroot.split('geophones_')[1]
    file_hydrophones = directory + '/' + root_hydrophones + '.csv'
    data_geophones=pd.read_csv(filen)
    data_hydrophones=pd.read_csv(file_hydrophones)
    sidex_utils.plot_specgram(data_geophones,'g',outfile='/kaggle/working/' + fileroot + 'specgram.png')
    sidex_utils.plot_timeseries(data_geophones,'g',outfile='/kaggle/working/' + fileroot + 'tseries.png')
    sidex_utils.plot_specgram(data_hydrophones,'h',outfile='/kaggle/working/' + root_hydrophones + 'specgram.png')
    sidex_utils.plot_timeseries(data_hydrophones,'h',outfile='/kaggle/working/' + root_hydrophones + 'tseries.png')
    
    plt.pause(1)
