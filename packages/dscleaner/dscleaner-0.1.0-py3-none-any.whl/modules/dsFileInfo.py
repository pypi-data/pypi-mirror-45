from . import IFileInfo
import numpy as np
import soundfile as sf

class dsFile(IFileInfo.IFileInfo):
    """
        Creates a file in a temporary location
        Gets edited through the other classes
        and dsFileWriter writes converts and writes to another location
    """
    def __init__(self,path):
        super().__init__(path)
        self._path = path

        import tempfile
        self._tmpPath = tempfile.gettempdir()

        try:
            import shutil
            self._tmpPath = shutil.copy(self._path,self._tmpPath)
        except FileExistsError:
            print("FEXISTS l25")
            pass
        self._initinfo()

    def __enter__(self):
        return self

    def __exit__(self,type,value,traceback):
        self.close()

    def _initinfo(self):
        with sf.SoundFile(self._tmpPath, mode ='r') as rfile:
            self._samplerate = rfile.samplerate
            self._frames = rfile.read()
            self._numchannels = rfile.channels
        return

    #================READ METHODS ==================#

    def getFilepath(self):
        return self._path

    def getNumberOfFrames(self):
        return len(self.getSamples())
            
    def getSamplerate(self):
        return self._samplerate

    def getNumChannels(self):
        """
        Returns:
            Number of channels the file has
        """
        return self._numchannels

    def getDuration(self):
        """Returns the duration of the file in seconds"""
        return self.getNumberOfFrames()/self.getSamplerate()

    def get_rounded_duration(self):
        """
            Returns the rounded duration in seconds
        """
        from math import ceil
        rounded_duration = ceil(self.getDuration()) #in seconds
        return rounded_duration 
    
    def getSamples(self):
        """
        Reads all of the samples in the file
        Returns: 
            numpy array containing the samples
        """
        return self._frames
        
    #================WRITE METHODS ==================#

    def setSamples(self, samples, samplerate = None):
        """
            Writes the ´samples´ as the new samples in the file
            samples: numpy array with (n,x), where x is the number of channels
            samplerate: the new sample rate the file will have, if none it will use the initial samplerate
        """ 
        if (samplerate == None):
            samplerate = self.getSamplerate()
        samples = self._soundfile_array_converter(samples)
        with sf.SoundFile(self._tmpPath, mode = 'w', samplerate = self.getSamplerate(), channels = self.getNumChannels()) as wfile:
            wfile.truncate(0) #removes all the samples in the file                
        sf.write(self._tmpPath,samples,samplerate)
        self._initinfo()

    def truncate(self,num_frames):
        """
            Truncates the file to only have until num_frames
        """
        #with sf.SoundFile(self._tmpPath, mode = 'w', samplerate = self.getSamplerate(), channels = self.getNumChannels()) as wfile:
        #   wfile.truncate(num_frames)
        self.setSamples(self.getSamples()[:num_frames])
        self._initinfo()

    def addSamples(self,samples):
        """
            Appends the samples to the file
            Similar to ´setSamples()´ 
        """
        samples = self._soundfile_array_converter(samples)
        with sf.SoundFile(self._tmpPath,mode = 'w', samplerate = self.getSamplerate(),channels = self.getNumChannels()) as wfile:
            #if it is seekable then it goes to the beginning and writes all the samples
            #else it writes normally
            if(wfile.seekable()):

                wfile.seek(-1,whence = sf.SEEK_END)
                wfile.write(samples)
                print("seelable", len(samples))

            else:
                wfile.write(np.append(self.getSamples(),samples,axis = 0))
        self._initinfo()

    #================MISC METHODS ==================#
 
    def _soundfile_array_converter(self,array):
        """
            Checks if it has the correct array shape to be worked by pysoundfile
            If not, it will transpose de array
            Args:
                array: ndarray to convert
            Returns:
                array: the converted array
        """
        if(array.shape[1] > 9): #meaning it doesnt represent the number of channelsnumber of channels
            array = array.T
        return array
    
    def close(self):
        """
        Must always be called or the file won't be accessible by other processes
        """
        import os 
        os.unlink(self._tmpPath)
