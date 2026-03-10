#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 13:28:40 2026

@author: camille
"""

from pathlib import Path
import pyxdf
import matplotlib.pyplot as plt
import numpy as np
# %matplotlib qt

path = '/home/camille/Documents/CurrentStudy/sub-P001/ses-S001/eeg'
# name_file = "sub-P001_ses-S001_task-Default_run-001_eeg_old16.xdf"
# name_file = "sub-P001_ses-S001_task-Default_run-001_eeg_old20.xdf"
name_file = "sub-P001_ses-S001_task-Default_run-001_eeg.xdf"

dir_path = Path(path,name_file)
streams, header = pyxdf.load_xdf(dir_path)

plt.figure()

for stream in streams:
    if stream["info"]["name"][0] == 'psychopy_markers':
        for t in stream["time_stamps"]:
            plt.axvline(x=t,linestyle = '--')
    elif stream["info"]["name"][0] == 'obci_eeg1':
        y = stream["time_series"]
        plt.plot(stream["time_stamps"], y[:,2])

