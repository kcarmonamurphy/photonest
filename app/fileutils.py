import os
import magic
from datetime import datetime
import pytz
from django.utils import timezone

class FileUtils():
  """
  Module containing various file utilities used in view methods
  """

  @staticmethod
  def mimetype_is_image(path):
    '''
    Accepts a path string value
    '''
    mime_type = magic.from_file(str(path), mime=True)
    mime_category = mime_type.split('/')
    if mime_category[0] == 'image':
      return True
    return False

  @staticmethod
  def get_last_modified_datetime(path):
    '''
    Accepts a PurePath value
    '''
    epoch_time = os.path.getmtime(path)
    date_time = datetime.utcfromtimestamp(epoch_time)
    return timezone.make_aware(date_time, timezone=pytz.UTC)
