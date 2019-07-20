#!/usr/bin/env python
# coding: utf-8

import os
import json

# We do not want to save files anywhere
workingdir = 'C:\\Users\\zcc\\Documents\\ht_rawdata_analysis'

# Make simulate dir to regular raw path into new path
simulateddir = os.path.join(workingdir, 'simulated_ds')
if not os.path.exists(simulateddir):
	os.mkdir(simulateddir)

# Where we load experiment_path_table
resultdir = os.path.join(workingdir, 'results')
if not os.path.exists(resultdir):
    os.mkdir(resultdir)


#####################################################################
# Loading experiment_path_table
# It is from parse_good_records.py
# There is also quick check txt file for it
with open(os.path.join(resultdir, 'experiment_path_table.json'), 'r') as f:
    experiment_path_table = json.load(f)


for name, path in experiment_path_table.items():
	# For each entry, try to write a new file to simulate new regular data structure
	try:
		with open(os.path.join(simulateddir, name), 'w') as f:
			f.write(path)
	except FileNotFoundError as err:
		print(err)