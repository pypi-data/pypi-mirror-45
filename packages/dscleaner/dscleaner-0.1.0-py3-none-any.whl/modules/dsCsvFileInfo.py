from . import IFileInfo
import pandas as pd

class dsCsvFileInfo(IFileInfo.IFileInfo):

    def __init__(self, samples, samplerate):
        self._samples = samples
        self._samplerate = samplerate
        pass

    def __enter__(self):
        return self

    def __exit__(self,type,value,traceback):
        self.close()

    def getSamples(self):
        return self._samples

    def getSamplerate(self):
        return self._samplerate
    
    def getNumberOfFrames(self):
        return len(self._samples)
    
    def getNumChannels(self):
        return self._samples.shape[1]

    def getFilepath(self):
        raise NotImplementedError("Not avaliable in csvFIle")

    #WRITE
    def setSamples(self, samples, framerate = None):
        self._samples = samples
        self._samplerate = framerate
        return
    
    def truncate(self, num_frames):
        self._samples = self._samples[:num_frames]
        return

    def addSamples(self, samples):
        self._samples.append(samples)
        return 

    def close(self):

        return