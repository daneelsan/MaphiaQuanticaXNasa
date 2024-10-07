import numpy as np
from obspy import read
from scipy.integrate import simps
from obspy.signal.trigger import classic_sta_lta, trigger_onset

def arrival_time_predictor(mseed_file1):
    
    ## Reading the .mseed file
    st = read(mseed_file1)

    ## Getting the data and the time
    tr = st.traces[0].copy()
    tr_times = tr.times()
    tr_data = tr.data

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

    ## Initilizating list to save the time_ons and the area below the curve between
    ## the on and off signals
    times_areas = []
    for i in np.arange(0,len(on_off)):
        triggers = on_off[i]
        # We are just keeping the triggers that have more that 3000 data points between
        # on and off, to further avoid catching a spike
        if abs(triggers[0]-triggers[1]) > 3000:      
            times_areas.append([tr_times_filt[triggers[0]],simps(tr_data_filt[triggers[0]:triggers[1]+1],tr_times_filt[triggers[0]:triggers[1]+1])])

    ## If there's a dataset without saved triggers, just return an empty list
    if len(times_areas) == 0:
        return []

    ## Setting a lower limit to the integral values
    area_test = 2.5*10**-7

    ## Only keeping the arrival times which integrals pass this threshold 
    times_areas = np.asarray(times_areas)
    survive_time_area = times_areas[times_areas[:,1] >= area_test]
    
    return list(survive_time_area[:,0])