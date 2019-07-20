#!/usr/bin/env python
# coding: utf-8

import os
import json

# We do not want to save files anywhere
workingdir = 'C:\\Users\\zcc\\Documents\\ht_rawdata_analysis'
resultdir = os.path.join(workingdir, 'results')
if not os.path.exists(resultdir):
    os.mkdir(resultdir)


#####################################################################
# Loading good_records from json file, if this fails check build_good_records.py
with open(os.path.join(resultdir, 'good_records.json'), 'r') as f:
    infos = json.load(f)


#####################################################################
# Init output variables
# dataset: well sorted dict of subject_name: experiments as list
# pathtable: quick table contains raw data path of experiments
# repeat_session: some same task experiment may repeat during experiment
dataset = {}
pathtable = {}
repeat_session = {}

# Start parsing infos
# tmpset: less sorted version of dataset
tmpset = {}

for info in infos:
    # For each entry in infos
    # print(info)

    # Guess subject_name
    subject_name = info['name'].replace('-', '_').split('_')[0]
    subject_name = subject_name.lower()

    # If subject_name not in tmpset, init an empty list
    if subject_name not in tmpset.keys():
        tmpset[subject_name] = []

    # Guess task
    if 'aud' in info['name']:
        task = 'aud'
    if 'rest' in info['name']:
        task = 'rest'

    # Read experiment date and session number
    date = info['date']
    session = info['session']

    # Now we have experiment information for this session
    exp_info = '-'.join([task, date, session])

    # Check if the same task of experiment is repeated in one day
    for e in tmpset[subject_name]:
        if '-'.join([task, date]) in e:
            print('Repeat session:', subject_name, e, exp_info)
            sd = '%s-%s' % (subject_name, date)
            if sd not in repeat_session.keys():
                repeat_session[sd] = set()
            repeat_session[sd].add(e)
            repeat_session[sd].add(exp_info)

    # Record raw data path for each experiment session
    pathtable['-'.join([subject_name, exp_info])] = info['path']

    # Finally, append this session
    tmpset[subject_name].append(exp_info)


# Sort each subject's several experiment, ordered as task, date, session
for subject_name, exp_info in tmpset.items():
    tmpset[subject_name] = sorted(exp_info)

# Sort tmpset, ordered as subject_name
# Reload them into dataset
for e in sorted(tmpset.items(), key=lambda e: e[0]):
    dataset[e[0]] = e[1]


#####################################################################
# Save pathtable into json file for useable
with open(os.path.join(resultdir, 'experiment_path_table.json'), 'w') as f:
    json.dump(pathtable, f)

# Save pathtable into txt file for readable
with open(os.path.join(resultdir, 'quick_check_experiment_path_table.txt'), 'w') as f:
    for name, path in pathtable.items():
        f.write('%20s: %s\n' % (name, path))


#####################################################################
# Save dataset into json file for useable
with open(os.path.join(resultdir, 'dataset.json'), 'w') as f:
    json.dump(dataset, f)

# Save dataset into txt file for readable
with open(os.path.join(resultdir, 'quick_check_dataset.txt'), 'w') as f:
    for name, exp in dataset.items():
        print('%16s:' % name, ', '.join(exp), file=f)


#####################################################################
# Convert values in repeat_session into list for seriable and sort it
for e in repeat_session.items():
    repeat_session[e[0]] = sorted(list(e[1]))

# Save repeat_session into json file for useable
with open(os.path.join(resultdir, 'repeat_session.json'), 'w') as f:
    json.dump(repeat_session, f)

# Save repeat_session into txt file for readable
with open(os.path.join(resultdir, 'quick_check_repeat_session.txt'), 'w') as f:
    for name, exps in repeat_session.items():
        f.write('%25s' % name)
        f.write(': ')
        f.write(', '.join(exps))
        f.write('\n')