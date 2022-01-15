from rest_framework import serializers

from books.models import Publication, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'author']


class PublicationSerializer(serializers.ModelSerializer):
    queryset = Author.objects.all()
    author = AuthorSerializer(queryset, read_only=True)

    class Meta:
        model = Publication
        fields = ['id', 'url', 'author', 'publication_date', 'publication_date_type',
                  'isbn', 'page_count', 'book_cover', 'language']

