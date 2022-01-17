from api.filters import PublicationFilter, AuthorSearch, PublicationSearch
from api.serializers import PublicationSerializer, AuthorSerializer
from books.models import Publication, Author
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets


class AuthorFilterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only endpoint, allowing user to filter authors using query strings,
    by id or name.
    Use by adding '?firstparametername=value' then &otherparam=othervalue
    for each next parameter to filter url.
    Fields that can be used for filtering include: 'id' and 'author'.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'author']


class PublicationFilterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only endpoint, allowing user to filter publications by id, author,
    title, language or publication_date.
    Publication date can be filtered only by publication_date
    Use by adding '?firstparametername=value' then &otherparam=othervalue
    for each next parameter to filter url.
    Fields that can be used for filtering include:
    'id', 'author', 'title', 'language', 'publication_date', and also
    'publication_before' and 'publication_after' for after and before specific
    date filtering.
    """
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PublicationFilter


class AuthorSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only endpoint, allowing user to search through all Author model fields
    using search parameter with query string.
    To use, add ?search=<value> to the url. Value can be any of author model
    fields.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filterset_class = AuthorSearch


class PublicationSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only endpoint, allowing user to search through Publication model
    fields using search parameter, with using query string.
    To use, add ?search=<value> to the url. Value can be any of publication
    model fields.
    """
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    filterset_class = PublicationSearch


class AuthorViewSet(viewsets.ModelViewSet):
    """
    Endpoint allowing list, retrieve, create, put, delete, update operations
    on authors.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class PublicationViewSet(viewsets.ModelViewSet):
    """
    Endpoint allowing list, retrieve, create, put, delete operations on
    publications.
    """
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
