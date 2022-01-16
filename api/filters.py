import django_filters
from books.models import Publication, Author
from django.db.models import Q


class PublicationFilter(django_filters.FilterSet):
    """
    Filter allowing filtering by mostly the same fields as in index page.
    Argument for publication date is a date in YYYY-MM-DD format.
    It can be filtered in 3 ways. Use publication_date for exact date,
    publication_before or publication_after for filtering before, and after
    specific date.
    Before and after filters can be used as the same time for a date range.
    """
    # Like publication_date, but to be used only as publication_after or
    # publication_before (date) param
    publication = django_filters.DateFromToRangeFilter(
        field_name='publication_date')

    class Meta:
        model = Publication
        fields = ['id', 'author', 'title', 'language', 'publication_date',
                  'publication']


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
        expression
        :param queryset: queryset that we are searching, originating from view
        :param name: query string field name. Here it is 'search'
        :param value: inputed value that will be used to search through
        model fields
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
        Searches through all Publication field using OR operator from django
        Q expression
        :param queryset: queryset that we are searching, originating from view
        :param name: query string field name. Here it is 'search'
        :param value: inputed value that will be used to search through
        model fields
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

        publication_queryset = publication_queryset.filter(q_query)
        return publication_queryset
