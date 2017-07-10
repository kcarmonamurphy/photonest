import json
from subprocess import check_output

class MetaData():

    def __init__(self, file_path): # this method creates the class object.
        self.file_path = file_path

    def _getMetaData(self, key=None):

        # try:
        output = check_output(["exiftool", "-json", self.file_path])
        # except:
        #     pass

        metadataDict = json.loads(output)[0]

        if key:
        	return metadataDict.get(key, '')

        return metadataDict

    def _setMetaData(self, key, value):

        arg = "-" + key + "=" + value

        try:
            output = check_output(["exiftool", arg, self.file_path])
        except:
            return False

        return True
        
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

    # Writeable Tags

    def getDescription(self):

        return self._getMetaData("Description")

    def setDescription(self, value):

        return self._setMetaData("Description", value)

    def getTitle(self):

        return self._getMetaData("Title")

    def setTitle(self, value):

        return self._setMetaData("Title", value)

    def getKeywords(self):

        return self._getMetaData("Keywords")

    def setKeywords(self, value):

        return self._setMetaData("Keywords", value)

    def getRating(self):

        return self._getMetaData("Rating")

    def setRating(self, value):

        return self._setMetaData("Rating", value)





