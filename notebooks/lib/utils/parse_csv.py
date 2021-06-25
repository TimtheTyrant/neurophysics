#parse csv files as described in doc/schema.docx
#programmer: Tim Tyree
#date: 6.6.2021
import numpy as np, os

##################
# Main Utils
##################
def parse_spikeTimes(input_fn,scale=1/30000, warnings=True, **kwargs):
    '''
    import data and return it as a dictionary of spike times.
    Example Usage:
    number_of_neurons, dict_spike_times=parse_spikeTimes(input_fn)
    first_neuron_spike_times=dict_spike_times[0]
    '''
    dict_spike_times=dict()
    with open(input_fn) as f:
        nid=0
        for line in f:
            spikes=[]
            for val in line.split(','):
                try:
                    val=eval(val)
                    spikes.append(val)
                # except NameError as ee:
                except SyntaxError as e:
                    pass
            dict_spike_times[nid]=np.array(spikes[1:])*scale
            nid+=1
    number_of_neurons=nid
    return number_of_neurons, dict_spike_times

def filter_spikeTimes(number_of_neurons, dict_spike_times, percentile=.95,printing=False, **kwargs):
    '''
    import data and return it as a dictionary of spike times.
    Example Usage:
    t_min_considered, number_of_neurons, dict_spike_times=filter_spikeTimes(number_of_neurons, dict_spike_times)
    first_neuron_spike_times=dict_spike_times[0]
    '''
    #make map from neuron to t_min,t_max
    t_min_lst=[];t_max_lst=[];nid_lst=[]
    for nid in range(number_of_neurons):
        st=dict_spike_times[nid]
        if len(st)>0:
            t_min_lst.append(np.min(st))
            t_max_lst.append(np.max(st))
            nid_lst.append(nid)

    #pick a reasonable set of neurons to not consider
    # np.min(t_min_lst),np.median(t_min_lst),np.max(t_min_lst)
    t_min_considered=np.quantile(t_min_lst,percentile)
    # t_max_considered=np.quantile(t_max_lst,.05)
    if printing:
        print(f"{100*(1-t_min_considered/np.max(t_max_lst)):.1f}% of the raw timeline is preserved in this well-defined point-process")

    #determine which neurons to drop
    # keep_nid_lst=[]
    # keep_spiketimes_lst=[]
    didnt_spike_yet_nid_lst=[]
    nid_out=0
    dict_spike_times_out=dict()
    for nid in range(number_of_neurons):
        st=dict_spike_times[nid]
        if (len(st)>0):
            if (np.min(st)<=t_min_considered):
                # keep_nid_lst.append(nid_out)
                # keep_spiketimes_lst.append(dict_spike_times[nid])
                dict_spike_times_out[nid_out]=st
                nid_out+=1
            else:
                didnt_spike_yet_nid_lst.append(nid)
    num_neurons_out=nid_out
    if printing:
        print(f"this will result in a {num_neurons_out}-dimensional point process.")
    return t_min_considered, num_neurons_out, dict_spike_times_out

def load_spikeTimes(input_fn,percentile=.95,**kwargs):
    number_of_neurons, dict_spike_times=parse_spikeTimes(input_fn,**kwargs)
    return filter_spikeTimes(number_of_neurons, dict_spike_times, percentile=percentile,**kwargs)

def parse_trialTimes(input_fn, warnings=True, **kwargs):
    '''
    import data and return it as a dictionary of stimulus timings.
    Example Usage:
    dict_trialTimes=parse_trialTimes(input_fn)
    '''
    trialnum_lst=[]
    t_stim_start_lst=[]
    t_stim_end_lst=[]
    with open(input_fn) as f:
        lineno=0
        for line in f:
            t_stim_start,t_stim_end=eval(line)
            trialnum_lst.append(lineno)
            t_stim_start_lst.append(t_stim_start)
            t_stim_end_lst.append(t_stim_end)
            lineno+=1
    dict_trialTimes={
        "trialnum":trialnum_lst,
        "t_stim_start":t_stim_start_lst,
        "t_stim_end":t_stim_end_lst
    }
    return dict_trialTimes

