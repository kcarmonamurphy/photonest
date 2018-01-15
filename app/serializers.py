from .models import Image, Folder

from rest_framework import serializers

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('uri', 'name', 'size', 'title', 'description', 'parent')

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('uri', 'name')