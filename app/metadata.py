import json
from subprocess import check_output

class MetaData():
    """
    Module for getting, setting, and writing metadata
    to image files using the `exiftool` program by
    Phil Harvey
    """

    '''
    Initialization of Class
    -----------------------
    '''

    def __init__(self, file_path): # this method creates the class object.
        self.file_path = file_path
        self.args_list = []

        try:
            output = check_output(["exiftool", "-json", self.file_path])
        except:
            print("something went wrong")

        self.metadataDict = json.loads(output)[0]

    '''
    Private Methods
    ---------------
    '''

    def _getMetaData(self, key=None):

        if key:
        	return self.metadataDict.get(key, '')

        return self.metadataDict

    def _setMetaData(self, key, value):

        arg = "-" + key + "=" + value

        self.args_list.append(arg)

    def _showArgsList(self):
        pass
        # print(self.args_list)

    '''
    Public Methods
    ----------------
    '''
        
    def getImageSize(self):

    	return self._getMetaData("ImageSize")

    def getFileSize(self):

    	return self._getMetaData("FileSize")

    def getFileType(self):

    	return self._getMetaData("FileType")

    def getMake(self):

    	return self._getMetaData("Make")

    def getModel(self):

    	return self._getMetaData("Model")

    def getMegapixels(self):

    	return self._getMetaData("Megapixels")

    def getModifyDate(self):

    	return self._getMetaData("ModifyDate")

    def getCreateDate(self):

    	return self._getMetaData("CreateDate")

    def getGPSPosition(self):

    	return self._getMetaData("GPSPosition")

    def getShutterSpeed(self):

    	return self._getMetaData("ShutterSpeed")

    def getDescription(self):

        return self._getMetaData("Description")

    def getTitle(self):

        return self._getMetaData("Title")

    def getKeywords(self):

        value = self._getMetaData("Keywords")

        if (type(value) is str):
            return [value]

        return value

    def setTitle(self, value):

        return self._setMetaData("Title", value)

    def setDescription(self, value):

        return self._setMetaData("Description", value)

    def setKeywords(self, lst):

        assert (type(lst) is list), 'should be list'

        for value in lst:
            self._setMetaData("Keywords", value)

        if not lst: # if lst is empty
            self._setMetaData("Keywords", "")


    def write(self):
        """Write metadata to image.

        Runs `exiftool` program against list of arguments
        defined in `self.args_list`

        Returns False if Exception was raised or if not exactly
        1 image was updated
        """

        cmd = ['exiftool'] + self.args_list + [self.file_path] + ['-overwrite_original']

        try:
            output = check_output(cmd)

            # output respone should be '1 image files updated'
            if output.decode("utf-8").lstrip() != '1 image files updated':
                return True
            return False

        except:
            return False





