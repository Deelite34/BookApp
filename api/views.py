from django.shortcuts import render

# Create your views here.
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from api.serializers import PublicationSerializer, AuthorSerializer
from books.models import Publication, Author
from api.filters import PublicationFilter, AuthorSearch, PublicationSearch


class AuthorFilterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only endpoint, allowing user to filter authors using query string, by id or name
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'author']


class PublicationFilterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only endpoint, allowing user to filter publications by id, author, title, language or publication_date.
    Publication date can be filtered
    """
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PublicationFilter


class AuthorSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only endpoint, allowing user to search through Author model fields using search parameter,
    using query string. To use, include search=<value> in query string.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filterset_class = AuthorSearch


class PublicationSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only endpoint, allowing user to search through Publication model fields using search parameter,
    using query string. To use, include search=<value> in query string.
    """
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    filterset_class = PublicationSearch


class AuthorViewSet(viewsets.ModelViewSet):
    """
    Endpoint allowing list, retrieve, create, put, delete operation on authors
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class PublicationViewSet(viewsets.ModelViewSet):
    """
    Endpoint allowing list, retrieve, create, put, delete operation on publications
    """
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


