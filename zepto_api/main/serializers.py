from rest_framework import serializers

from .models import Library, Author, Book


class LibraryListSerializer(serializers.ModelSerializer):
    """Список Библиотек"""

    class Meta:
        model = Library
        fields = '__all__'




class AuthorListSerializer(serializers.ModelSerializer):
    """Список Авторов"""


    class Meta:
        model = Author
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
    """Список Авторов"""

    class Meta:
        model = Book
        fields = '__all__'