import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from pydub import AudioSegment
from tempfile import mktemp
import numpy as np
import librosa
import imagehash
from PIL import Image
import librosa.display
import glob
import gc
import functools
import soundfile as sf
from operator import itemgetter

class audioSpectogram():

    def __init__(self,path:str,id:int = 0,hashingMode:str="perception"):
        self.path = path
        self.id = id
        self.hashMode = hashingMode
        self.samples = None
        self.sample_rate = None
        self.lenght = None
        self.hash = None
        self.spectrogram = None
        self.frequencies = None
        self.times = None
        self.spectHash = None
        self.mffcHash = None
        self.tonnetzHash = None
        self.chromaHash = None

        print("objct {} created :)".format(self.id))
        self.readAudio()    
        self.setData()

    def __del__(self):
        self.path = None
        self.samples = None
        self.sample_rate = None
        self.lenght = None
        self.hash = None
        self.spectrogram = None
        self.frequencies = None
        self.times = None
        self.spectHash = None
        self.mffcHash = None
        self.tonnetzHash = None
        self.chromaHash = None
        # gc.collect()
        print("objct {} deleted :X".format(self.id))

    def readAudio(self):
                
        self.samples , self.sample_rate = librosa.load(self.path, duration=60.0,mono = True) # Read mp3
                

    def setData(self):
        spect = self.spectro()
        ft1,ft2,ft3 = self.features()
        self.spectHash = self.hashFile(spect,self.hashMode)
        self.mffcHash  = self.hashFile(ft1,self.hashMode)
        self.tonnetzHash = self.hashFile(ft2,self.hashMode)
        self.chromaHash = self.hashFile(ft3,self.hashMode)
        
    def getData(self):
        return (self.spectHash,self.mffcHash,self.tonnetzHash,self.chromaHash,self.times,self.frequencies,self.spectrogram)    

    def spectro(self):
        
        X = librosa.stft(self.samples)
        Xdb = librosa.amplitude_to_db(abs(X))
        librosa.display.specshow(Xdb, sr=self.sample_rate)
        plt.tight_layout(pad = 0)
        spectFig = mktemp('.png')  # use temporary file
        plt.savefig(spectFig,bbox_inches='tight', transparent=True, pad_inches=0)
        return spectFig
    
    
    def hashFile(self,figure:str,mode:str = "perception"): # Hashing function , returns a string
        if mode == "average":
            hash = imagehash.average_hash(Image.open(figure))
        elif mode == "perception":    
            hash = imagehash.phash(Image.open(figure))
        elif mode == "difference":
            hash = imagehash.dhash(Image.open(figure))
        elif mode == "wavelet":
            hash = imagehash.whash(Image.open(figure))    
        # print(hash)
        return hash

    def features(self):
        # mffcs (Featrue 1)
        mfccs = librosa.feature.mfcc(y=self.samples, sr=self.sample_rate)
        librosa.display.specshow(mfccs)
        plt.tight_layout(pad = 0)
        # mffcFig = 'mffc.png'
        mffcFig = mktemp('.png') # tempfile
        plt.savefig(mffcFig,bbox_inches='tight', transparent=True, pad_inches=0)

        #  tonal centroid (feature 2)
        tonnetz = librosa.feature.tonnetz(y=self.samples, sr=self.sample_rate)
        librosa.display.specshow(tonnetz)
        plt.tight_layout(pad = 0)
        # tonnetzFig = 'tonnetz.png'
        tonnetzFig = mktemp('.png') # tempfile
        plt.savefig(tonnetzFig,bbox_inches='tight', transparent=True, pad_inches=0)
        
        # chroma (feature 3 )
        chroma = librosa.feature.chroma_cqt(self.samples, sr=self.sample_rate)
        librosa.display.specshow(chroma)
        plt.tight_layout()
        # chromaFig = 'chroma.png'
        chromaFig = mktemp('.png') # tempfile
        plt.savefig(chromaFig,bbox_inches='tight', transparent=True, pad_inches=0)
        return (mffcFig,tonnetzFig,chromaFig)


def loopFolder(path:str,extension:str):
    Files = glob.glob(path + "/*" + extension) # list of all (mp3/or else) files in the folder
    return Files

