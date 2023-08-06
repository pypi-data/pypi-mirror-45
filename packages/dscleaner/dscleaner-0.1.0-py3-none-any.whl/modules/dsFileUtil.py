import os #for listing directories etc
import numpy as np
class dsFileUtil():

    def __init__(self,f):
        from modules import IFileInfo
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
        #TODO NEED TO  test for data shape
        data = self.file.getSamples()

        import librosa
        new_data = librosa.resample(data.T, self.file.getSamplerate(), new_framerate, res_type=method, fix=True)
        self.file.setSamples(new_data.T,new_framerate)
        
    @staticmethod
    def get_UKDALE_duration(dataset_array, index, file):
        """
            get_UKDALE_duration:
                Specific function to retrieve the duration and name for the ukdale dataset
            Args: 

            Returns:
                A tuple with the duration as the first element and the name for the file on the second 
        """
        name = "Hour-"+str(index)+".wav"
        try:
            timestamp_next_file = dataset_array[int(index)+1][3:13]
            timestamp_cur_file = dataset_array[index][3:13]
            duration = int(timestamp_next_file) - int(timestamp_cur_file)
            duration /= 60
            print(duration)
        except IndexError:
            duration = file.get_rounded_duration()/60
            #it divides by 60 because it will then be multiplied by 60 when doing the data_clean
            #if it is the last file it will throw this exception, hence doing this
        return {"duration":duration, "name":name}
    '''
    @staticmethod
    def data_cleaner(dataset_array,new_path,cur_path,dataset_specific_function, new_framerate, old_framerate, num_channels, grid_rate, filetype):
        """
            data_cleaner:
                Fixes the length of the file, resamples the file to the
                    `old_framerate` framerate, and saves the new file
                    to `new_path`
            Args:
                dataset_array:
                    array with filenames of the files 
                    that are going to be cleaned
                new_path:
                    path where the new files are going to
                        be written to
                cur_path:
                    Path where the files are currently
                dataset_specific_function:
                    function that returns a tuple with
                        the info of the expected duration and 
                    filename
                new_framerate:
                    the final framerate the files will have
                old_framerate:
                    The framerate the input files have
                num_channels:
                    Number of channels each file has
                grid_rate:
                    Rate at which the grid is recorded
                filetype:
                    filetype the files will have(not sure if is needed)
            
        """ 
        for i in range(0,len(dataset_array)): #did it with range because i want the the iteration number and not the actual value
            path = os.path.join(cur_path,dataset_array[i])
            file = SoundFileInfo(path)
            tmp_tuple = dataset_specific_function(dataset_array, i, file)
            fixed_data = Util.fix_duration(file.getSamples(), tmp_tuple["duration"], num_channels, old_framerate, grid_rate)
            resampled_data = Util.resample(fixed_data,old_framerate,new_framerate)
            new_filepath = os.path.join(new_path,tmp_tuple["name"])
            file.create_file(resampled_data.T, new_filepath, new_framerate)
            file.close()
        '''
            