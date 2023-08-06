class dsFileWriter:

    def __init__(self,futil):
        from . import dsFileUtil, IFileInfo
        if(issubclass(type(futil),IFileInfo.IFileInfo)):
            self.file = futil
        elif(issubclass(type(futil),dsFileUtil.dsFileUtil)):
            self.file = futil.file
        else:
            raise TypeError("Wrong argument type")

    def __enter__(self):
        return self

    def __exit__(self,type,value,traceback):
        pass

    #writer should allow for merging a lot of files 
    #right now its consuming a lot of space, must reduce the bitrate somehow
    #possibilities: numpy64/ using pysoundfilewrite function isntead of lb.write_wav
    def create_file(self,new_filepath,samplerate = None, normalize = True):
        """
            Creates a new file with the extension of the current one
            Arguments:
                data - A multidimensional numpy array(channels x frames)
                new_filepath - The diretory and  name the new file will have, it will convert based on file extension
                samplerate (Optional) - The samplerate the file should have, if not supplied it will use the own file samplerate .
                normalize - If the data should be normalized, True by default
        """

        if(samplerate == None):
            samplerate = self.file.getSamplerate()
        new_filepath = new_filepath.strip() #removes extra whitespace
        if(new_filepath.endswith("/")): 
            new_filepath = new_filepath[:-1]
            #if it ends with a slash removes it

        if("." in new_filepath[2:]): #if it has a dot means it has an extension
            stripped_path = new_filepath.split("/")
            new_filepath = '/'.join(stripped_path[:-1]) #joins the path again
            file_name = stripped_path[-1] #gets the last element (the filename)
        else:
            raise TypeError("It does NOT contain a filename")
            #file_name = self.file._path.split("/")[-1]
        try:
            import os
            os.mkdir(new_filepath)
            #tries to create the directory
        except OSError as e:
            import errno
            if(e.errno != errno.EEXIST):
                raise #if there's an error thats not eexits(file exists/ directory)
            pass
        new_path = new_filepath + '/' + file_name
        
        # normalize
        import soundfile as sf
        import numpy as np
        from librosa.util import normalize as lb_normalize
        samples = self.file.getSamples()
        if normalize and np.issubdtype(samples.dtype, np.floating): #checks if it of floating type
            #since it is librosa data must be transposed
            samples_normalized = lb_normalize(samples.T, norm=np.inf, axis=None) #normalize using librosa
            samples_normalized = samples_normalized.T
        else:
            samples_normalized = samples #or just copies the samples
        sf.write(new_path, samples_normalized, samplerate,format='WAV')
        
        #should copy the current file and overwrite with the new data
        self.file._path = new_path
        return  