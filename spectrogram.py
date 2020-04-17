#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 21:13:45 2020

@author: yossef
"""
import librosa
import matplotlib.pyplot as plt
import librosa.display
audio_data = 'Sia_Alive_05.mp3'
x , sr = librosa.load(audio_data, duration=60.0)
X = librosa.stft(x)
Xdb = librosa.amplitude_to_db(abs(X))
plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
plt.colorbar()
