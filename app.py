import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from pydub import AudioSegment
from tempfile import mktemp
import numpy as np
# import librosa
import imagehash
from PIL import Image
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
  


# functions to implement 
# 1 - (read) mp3
# 2 - (loop) throught the folder
# 3 - (specto) 
# 4 - (hash)
# 5 - (write into txt)
# 6 - (search)




class audioSpectogram():

    def __init__(self,path:str):
        self.path = path
        self.samples = None
        self.sample_rate = None
        self.lenght = None
        self.hash = None
        self.spectrogram = None
        self.frequencies = None
        self.times = None


    def readAudio(self):

        # mp3_audio = AudioSegment.from_mp3('Sam Smith_Too_Good_At_Goodbyes_05.mp3')  # read mp3
        # mp3_firstMin = mp3_audio[:60000] #Read first min 
        # mp3_firstMin.set_channels(1) # convert to mono
        # wname = mktemp('.wav')  # use temporary file
        # mp3_firstMin.export('hoho.wav', format="wav",)  # convert to wav
        
        self.sample_rate,self.samples =  wavfile.read(self.path)  # read wav file
        self.lenght = self.samples.shape[0]/self.sample_rate # length of the song (in secs) 

        if len(self.samples.shape) == 2: #Check if setreo and convert it to mono
            self.samples = np.mean(self.samples, axis=1)
        
        print(self.samples.shape)    
        print('time (secs): ',self.lenght)

        # check if the length of the song is more than 1 min, if so ,clip it 
        if self.lenght > 60:
            min1Index =self. sample_rate * 60
            self.samples = self.samples[:min1Index]
            self.lenght = self.samples.shape[0]/self.sample_rate
            print("time after check (secs):",self.lenght)

        spect = self.spectro()
        self.hashFile(spect)
        

    def spectro(self):
        self.frequencies,self.times, self.spectrogram = signal.spectrogram(self.samples, self.sample_rate,window='hamming',detrend=False, scaling='spectrum')

        plt.pcolormesh(self.times, self.frequencies/1000, 10 * np.log10(self.spectrogram))
        # plt.imshow(spectrogram)
        plt.ylabel('Frequency [KHz]')
        plt.xlabel('Time [sec]')
        # tempFig = mktemp('.png')  # use temporary file
        tempFig = 'temp.png'
        plt.savefig(tempFig,bbox_inches='tight', transparent=True, pad_inches=0)
        plt.show()
        return tempFig
    
    
    def hashFile(self,figure:str): # Hashing function , returns a string
        hash = imagehash.phash(Image.open(figure))
        print(hash)
        return hash

hehe = audioSpectogram('africa-toto.wav')
hehe.readAudio()