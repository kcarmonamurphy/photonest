import os
from subprocess import check_output
from .path import Path

def generateThumbnailsIfNotPresent(file):

    path = Path(file.path, 'app')

    if not os.path.exists(path.thumbnail.dir):
        os.mkdir(path.thumbnail.dir)

    if not os.path.isfile(path.thumbnail.small):
        try:
            check_output(["convert", path.app.file, "-strip", "-resize", "256x256", path.thumbnail.small])
        except:
            print("Error generating 256x256 thumbnail")

    # if not os.path.isfile(path.thumbnail.medium):
    #     try:
    #         check_output(["convert", path.app.file, "-strip", "-resize", "512x512", path.thumbnail.medium])
    #     except:
    #         print("Error generating 512x512 thumbnail")