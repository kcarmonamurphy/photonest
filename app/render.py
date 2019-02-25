
def fetch_thumbnail(path):
  return open(path.thumbnail(), "rb").read()

def fetch_fullsize_image(path):
  return open(path.app, "rb").read()