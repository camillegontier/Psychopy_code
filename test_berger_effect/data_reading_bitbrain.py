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
from scipy.signal import butter, filtfilt, hilbert, spectrogram
# %matplotlib qt

path = '/home/camille/Code/Psychopy_code/test_berger_effect/data/long_berger_effect'
name_file = "sub-P001_ses-S001_task-Default_run-001_eeg.xdf"

dir_path = Path(path,name_file)
streams, header = pyxdf.load_xdf(dir_path)

def bandpass(data, lowcut, highcut, fs, order=4):
    nyquist = fs / 2
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

fs = 256
list_channels = ["AF7", "FP1", "FP2", "AF8", "P7", "O1", " O2", "P8"]

# Spectrogram for alpha identifiation #########################################

fmin = 9
fmax = 11

for stream in streams:
      if stream["info"]["name"][0] == 'eeg8ch_eeg':
          y = stream["time_series"]
          fig, axs = plt.subplots(2, 4, sharey=True, sharex=True)
          
          for ch,ax in enumerate(axs.reshape(-1)): 
            signal = y[:,ch]
            f, t, Sxx = spectrogram(signal, fs)
            frequencies_of_interest = np.where((f<20) & (f>5))[0]
            ax.pcolormesh(t, f[frequencies_of_interest], Sxx[frequencies_of_interest,:], shading='gouraud')
            ax.axhline(y=fmin,linestyle='--',linewidth=3,c='tab:red')
            ax.axhline(y=fmax,linestyle='--',linewidth=3,c='tab:red')
            ax.set_title(f"CH{ch}-{list_channels[ch]}")
          fig.supxlabel('Time [sec]')
          fig.supylabel('Frequency [Hz]')

# Plot of alpha band power ####################################################

for stream in streams:
      if stream["info"]["name"][0] == 'psychopy_markers':
        t_markers = stream["time_stamps"]
      elif stream["info"]["name"][0] == 'eeg8ch_eeg':
          print(stream["info"])
          y = stream["time_series"]
          for ch in range(8):            
            signal = y[:,ch]
            plt.figure(figsize = (20,4))
            alpha = bandpass(signal, fmin, fmax, fs)
            alpha_power = np.abs(hilbert(alpha))**2
            plt.plot(stream["time_stamps"]-stream["time_stamps"][0], alpha_power)
            plt.title(f"CH{ch}-{list_channels[ch]}-Alpha power")
            plt.ylabel("uV^2")
            plt.xlabel("Time (s)")
            for i,t in enumerate(t_markers):
              plt.axvline(x=t-stream["time_stamps"][0],linestyle = "--", color = "black")
              if i%2==0:
                  plt.fill_between([t_markers[i]-stream["time_stamps"][0],t_markers[i+1]-stream["time_stamps"][0]], max(alpha_power),  facecolor='grey', alpha=.5)
            plt.show()
            
# Sanity check ################################################################
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.signal import hilbert, chirp
# duration, fs = 1, 400  # 1 s signal with sampling frequency of 400 Hz
# t = np.arange(int(fs*duration)) / fs  # timestamps of samples
# signal = chirp(t, 20.0, t[-1], 100.0)
# signal *= (1.0 + 0.5 * np.sin(2.0*np.pi*3.0*t) )
# analytic_signal = hilbert(signal)
# amplitude_envelope = np.abs(analytic_signal)
# # filtered_signal = signal
# filtered_signal = bandpass(signal, 50, 60, fs)
# instantaneous_phase = np.unwrap(np.angle(analytic_signal))
# instantaneous_frequency = np.diff(instantaneous_phase) / (2.0*np.pi) * fs
# fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, sharex='all', tight_layout=True)
# ax0.set_title("Amplitude-modulated Chirp Signal")
# ax0.set_ylabel("Amplitude")
# ax0.plot(t, signal, label='Signal')
# ax0.plot(t, amplitude_envelope, label='Envelope')
# ax0.legend()
# ax1.set(xlabel="Time in seconds", ylabel="Frequency in Hz", ylim=(0, 120))
# ax1.plot(t[1:], instantaneous_frequency, 'C2-',
#          label='Instantaneous Frequency')
# ax1.legend()
# ax2.plot(t,np.abs(hilbert(filtered_signal))**2)
# plt.show()

