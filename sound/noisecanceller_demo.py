# coding: utf-8
import os
from os.path import dirname, abspath
from noisecanceller import NoiseCanceller

dir_scr = dirname(abspath(__file__))
os.chdir(dir_scr)
print(dir_scr)
nc = NoiseCanceller()
nc.load("nc.wav")
nc.spectral_canceller(env_thresh=0.1, noise_level=1.0, volume_fix=True)
# output noise cancelled wav
wav_nc_path = nc.write("nc_.wav")
print(wav_nc_path)
