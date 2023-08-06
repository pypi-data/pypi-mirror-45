import os
import numpy as np
class dsFileUtil():

    def __init__(self,f):
        from . import IFileInfo
        assert issubclass(type(f),IFileInfo.IFileInfo),"Not a specialization of IFileInfo" #if not, ded
        self.file = f
    
    def __enter__(self):
        return self

    def __exit__(self,type,value,traceback):
        pass

    @staticmethod
    def merger(pathIn,pathOut):
        """
        Receives a directory and joins all the files together
        NOT IMPLEMENTED
        """
        raise NotImplementedError

    def fix_duration(self, expected_duration, grid_rate = 50):
        """
            Fixes the file to the expected duration
            A new file is created with the same name on the targetDirectory
            Args:
                expected_duration: Duration the file should have in minutes.
                grid_rate: frequency of the grid in hertz, this is used to discover the wave signal in order to upsample
            Returns:
                data: array with the expected duration
        """
        data = self.file.getSamples()
        sample_rate = self.file.getSamplerate()

        actual_frame_number = len(data)
        expected_frame_number = sample_rate * expected_duration * 60
        #rate * minutes * seconds
        if(actual_frame_number == expected_frame_number):
            #no cleaning needed
            return
        else:
            if(actual_frame_number > expected_frame_number):
                self.file.truncate(expected_frame_number)
            else:
                #needs adding
                wave_length = int((sample_rate / grid_rate) )
                last_wave = list(data[-wave_length:]) # gets the last wave_length elements
                samples_missing = int(expected_frame_number - actual_frame_number)
                from math import ceil
                last_wave *= ceil(samples_missing/wave_length) #replicates the last wave several times
                last_wave = np.asarray(last_wave[:samples_missing]) #removes any more than its actually missing
                self.file.addSamples(last_wave)

    def resample(self, new_framerate, method = 'kaiser_fast'):
        """
            Resample:
                Resamples the data to the new framerate using librosa resample,
            
            Args:
                data: numpy.array shaped like (num_frames,num_channels) is expected to receive the soundfile.getSamples()
                    not the transposed array,
                    NOTE: in theory can use any amount of channels.
                original_framerate: the original framerate the data array uses.
                new_framerate: the new framerate that data will be resampled to.
                method: Methods that librosa accepts are also accepted here,uses `kaiser_fast` by default;
            Returns:
                the original file but resampled to the new_framerate    
        """
        data = self.file.getSamples()

        import librosa
        new_data = librosa.resample(data.T, self.file.getSamplerate(), new_framerate, res_type=method, fix=True)
        self.file.setSamples(new_data.T,new_framerate)