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
# Loading dataset, experiment_path_table and repeat_session
# They are all from parse_good_records.py
# There are also quick check txt files for them
with open(os.path.join(resultdir, 'dataset.json'), 'r') as f:
    dataset = json.load(f)

with open(os.path.join(resultdir, 'experiment_path_table.json'), 'r') as f:
    experiment_path_table = json.load(f)

with open(os.path.join(resultdir, 'repeat_session.json'), 'r') as f:
    repeat_session = json.load(f)

# Get all repeated session in a set, to provide warning
all_repeat_session = set()
for sessions in repeat_session.values():
    [all_repeat_session.add(e) for e in sessions]


#####################################################################
# Specific task, start_date and stop_date for fetch
task = 'aud'
start_date = '2018-01-01'
stop_date = '2018-09-02'


# To tell if given date between start and stop
def indate(date, start=start_date, stop=stop_date):
    return all([date > start, date < stop])


#####################################################################
# Start fetching 
wanted = []
repeated_wanted = []

for name, sessions in dataset.items():
    for session in sessions:
        # Run for every single session in dataset
        if all([task in session,
                indate(session.split('-', 1)[1])]):
            # If task and date fits request
            print(name, session)
            data_path = experiment_path_table['%s-%s' % (name, session)]
            
            # If it is in repeated sessions, provide warning
            if session in all_repeat_session:
                repeated_wanted.append('%d: %s' % (len(wanted)+1, session))
                wanted.append('--'+data_path+'\n')
            else:
                wanted.append(data_path+'\n')


#####################################################################
# Report fetched data path and save them into wanted.txt file
print('Task %s, from %s to %s, there are %d data fetched.' % (
    task, start_date, stop_date, len(wanted)))

print('You should pay attention on following data, since they are repeated session for same task on same day.')
[print(e) for e in repeated_wanted]

print('Path saved in wanted.txt file.')
with open(os.path.join(resultdir, 'wanted.txt'), 'w') as f:
    f.writelines(wanted)
