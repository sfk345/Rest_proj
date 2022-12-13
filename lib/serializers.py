from rest_framework import serializers

from .models import *


class BooksSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'yearOfRel', 'genre', 'category', 'publisher', 'photoPreview', 'bookFile')


class AuthorsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('objects', 'name', 'lastName', 'middle_name', 'dateOfBirth')
