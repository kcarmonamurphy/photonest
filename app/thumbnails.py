import os
from subprocess import check_output

def generate_thumbnails_if_missing(path):

  # if there is no thumbnail dir for folder, create one
  if not path.thumbnail_dir.is_dir():
      os.mkdir(path.thumbnail_dir)

  # create small thumbnail image
  if not path.thumbnail('small').is_file():
      try:
          check_output(["convert", path.app, "-strip", "-resize", "256x256", path.thumbnail('small')])
      except:
          print("Error generating 256x256 thumbnail")

    # if not os.path.isfile(path.thumbnail.medium):
    #     try:
    #         check_output(["convert", path.app.file, "-strip", "-resize", "512x512", path.thumbnail.medium])
    #     except:
    #         print("Error generating 512x512 thumbnail")