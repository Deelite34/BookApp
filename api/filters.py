import django_filters
from books.models import Publication, Author
from django.db.models import Q


class PublicationFilter(django_filters.FilterSet):
    """
    Filter allowing filtering by mostly the same fields as in index page.
    Publication date can be filtered by publication_date_before or publication_date_after,
    or both at the same time to indicate range.
    """
    publication_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Publication
        fields = ['id', 'author', 'title', 'language', 'publication_date']


class AuthorSearch(django_filters.FilterSet):
    """
    Searches all Author model fields for inputed keyword
    """
    search = django_filters.CharFilter(method='search_fields', label="Search")

    class Meta:
        model = Author
        fields = ['search']

    def search_fields(self, queryset, name, value):
        """
        Searches through all Author field using OR operator from django Q
        :param queryset: queryset that we are searching, originating from view
        :param name: query string field name. Here it is 'search'
        :param value: inputed value that will be used to search through model fields
        :return author_queryset: end result queryset used for searching
        """
        q_query = Q()
        if value.isnumeric():
            q_query |= Q(id=value)
        if value.isalpha():
            q_query |= Q(author__icontains=value)

        author_queryset = Author.objects.filter(q_query)
        return author_queryset


class PublicationSearch(django_filters.FilterSet):
    """
    Searches all Author model fields for inputed keyword
    """
    search = django_filters.CharFilter(method='search_fields', label="Search")

    class Meta:
        model = Publication
        fields = ['search']

    def search_fields(self, queryset, name, value):
        """
        Searches through all Publication field using OR operator from django Q
        :param queryset: queryset that we are searching, originating from view
        :param name: query string field name. Here it is 'search'
        :param value: inputed value that will be used to search through model fields
        :return publication_queryset: end result queryset used for searching
        """
        q_query = Q()
        publication_queryset = Publication.objects
        if value.isnumeric():
            q_query |= Q(id=value)
            q_query |= Q(page_count=value)
            q_query |= Q(author__id=value)
        if value.isalpha():
            q_query |= Q(title__icontains=value)
            q_query |= Q(author__author__icontains=value)
            q_query |= Q(isbn__icontains=value)
            q_query |= Q(language__icontains=value)
            # TODO szukanie daty w jednym z 3 formatów

        publication_queryset = publication_queryset.filter(q_query)
        return publication_queryset
