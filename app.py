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




###########################################################################
# What to do ?
# 1 - read mp3 files from the group folder 
    # make a function that loops throught the folder and read each file and call functions 2 and 3 
# 2 - get the spectogram of each file being read from the folder and store it locally in txt file as 2 array
    #  make a function (Specto) that take an array(mp3 array) and get it's spectogram 
    #  write the out of (Specto) into txt file 

# 3 - get the feature of each spectogram and store it 
    # make function (Feature) that takes the out of (specto) and get the features of it and store it locally in txt file ???? to be explained later 
# 4 - get the hashing of each spectogram and store it 
    # make a function (Hash) that takes the out of (specto) amd hash it into a (string (????)) and write it into a txt file 
     
# 5 - Make a function that reads the input songs and get its spectrogram
    # read the two input songs and mix them both into a single file and get the (specto) and hash it and get it's feature 
# 6 - make a function that searches through the txt files of specto features and hashing to find a matching or similar file to the input  
  
###########################################################################

###########################################################################

# functions to implement 
# 1 - (read) mp3
# 2 - (loop) throught the folder
# 3 - (specto) 
# 4 - (hash)
# 5 - (write into txt)
# 6 - (search)
# 7 - (feature)
###########################################################################


class audioSpectogram():

    def __init__(self,path:str,id:int):
        self.path = path
        self.id = id
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
        gc.collect()
        print("objct {} deleted :X".format(self.id))

    def readAudio(self):

        # mp3_audio = AudioSegment.from_mp3('Sam Smith_Too_Good_At_Goodbyes_05.mp3')  # read mp3
        # mp3_firstMin = mp3_audio[:60000] #Read first min 
        # mp3_firstMin.set_channels(1) # convert to mono
        # wname = mktemp('.wav')  # use temporary file
        # mp3_firstMin.export('hoho.wav', format="wav",)  # convert to wav
                
        self.samples , self.sample_rate = librosa.load(self.path, duration=60.0) # Read mp3
        # self.sample_rate,self.samples =  wavfile.read(self.path)  # read wav file
        self.lenght = self.samples.shape[0]/self.sample_rate # length of the song (in secs) 

        if len(self.samples.shape) == 2: #Check if setreo and convert it to mono
            self.samples = np.mean(self.samples, axis=1)
        
        print(self.samples.shape)    
        print('time (secs): ',self.lenght)

        # check if the length of the song is more than 1 min, if so ,clip it (now it's trivial  T_T )
        if self.lenght > 60:
            min1Index =self. sample_rate * 60
            self.samples = self.samples[:min1Index]
            self.lenght = self.samples.shape[0]/self.sample_rate
            print("time after check (secs):",self.lenght)
        
        
        # self.features()        

    def setData(self):
        spect = self.spectro()
        ft1,ft2,ft3 = self.features()
        self.spectHash = self.hashFile(spect)
        self.mffcHash  = self.hashFile(ft1)
        self.tonnetzHash = self.hashFile(ft2)
        self.chromaHash = self.hashFile(ft3)
        print(ft1,ft2,ft3)
        print('spect: ',self.hashFile(spect))
        print('mffc: ',self.hashFile(ft1))
        print('tonnetz: ',self.hashFile(ft2))
        print('chroma: ',self.hashFile(ft3))
        print(self.path) 

    def getData(self):
        return (self.spectHash,self.mffcHash,self.tonnetzHash,self.chromaHash,self.times,self.frequencies,self.spectrogram)    

    def spectro(self):
        self.frequencies,self.times, self.spectrogram = signal.spectrogram(self.samples, self.sample_rate,window='hamming',detrend=False, scaling='spectrum')

        # plt.figure(figsize=(14, 5))
        # plt.tight_layout(pad = 0)
        # plt.pcolormesh(self.times, self.frequencies/1000, 10 * np.log10(self.spectrogram))
        # # plt.imshow(spectrogram)
        # plt.ylabel('Frequency [KHz]')
        # plt.xlabel('Time [sec]')
        # plt.show()
        X = librosa.stft(self.samples)
        Xdb = librosa.amplitude_to_db(abs(X))
        plt.figure(figsize=(14, 5))
        librosa.display.specshow(Xdb, sr=self.sample_rate)
        plt.tight_layout(pad = 0)
        spectFig = mktemp('.png')  # use temporary file
        # spectFig = 'spect.png'
        plt.savefig(spectFig,bbox_inches='tight', transparent=True, pad_inches=0)
        # plt.show()
        return spectFig
    
    
    def hashFile(self,figure:str): # Hashing function , returns a string
        hash = imagehash.phash(Image.open(figure))
        # print(hash)
        return hash

    def features(self):
        # mffcs (Featrue 1)
        mfccs = librosa.feature.mfcc(y=self.samples, sr=self.sample_rate)
        plt.figure(figsize=(10, 6))
        librosa.display.specshow(mfccs)
        plt.tight_layout(pad = 0)
        # mffcFig = 'mffc.png'
        mffcFig = mktemp('.png') # tempfile
        plt.savefig(mffcFig,bbox_inches='tight', transparent=True, pad_inches=0)
        # plt.show()

        #  tonal centroid (feature 2)
        tonnetz = librosa.feature.tonnetz(y=self.samples, sr=self.sample_rate)
        plt.figure(figsize=(10, 6))
        librosa.display.specshow(tonnetz)
        plt.tight_layout(pad = 0)
        # tonnetzFig = 'tonnetz.png'
        tonnetzFig = mktemp('.png') # tempfile
        plt.savefig(tonnetzFig,bbox_inches='tight', transparent=True, pad_inches=0)
        # plt.show()
        
        # chroma (feature 3 )
        chroma = librosa.feature.chroma_cqt(self.samples, sr=self.sample_rate)
        plt.figure(figsize=(10, 6))
        librosa.display.specshow(chroma)
        plt.tight_layout()
        # chromaFig = 'chroma.png'
        chromaFig = mktemp('.png') # tempfile
        plt.savefig(chromaFig,bbox_inches='tight', transparent=True, pad_inches=0)
        # plt.show()
        return (mffcFig,tonnetzFig,chromaFig)