def stripName(path:str):
    names  = path.split('/')
    songName = names[-1]
    songNameLst = songName.split('.')
    songName = songNameLst[0]
    return songName

def  generateTxt(inputMixedSong : 'audioSpectogram',hashMode:str="perception"):
    files =  loopFolder('/home/adel/dsp-task4/songs','.mp3')

    hashFile = open("hashing-output/hashing.txt","w") 

    similarityScore = open("hashing-output/similarityScore.txt","w")

    MixedSpectHash,MixedMffcHash,MixedTonnetzHash,MixedChromaHash,MixedTimes,MixedFrequencies,MixedSpectrogram = inputMixedSong.getData()

    hashFile.write("{ \n") 
    for i in range(len(files)):
        songName =  stripName(files[i])

        print("NAME: ",songName)

        song = audioSpectogram(files[i],i,hashMode)
        spectHash,mffcHash,tonnetzHash,chromaHash,times,frequencies,spectrogram = song.getData()        
        
        hashFile.write("Name:{},spectHash:{},mffcHash:{},tonnetzHash:{},chromaHash:{}\n".format(songName,spectHash,mffcHash,tonnetzHash,chromaHash))
       
       
        spectScore = 100 - (spectHash - MixedSpectHash)
        mffcScore = 100 - (mffcHash - MixedMffcHash)
        tonnetzScore = 100 - (tonnetzHash - MixedTonnetzHash)
        chromaScore = 100 - (chromaHash - MixedChromaHash)
        totalScore = (spectScore + mffcScore + tonnetzScore + chromaScore)/4
       
        similarityScore.write("{},{},{},{},{},{}\n".format(songName,spectScore,mffcScore,tonnetzScore,chromaScore,totalScore))
        
        
        del song
        # gc.collect()
    hashFile.write("} \n")     
    hashFile.close()
    similarityScore.close()


def readFromTxt():
    hashFile = open("hashing-output/hashing.txt",'r')
    songsData =  hashFile.read().split('\n')[1:-2]
    return songsData

def extractFromline(dataLine:str):
    dataLine = list(map(functools.partial(str.split,sep = ','),dataLine))
    for i in range(len(dataLine)):

        dataLine[i] = list(map(functools.partial(str.split,sep = ':'),dataLine[i]))
        for j in range(len(dataLine[i])):
            
            dataLine[i][j] = dataLine[i][j][-1]
    return dataLine


def mix(path1:str,path2:str,ratio:float):
    x1 , sr1 = librosa.load(path1, duration=60.0)
    x2 , sr2 = librosa.load(path2, duration=60.0)
    x1=x1*ratio
    x2=x2*(1-ratio)
    x=x1+x2
    temp = mktemp('.wav')
    
    sf.write(temp,x ,sr1)
    # print(temp)
    sound = AudioSegment.from_wav(temp)

    sound.export('mixed.mp3', format="mp3")


def sortedScores():
    scoreFile = open("hashing-output/similarityScore.txt",'r')
    songsData =  scoreFile.read().split('\n')[:-1]#read lines into a list
    songsData = list(map(functools.partial(str.split,sep = ','),songsData))
    sortedSongsScores = sorted(songsData, key=lambda x: x[5],reverse=True)
    return sortedSongsScores
# sortedScores()
# mix('songs3/franksinatra_my_way_music_28.mp3','songs3/Birdy_strange_birds_10_vocals.mp3',0)

# hehe = audioSpectogram('/home/adel/dsp-task4/songs/Sam Smith_Too_Good_At_Goodbyes_vocals_05.mp3')
# hehe = audioSpectogram('Sam Smith_Too_Good_At_Goodbyes_music_05.mp3')
# hehe = audioSpectogram('Sam Smith_Too_Good_At_Goodbyes_05.mp3')
# hehe = audioSpectogram('Sia_Alive_05.mp3',0)





# mix('songs/Sia_Alive_05.mp3','songs/Sam Smith_Too_Good_At_Goodbyes_music_05.mp3',0.5)
# inputSong = audioSpectogram('/home/adel/dsp-task4/mixed.mp3',99,"wavelet")
# generateTxt(inputSong,"wavelet")