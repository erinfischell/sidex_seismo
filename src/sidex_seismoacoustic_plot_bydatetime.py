# ###############################################################
# sidex_seismoacoustic_plot_bydatetime
# Purpose: example code for plotting geophone and hydrophone data using a date string
# April 1, 2023
# Author:
# Erin Fischell, PhD
# Senior Scientist
# JPAnalytics
#
# This work was supported by the US Office of Naval Research
#
# questions? contact: efischell@gmail.com
#
# ###############################################################
# CONFIGURATION
# ###############################################################

# CHANGE THIS CODE FOR YOUR SETUP
datestruse='0305T2300' # datestring to match in identifying files to read. For all, use *
dataroot = '/media/efischell/T7/sidex_data/DataSet_for_realease/' # WHERE YOU PUT YOUR DATA DOWNLOAD
inputdir = dataroot + 'Raw_csvs/*/' # input directory: replace with wherever you downloaded and unzipped the data!
metadir = dataroot + 'Meta_csvs/' # metadata directory: where you put your GPS data, geophone and hydrophone meta csv files
outputdir = dataroot + 'outplots/' # output directory: replace with wherever you want to put plots!
show_plots=1 # if 1, show the plots! if 0, don't show the plots
# ###############################################################
# EXAMPLE FUNCTION CALLS/DATA INTERACTION BELOW THIS LINE
# ###############################################################
# IMPORTS
# ###############################################################
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import glob

import sidex_utils
import os
# ###############################################################
# CREATE FILE LIST
# ###############################################################
pattern = inputdir + 'geophones_' + datestruse + '*.csv'
filelist_rawcsv_geophones = sorted(glob.glob(pattern))
if len(filelist_rawcsv_geophones) ==0:
    raise Exception('ERROR: no files match pattern ' + pattern)
if not os.path.isdir(outputdir):
    os.mkdir(outputdir)
# ###############################################################
# META PLOTTING     
# ###############################################################
# plot GPS and relative locations as example:
sidex_utils.plot_rel_locations(metadir=metadir,outfile=outputdir + 'cabled_array_locations.png') # plot relative locations of sensors
sidex_utils.plot_GPS_v_time(metadir=metadir,outfile=outputdir + 'SIDEx_GPS_vtime.png') # plot GPS v time for ice drift
# ###############################################################
# DATA PLOTTING
# ###############################################################
for filen in filelist_rawcsv_geophones:    
    # identify root filename and hydrophone file:
    fileroot = filen.split('.csv')[0].split('/')[-1]
    directory = filen.split(fileroot)[0]
    root_hydrophones = 'hydrophones_'+fileroot.split('geophones_')[1]
    file_hydrophones = directory + '/' + root_hydrophones + '.csv'
    print('plotting ' +fileroot.split('geophones_')[1] + ' geophone and hydrophone data')
    
    # read in data for geophones and hydrophones:
    data_geophones=pd.read_csv(filen)
    data_hydrophones=pd.read_csv(file_hydrophones)
    plt.close('all')
    # plot geophone data:
    sidex_utils.plot_specgram(data_geophones,'g',metadir=metadir,outfile=outputdir + fileroot + 'specgram.png')
    sidex_utils.plot_timeseries(data_geophones,'g',metadir=metadir,outfile=outputdir + fileroot + 'tseries.png')
    # plot hydrophone data:
    sidex_utils.plot_specgram(data_hydrophones,'h',metadir=metadir,outfile=outputdir + root_hydrophones + 'specgram.png')
    sidex_utils.plot_timeseries(data_hydrophones,'h',metadir=metadir,outfile=outputdir + root_hydrophones + 'tseries.png')
    if show_plots:
    	plt.pause(1)
