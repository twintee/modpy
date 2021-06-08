# coding: utf-8
import os
from os.path import dirname, abspath
from .soundrecorder import SoundRecoder

dir_scr = dirname(abspath(__file__))
os.chdir(dir_scr)

sr = SoundRecoder()
sr.rec()
