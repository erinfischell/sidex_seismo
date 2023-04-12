# ###############################################################
# sidex_utils
# Purpose: example code and utilities for sidex seismoacoustic code
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
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import scipy.io.wavfile as wv
from scipy import signal
import scipy
import glob

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from datetime import datetime

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os


def timefromfilename(filename):
    # get timestamp from filename
     # parse filename to get basic information:
    #/home/efischell/AcBoticsResearch/data/sidex/N1/2021-03-16_16:40:29_D40s_N1_T1.csv
    fname =filename.split('/')[-1]
    tstamp=fname.split('p')[0]
    time_arrival = datetime.strptime(tstamp, 'Sidex_%Y%m%dT%H%M%S').replace(tzinfo=timezone.utc) #+ timedelta(hours=time[itt])
    return time_arrival

def write_wav_file(data_vector,outfilename,FS=1000,speedup=1,verbose=0):
    # write a .wav file of data vector
    # to outfilename
    # FS: samplerate (default 1000)
    # speedup: x speedup for writing wav file
    # ch_idx_list: list of channel idx to create wave files in
    
   
    cur_data_amp = (data_vector-np.mean(data_vector))/np.max(data_vector-np.mean(data_vector))
    wv.write(outfilename,FS*speedup,cur_data_amp)
    if verbose:
        print('Created .wav file: ' + str(fnameout))
            
        
def bandpass_filter(datamat,f_lowpass,f_highpass,FS):
    Wn_LP = f_lowpass/(FS/2) # normalized frequency for filter- desired cutoff/nyquist, nyquist=Fs/2
    Wn_HP = f_highpass/(FS/2)
    b, a = signal.butter(6, Wn_LP, 'low')
    d, c = signal.butter(6, Wn_HP,'high')
    data_filt = signal.filtfilt(b,a,datamat[:,:],axis=0)
    return data_filt

    
def geophone_filter_df(datamat,f_lowpass=300,f_highpass = 2,FS=1000):
    # filter pandas datamat of N x M, where N is the number of rows and
    # M is the number of channels
    # default settings for geophone: lowpass 100 Hz, highpass 1 Hz, FS=1000
    # outputs new pandas dataframe
    data_convert = datamat.to_numpy()[:,2:]
    data_convert = data_convert - np.mean(data_convert)
    data_filt=bandpass_filter(data_convert,f_lowpass,f_highpass,FS)
    pd_filt = datamat.copy()
    pd_filt.iloc[:,2:]=data_filt
    return pd_filt

def hydrophone_filter_df(datamat,f_lowpass=499,f_highpass = 2,FS=1000):
    # filter pandas datamat of N x M, where N is the number of rows and
    # M is the number of channels
    # default settings for hydrophone: lowpass 499 Hz, highpass 5 Hz, FS=1000
    data_convert = datamat.to_numpy()[:,2:]
    data_filt=bandpass_filter(data_convert,f_lowpass,f_highpass,FS)
    pd_filt = datamat.copy()
    pd_filt.iloc[:,2:]=data_filt
    return pd_filt

def get_moving_avg(df,time_movingavg):
    # df = pandas dataframe, loaded from file
    FS=1000 # sample rate (samples/s)
    return df.rolling(int(time_movingavg*FS)).mean()

