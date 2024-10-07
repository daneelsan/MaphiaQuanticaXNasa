import os
import numpy as np
from datetime import datetime, timedelta
from obspy import read
from scipy.integrate import simps
from obspy.signal.trigger import classic_sta_lta, trigger_onset

def arrival_time_predictor(mseed_file1):
    
    ## Reading the .mseed file
    st = read(mseed_file1)

    ## Bandpass
    # Set the minimum frequency
    minfreq = 0.5
    maxfreq = 1.5

    # Going to create a separate trace for the filter data
    st_filt = st.copy()
    st_filt.filter('bandpass',freqmin=minfreq,freqmax=maxfreq)
    tr_filt = st_filt.traces[0].copy()
    tr_times_filt = tr_filt.times()
    tr_data_filt = tr_filt.data
    
    tr_data_filt = np.abs(tr_data_filt) - np.median(np.abs(tr_data_filt))
    
    ## Create STA/LTA algoritm
    # Sampling frequency of our trace
    df = tr_filt.stats.sampling_rate
    
    #Setting the short-term and long-term windows
    sta_len = 100
    lta_len = 2700
    
    # Run Obspy's STA/LTA to obtain a characteristic function
    cft = classic_sta_lta(tr_data_filt, int(sta_len * df), int(lta_len * df))
    
    # Setting the on and off triggers, based on values in the characteristic function
    thr_on = 2.7
    thr_off = 1.5 

    # The first column contains the indices where the trigger is turned "on". 
    # The second column contains the indices where the trigger is turned "off".
    on_off = np.array(trigger_onset(cft, thr_on, thr_off))

    # Determine the duration threshold in seconds
    duration_threshold_secs = 3  # Minimum duration of 3 seconds

    # Calculate the corresponding number of data points based on the sampling rate
    duration_threshold_points = duration_threshold_secs * df

    ## Initilizating list to save the time_ons and the area below the curve between
    ## the on and off signals
    times_areas = []
    for i in np.arange(0,len(on_off)):
        triggers = on_off[i]
        # We are just keeping the triggers that have more that 3000 data points between
        # on and off, to further avoid catching a spike
        if abs(triggers[0]-triggers[1]) > duration_threshold_points:
            times_areas.append([tr_times_filt[triggers[0]],simps(tr_data_filt[triggers[0]:triggers[1]+1],tr_times_filt[triggers[0]:triggers[1]+1])])

    ## If there's a dataset without saved triggers, just return an empty list
    if len(times_areas) == 0:
        return []

    ## Setting a lower limit to the integral values
    area_test = 2.5*10**-7

    ## Only keeping the arrival times which integrals pass this threshold 
    times_areas = np.asarray(times_areas)
    survive_time_area = times_areas[times_areas[:,1] >= area_test]
    detection_times_rel = list(survive_time_area[:,0])

    detection_events = []
    starttime = st[0].stats.starttime.datetime
    for dt in detection_times_rel:
        on_time = starttime + timedelta(seconds = dt)
        on_time_str = datetime.strftime(on_time, "%Y-%m-%dT%H:%M:%S.%f")
        detection_events.append({"time_rel(sec)":dt, "time(%Y-%m-%dT%H:%M:%S.%f)": on_time_str})

    return {
        "filename": os.path.splitext(os.path.basename(mseed_file1))[0],
        "detection_events": detection_events
    }