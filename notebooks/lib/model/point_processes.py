import numpy as np

def comp_data(nid_self,dict_spike_times,number_of_neurons,t_stim_start,
    t_stim_end,printing=False,t_arrival_physical=.15,t_stop=3.):
    #compute the point process matrix for a single trial
    if printing:
        print (f"the stimulus duration was {t_stim_end-t_stim_start:.2f} seconds.")

    #extract spiketimes as a list of numpy arrays
    t_values_lst=[]
    for nid in range(number_of_neurons):
        t_values=np.array(dict_spike_times[nid])
        t_values_lst.append(t_values)

    if printing:
        print(f'the reference neuron is #{nid_self} as the most spiking neuron.')
    t_self_values=t_values_lst[nid_self]

    t_start=t_stim_start+t_arrival_physical
    t_end=t_stim_start+t_stop
    zeros=np.zeros(number_of_neurons)
    #extract times of self spiking
    boo=(t_self_values>=t_start)&(t_self_values<t_end)
    ts=t_self_values[boo]
    #extract times of their spiking for each neuron
    X_values_lst=[]
    for t in ts:
        tt_values=zeros.copy()
        for j,t_values in enumerate(t_values_lst):
            #given each neighbor at least the most recent spike that is strictly before t
            boo=t_values<t
            tt_values[j]=t_values[boo][-1]
        X_values=t-tt_values
        X_values_lst.append(X_values)
    data=np.stack(X_values_lst)
    t_values=ts-t_stim_start
    return t_values, data

def comp_target(t_values,t_arrival,t_departure):
    '''classify spikes as before or during the arrival time of the information of the stimulus
    Example Usage:
    target=comp_target(t_values)
    target_names=[r'dubious',r'decisive',r'reflective']
    '''
    boo_before=t_values<t_arrival
    boo_after=~boo_before
    boo_after&=t_values<t_departure
    boo_ignore=t_values>=t_departure
    target=boo_before*0+boo_after*1+boo_ignore*2
    return target

def compute_point_process_data(t_min_considered, number_of_neurons,
    dict_spike_times, dict_trial_times, dict_trial_data,
    printing=False,nid_self=None,
    t_arrival=1.5,t_departure=2.5,
    t_arrival_physical=.15,t_stop=3.,
    **kwargs):
    '''t_min_considered is for the entire set, not for the individual trial.
    Example Usage:
    target,data,trialnum_values,t_values=compute_point_process_data(
        t_min_considered,
        number_of_neurons,
        dict_spike_times,
        dict_trial_times,
        dict_trial_data,
        printing=True,nid_self=None,
        t_arrival=1.5,t_departure=2.5,
        t_arrival_physical=.15,t_stop=3.,
        **kwargs)
    '''
    if nid_self is None:
        #identify the neuron with the most spikes as nid_self
        nid_self=0
        max_obs=0
        for nid in range(number_of_neurons):
            obs=dict_spike_times[nid].shape[0]
            if obs>max_obs:
                max_obs=obs
                nid_self=nid

    #iterate over trials and compute the point process matrix for each trial
    target_names=[r'dubious',r'decisive',r'reflective'] #see lib/model/point_processes.py
    trialnum_lst    =dict_trial_times['trialnum']
    t_stim_start_lst=dict_trial_times['t_stim_start']
    t_stim_end_lst  =dict_trial_times['t_stim_end']

    trialnum_out_lst=[]
    target_out_lst=[]
    data_out_lst=[]
    t_values_lst=[]
    for trialnum,t_stim_start,t_stim_end in zip(trialnum_lst,t_stim_start_lst,t_stim_end_lst):
        if (t_stim_start>=t_min_considered):
            try:
                t_values,data=comp_data(nid_self,dict_spike_times,number_of_neurons,t_stim_start,t_stim_end,
                t_arrival_physical=t_arrival_physical,t_stop=t_stop)
                target=comp_target(t_values,t_arrival=t_arrival,t_departure=t_departure)
                trialnum_out_lst.append(trialnum+0*target)
                target_out_lst.append(target)
                data_out_lst.append(data)
                t_values_lst.append(t_values)
            except Exception as e:
                pass
                # print(e)

            # # try:
            # t_values,data=comp_data(dict_spike_times,number_of_neurons,t_stim_start,t_stim_end)
            # target=comp_target(t_values)
            # trialnum_out_lst.append(trialnum)
            # target_out_lst.append(target)
            # data_out_lst.append(data)
            # # except Exception as e:
            # #     print(e)

    #concatenate data_out_lst
    data=np.concatenate(data_out_lst)
    target=np.concatenate(target_out_lst)
    trialnum_values=np.concatenate(trialnum_out_lst)
    t_values=np.concatenate(t_values_lst)
    if printing:
        num_obs=data.shape[0]
        num_neurons=data.shape[1]
        print(f"{len(trialnum_out_lst)} trials successfully parsed into {num_obs} observations.")
        #assert the data is well defined and positive everywhere
        assert (not np.isnan(data).any())
        assert ((data>0).any())
        print(f"this point-process measure is embedded into $\mathbb{{R}}^{{+d}}$ real Euclidean space of dimension d={num_neurons}.")
    return nid_self,target,data,trialnum_values,t_values