def plot_specgram(data,data_type,metadir,outfile = None):
    

    if data_type=='h':
            
        # filter:
        metafile=  metadir + 'SIDEx_hydrophones_surveyed.csv'

        data_filt = hydrophone_filter_df(data)
        num_rows=5
        num_cols=3
        vmin=-100
        vmax=-30
    elif data_type=='g':
        metafile= metadir + '/SIDEx_geophones_surveyed.csv'#hydrophone_metadata
        data_filt = geophone_filter_df(data)
        num_rows= 4
        num_cols=3
        vmin=-150
        vmax=-80
    # plot!
    print('Plotting spectrogram!')
    metadata = pd.read_csv(metafile)
    fig,ax = plt.subplots(nrows=num_rows,ncols=num_cols,sharex=True,sharey=True)
    
    timev = [datetime.utcfromtimestamp(tt) for tt in data_filt['Epoch']]#(data_filt['Epoch'].to_numpy() - time_start_epoch)/tdivide
    
    for row in range(0,num_rows):
        for col in range(0,num_cols):
            cur_ch_idx = row*3+col
            label_ch = metadata['ch_type'][cur_ch_idx]
            
            if cur_ch_idx < len(data_filt.columns):
                cur_ch_no = data_filt.columns[2+cur_ch_idx]
                cur_data = data_filt.iloc[:,2+cur_ch_idx].to_numpy()
                
                ax[row,col].specgram(cur_data,Fs=1000,NFFT=500,noverlap=490,vmin=vmin,vmax=vmax)
                
                ax[row,col].set_title(label_ch + ', CH: ' + cur_ch_no)
                
                if row == num_rows-1:
                    ax[row,col].set_xlabel('S since ' + timev[0].strftime('%m%dT%H%M%S'))
                    #if 
                    ax[row,col].set_ylim([0,100])
                    
                if col==0:
                    
                    ax[row,col].set_ylabel('Freq, N' + str(row))
                
   
    plt.tight_layout()
    # save file, and show if desired:
    if outfile is not None:
        plt.savefig(outfile)

def plot_geophone_particlemotion(data_select,outfile=None):
    if len(data_select['0'].to_numpy())>10*1000:
        print('WARNING: particle motion not likely to look meaningful wtih more than 10 s of data!')
    data_select_g_strike = geophone_filter_df(data_select,f_lowpass=50,f_highpass = 2)
    
    plt.figure()
    plt.subplot(221)
    plt.plot(data_select_g_strike['0'],(data_select_g_strike['1']**2+data_select_g_strike['2']**2)**.5*np.sign(data_select_g_strike['2']/data_select_g_strike['1']))
    print(P_id)
    plt.title('N0')
    plt.axis('equal')
    plt.subplot(222)
    plt.plot(data_select_g_strike['3'],(data_select_g_strike['4']**2+data_select_g_strike['5']**2)**.5*np.sign(data_select_g_strike['5']/data_select_g_strike['4']))
    
    plt.title('N1')
    plt.axis('equal')
    plt.subplot(223)
    plt.plot(data_select_g_strike['6'],(data_select_g_strike['7']**2+data_select_g_strike['8']**2)**.5*np.sign(data_select_g_strike['7']*data_select_g_strike['8']))
    
    plt.title('N2')
    plt.axis('equal')
    plt.subplot(224)
    plt.plot(data_select_g_strike['9'],(data_select_g_strike['10']**2+data_select_g_strike['11']**2)**.5*np.sign(data_select_g_strike['10']*data_select_g_strike['11']))
    
    plt.title('N3')
    plt.axis('equal')
    plt.tight_layout()
    if outfile is not None:
        plt.savefig(outfile)
    