# hehe = audioSpectogram('/home/adel/dsp-task4/Sam Smith_Too_Good_At_Goodbyes_vocals_05.mp3')
# hehe = audioSpectogram('Sam Smith_Too_Good_At_Goodbyes_music_05.mp3')
# hehe = audioSpectogram('Sam Smith_Too_Good_At_Goodbyes_05.mp3')
# hehe = audioSpectogram('Sia_Alive_05.mp3')



def loopFolder(path:str,extension:str):
    Files = glob.glob(path + "/*" + extension) # list of all (mp3/or else) files in the folder
    print(Files)
    return Files

def stripName(path:str):
    names  = path.split('/')
    songName = names[-1]
    songNameLst = songName.split('.')
    songName = songNameLst[0]
    print(names)
    print(songName)
    print(songNameLst)
    return songName

def  generateTxt():
    files =  loopFolder('/home/adel/dsp-task4/songs','.mp3')
    hashFile = open("hashing-output/hashing.txt","w") 
    
    hashFile.write("{ \n") 
    for i in range(len(files)):
        songName =  stripName(files[i])

        print("NAME: ",songName)
        spectFile = open("spectrogram-output/"+songName+".txt","w")    # needs to be filled with arrays
        song = audioSpectogram(files[i],i)
        spectHash,mffcHash,tonnetzHash,chromaHash,times,frequencies,spectrogram = song.getData()        
       
        hashFile.write("Name:{},spectHash:{},mffcHash:{},tonnetzHash:{},chromaHash:{};\n".format(songName,spectHash,mffcHash,tonnetzHash,chromaHash))
        spectFile.close()
        del song
        gc.collect()
    hashFile.write("} \n")     
    hashFile.close()
    
# loopFolder('/home/adel/dsp-task4','.mp3')
generateTxt()
