import os
from .path_helper import *
from subprocess import check_output

def generateThumbnailsIfNotPresent(file):

    dir_app_path = getDirAppPathFromFileAppPath(file.path)
    dir_thumbnail_app_path = getThumbnailAppPathFromDirAppPath(dir_app_path)

    if not os.path.exists(dir_thumbnail_app_path):
        os.mkdir(dir_thumbnail_app_path)

    thumbnail_path_256 = os.path.join(
        dir_thumbnail_app_path, 
        file.name + '_thumbnail_256'
    )

    thumbnail_path_512 = os.path.join(
        dir_thumbnail_app_path,
        file.name + '_thumbnail_512'
    )

    if not os.path.isfile(thumbnail_path_256):
        try:
            check_output(["convert", file.path, "-strip", "-resize", "256x256", thumbnail_path_256])
        except:
            print("Error generating 256x256 thumbnail")

    if not os.path.isfile(thumbnail_path_512):
        try:
            check_output(["convert", file.path, "-strip", "-resize", "512x512", thumbnail_path_512])
        except:
            print("Error generating 512x512 thumbnail")