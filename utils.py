import pandas as pd 
import numpy as np
import scipy

stimulus_raw = scipy.io.loadmat('dat_stimulus.mat')
spk_sample_raw = scipy.io.loadmat('dat_spk_sample.mat')
spk_test_raw = scipy.io.loadmat('dat_spk_test.mat')

stimulus = stimulus_raw['stimulus']
spk_sample = spk_sample_raw['spk_sample']
spk_test = spk_test_raw['spk_test']

#create sample file to pandas dataframe format
def get_sample_freq(sample_num, start_gap=0.1, window_size = 2, mode = 'Frequency'):
    assert mode in ['Frequency', 'Counts']
    df_deg_freq = pd.DataFrame(columns=['Time','Degree',mode])
    sample = spk_sample[sample_num-1,0]

    i = 0
    for time, degree in stimulus:
        if (time >= 50) & (time <= 350):
            frequency = len(sample[(sample > (time+start_gap)) & (sample <= (time + start_gap + window_size))]) #/ window_size
            if mode == 'Frequency':
                frequency /= window_size
            df_deg_freq.loc[i,:] = [time, int(degree), frequency]
            i += 1
    return df_deg_freq

#create sample file to pandas dataframe format 
def get_test_freq(num, start_gap=0.1, window_size = 2, mode = 'Frequency'):
    assert mode in ['Frequency', 'Counts']
    df_deg_freq = pd.DataFrame(columns=['Time','Degree',mode])
    sample = spk_test[num-1,0]

    i = 0
    for time, degree in stimulus:
        if (time >= 400) & (time <= 700):
            frequency = len(sample[(sample > (time+start_gap)) & (sample <= (time + start_gap + window_size))])
            if mode == 'Frequency':
                frequency /= window_size #/ window_size
            df_deg_freq.loc[i,:] = [time, int(degree), frequency]
            i += 1
    return df_deg_freq

def get_stimulus():
    degree_dict = dict()
    for degree in np.unique(stimulus[:,1]):
        stim_time_list = stimulus[stimulus[:,1] == degree,0]
        degree_dict[degree] = stim_time_list
    return degree_dict

def remove_outliers(arr, threshold=3):
    """
    Remove outliers from a 1-dimensional NumPy array using Z-score.

    Parameters:
    - arr: 1-dimensional NumPy array
    - threshold: Z-score threshold for identifying outliers (default is 3)

    Returns:
    - Array with outliers removed
    """
    if np.std(arr) < 1e-6:
        return arr
    else:
        z_scores = np.abs((arr - np.mean(arr)) / np.std(arr))
        filtered_arr = arr[z_scores < threshold]
        return filtered_arr