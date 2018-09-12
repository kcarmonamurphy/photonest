from .models import Image, Folder
from rest_framework import viewsets
from .serializers import ImageSerializer

class ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