def parse_trialData(input_fn, **kwargs):
    '''
    import data and return it as a dictionary of trial data/features/labels.
    Example Usage:
    dict_trial_data=parse_trialData(input_fn)
    '''
    trialnum_lst=[]
    t_stim_start_lst=[]
    trial_kwargs_lst=[]
    with open(input_fn) as f:
        lineno=-1
        for line in f:
            if lineno>0:
                trialnum_lst.append(lineno)
                trial_properties=line.split(',')
                trial_kwargs={
                    "imName":trial_properties[0],
                    "imNum":eval(trial_properties[1]),
                    "imPheeName":trial_properties[2],
                    "imMatchFlag":eval(trial_properties[3]),
                    "novel":eval(trial_properties[4]),
                    "imOff":trial_properties[5],
                    "vpltTrial":eval(trial_properties[6]),
                    "Block":eval(trial_properties[7]),
                    "PheeID":trial_properties[8],
                    "PicID_1":trial_properties[9],
                    "PicID_2":trial_properties[10],
                    "PidID_3":trial_properties[11].split('\n')[0]
                }
                trial_kwargs_lst.append(trial_kwargs)
            lineno+=1
    dict_trial_data=dict(zip(trialnum_lst,trial_kwargs_lst))
    return dict_trial_data


def load_dataset(modname,data_folder,warnings,printing,**kwargs):
    '''loads a set of trials
    Example Usage:
    data_dir=f"{nb_dir}/Data"
    modname="Archie_SRT_Set212_Subset1_200520_165716_"
    t_min_considered, number_of_neurons, dict_spike_times, dict_trialTimes, dict_trial_data=load_set(modname,data_folder)
    '''
    os.chdir(data_folder)
    trgt1='trialTimes.csv'
    trgt2='trialData.csv'
    trgt3='ChannelNums.csv'
    trgt4='SpikeTimes.csv'
    #todo(later): implement parsing of ChannelNums.csv
    #parse SpikeTimes.csv
    input_fn=modname+trgt4
    try:
        t_min_considered, number_of_neurons, dict_spike_times=load_spikeTimes(input_fn,**kwargs)
    except FileNotFoundError as e:
        t_min_considered, number_of_neurons, dict_spike_times = None, None, None
        if warnings:
            print(f"Warning: File not found: {input_fn}\n\t returning None...")

    #parse trialTimes.csv
    input_fn=modname+trgt1
    try:
        dict_trialTimes=parse_trialTimes(input_fn,**kwargs)
    except FileNotFoundError as e:
        dict_trialTimes = None
        if warnings:
            print(f"Warning: File not found: {input_fn}\n\t returning None...")

    #parse trialData.csv
    input_fn=modname+trgt2
    try:
        dict_trial_data=parse_trialData(input_fn,**kwargs)
    except FileNotFoundError as e:
        dict_trial_data = None
        if warnings:
            print(f"Warning: File not found: {input_fn}\n\t returning None...")

    return t_min_considered, number_of_neurons, dict_spike_times, dict_trialTimes, dict_trial_data

##################
# Misc. Utils
##################
def parse_for_modname(file):
    '''parse a modname from file name'''
    file_name=os.path.basename(file)
    modname='_'.join(file_name.split('_')[:-1])+'_'
    return modname

def return_output_modname(modname,trialnum,trial_kwargs,make_output_self_documenting=True):
    output_modname=modname+f"trial_{trialnum}"
    if make_output_self_documenting:
        # make trial output_modname self documenting
        for key in trial_kwargs.keys():
            if (key != 'imName')&(key != 'imOff'):
                value=trial_kwargs[key]
                if value != 'none':
                    #append to output_modname
                    output_modname=output_modname+f'_{key}_{value}'
    return output_modname

def determine_whether_all_files_were_found(t_min_considered, number_of_neurons, dict_spike_times, dict_trial_times, dict_trial_data):
    boo_all_files_found  = t_min_considered is not None
    boo_all_files_found &=number_of_neurons is not None
    boo_all_files_found &= dict_spike_times is not None
    boo_all_files_found &= dict_trial_times is not None
    boo_all_files_found &=  dict_trial_data is not None
    return boo_all_files_found

def parse_set_number(modname):
    base_str=os.path.basename(modname).lower()
    trgt='_set'
    setnum=eval(base_str[base_str.find(trgt)+len(trgt):].split('_')[0])
    return setnum
