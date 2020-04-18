#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 01:19:21 2020

@author: yossef
"""
import librosa
import IPython as ip
import soundfile as sf
from pydub import AudioSegment
audio_data1 = 'songs/Sia_Alive_05.mp3'
audio_data2 = 'songs/Sam Smith_Too_Good_At_Goodbyes_vocals_05.mp3'
x1 , sr1 = librosa.load(audio_data1, duration=60.0)
x2 , sr2 = librosa.load(audio_data2, duration=60.0)
x1=x1*0.5
x2=x2*0.5
x=x1+x2
sf.write('mixed.wav',x ,sr1)
sound = AudioSegment.from_wav('mixed.wav')

sound.export('mixed.mp3', format="mp3")


 
