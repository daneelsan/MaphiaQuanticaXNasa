def primer_algo(mseed_file1):
    st = read(mseed_file1)

    ## This is how you get the data and the time, which is in seconds
    tr = st.traces[0].copy()
    tr_times = tr.times()
    tr_data = tr.data

    ## Bandpass
    # Set the minimum frequency
    minfreq = 0.5
    maxfreq = 1.5

    # Going to create a separate trace for the filter data
    st_filt = st.copy()
    #st_filt.filter('bandpass',freqmin=minfreq,freqmax=maxfreq)
    tr_filt = st_filt.traces[0].copy()
    tr_times_filt = tr_filt.times()
    tr_data_filt = tr_filt.data

    
    mask = np.abs(tr_data_filt)>np.median(np.abs(tr_data_filt))
    tr_times_filt = tr_times_filt[mask]
    tr_data_filt = np.abs(tr_data_filt[mask])
    
    ## Create LTA algoritm
    # Sampling frequency of our trace
    df = tr.stats.sampling_rate
    
    # How long should the short-term and long-term window be, in seconds?
    sta_len = 100
    lta_len = 2000
    
    # Run Obspy's STA/LTA to obtain a characteristic function
    # This function basically calculates the ratio of amplitude between the short-term 
    # and long-term windows, moving consecutively in time across the data
    cft = classic_sta_lta(tr_data_filt, int(sta_len * df), int(lta_len * df))

    ## Haciendo el corte
    # Play around with the on and off triggers, based on values in the characteristic function
    thr_on = 2.75
    thr_off = 1.
    on_off = np.array(trigger_onset(cft, thr_on, thr_off))
    # The first column contains the indices where the trigger is turned "on". 
    # The second column contains the indices where the trigger is turned "off".

    results = []
    for i in np.arange(0,len(on_off)):
        triggers = on_off[i]
        if abs(triggers[0]-triggers[1]) >3000:
            results.append(tr_times_filt[triggers[0]])
    return results