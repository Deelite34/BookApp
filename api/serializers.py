from books.models import Publication, Author
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'author']


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ['id', 'title', 'url', 'author', 'publication_date',
                  'publication_date_type',
                  'isbn', 'page_count', 'book_cover', 'language']
