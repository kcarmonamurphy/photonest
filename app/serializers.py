from .models import Image, Folder

from rest_framework import serializers

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'uri', 'name', 'width', 'height', 'title', 'description')

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('id', 'uri', 'name', 'num_items')