def plot_timeseries(data,data_type,metadir,ax=None,outfile = None):
    # data: pandas dataframe containing data
    # data_type = h or g
    # ax: if you want the plot as an axis in existing plot
    # outfile: if you want to save the plot
    print('Plotting time series!')
    
    if data_type=='h':
        metafile = metadir + 'SIDEx_hydrophones_surveyed.csv'
        # filter:
        data_filt = hydrophone_filter_df(data)
    elif data_type=='g':
        metafile = metadir + 'SIDEx_geophones_surveyed.csv'
        data_filt = geophone_filter_df(data)

    #print(data_filt.columns)
    # load meta data for the array:
    metadata = pd.read_csv(metafile)
    
    # plot!
    #print(data_filt['Epoch'])
    time_start_epoch = data_filt['Epoch'].iloc[0]
    time_start_datetime = data_filt['UTCstr'].iloc[0]
   
    timev = [datetime.utcfromtimestamp(tt) for tt in data_filt['Epoch']]#(data_filt['Epoch'].to_numpy() - time_start_epoch)/tdivide
    if ax is None:
        
        fig,ax=plt.subplots(1,1,figsize=(10, 5))
    
    for cur_ch_idx in range(0,len(metadata['ch_type'])):
            
        label_ch = metadata['ch_type'][cur_ch_idx]
        peak_allchannels = np.max(np.max(np.abs(data_filt.iloc[:,2:])))
       # print(label_ch)
        if label_ch == 'g_y':
            cc = 'r-'
            
        elif label_ch == 'g_z':
            cc = 'g-'
        elif label_ch =='g_x':
            cc = 'b-'
        elif label_ch =='hydrophone':
            if metadata['z_pos'][cur_ch_idx]<-5:
                cc = 'k-'
            else:
                cc = 'm-'
        if cur_ch_idx < len(data_filt.columns):
            cur_ch_no = data_filt.columns[2+cur_ch_idx]
            cur_data = data_filt.iloc[:,2+cur_ch_idx].to_numpy()
            #print(cur_ch_no)
            cur_data=cur_data-np.mean(cur_data)
            cur_data_norm = cur_data/(peak_allchannels/2)
            
            ax.plot(timev,cur_data_norm + int(cur_ch_no),cc)
    if data_type=='g':
        ax.set_title(data_type + ' data, L=red, T=blue, V=green')
    else:
        ax.set_title(data_type + ' data, deep=black, shallow=pink')
    ax.set_xlabel('Time')
    ax.set_ylabel('Channel Number')
    
    
    plt.tight_layout()
    # save file, and show if desired:
    if outfile is not None:
        plt.savefig(outfile)
def plot_rel_locations(metadir,ax=None,outfile=None):
    print('plotting array')
    if ax is None:
        fig,ax=plt.subplots(1,1)
    loc_data_h=pd.read_csv(metadir + 'SIDEx_hydrophones_surveyed.csv')
    loc_data_g=pd.read_csv(metadir + 'SIDEx_geophones_surveyed.csv')
    ax.plot(loc_data_h['Easting'],loc_data_h['Northing'],'o')
    ax.plot(loc_data_g['Easting'],loc_data_g['Northing'],'kx')
    
    ax.legend(['Hydrophones','Geophones'])
    ax.set_ylabel('Northing (m)')
    ax.set_xlabel('Easting (m)')
    ax.axis('equal')
    plt.tight_layout()
    if outfile is not None:
        plt.savefig(outfile)
    
    
def plot_GPS_v_time(metadir,ax=None,outfile=None):
    if ax is None:
        fig,ax=plt.subplots(1,1)
    # plot the GPS drift v. time for the entire time series
    print('plotting gps drift')
    GPS_files = sorted(glob.glob(metadir + '*/GPS*.csv'))
    # create scatter plot of GPS location v. time:
    ii=0

    for csvfile in GPS_files[1:]:
        # load the csv of GPS data:
        df_cur = pd.read_csv(csvfile)
        if ii==0:
            time_start = df_cur['time_epoch'][0]
            df_gps = df_cur
        else:
            df_gps=df_gps.append(df_cur)

        ii=ii+1
        # plot the data:

    plt.scatter(df_gps['lon'][df_gps['lon']!=0],df_gps['lat'][df_gps['lon']!=0],c=(df_gps['time_epoch'][df_gps['lon']!=0]-time_start)/(60*60*24))
    plt.title(datetime.utcfromtimestamp(time_start).strftime('%y%m%dT%H%M%S')+' to ' + datetime.utcfromtimestamp(df_gps['time_epoch'].to_numpy()[-1]).strftime('%y%m%dT%H%M%S'))
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.colorbar()
    plt.tight_layout()
    if outfile is not None:
        plt.savefig(outfile)

        
