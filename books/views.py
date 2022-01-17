import urllib
from datetime import datetime

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from .forms import form_date_errors, PublicationSearchForm, AuthorForm, \
    PublicationForm, SearchForImportBookForm
from .models import Publication, Author
from .utils import check_date_format, append_to_url_query


class ListPublicationsView(View):
    def get(self, request):
        """
        Displays all books in a table, and a book publication search form.
        :param request:
        :return:
        """
        form = PublicationSearchForm()
        books = Publication.objects.select_related('author')

        context = {'books': books, 'form': form}
        return render(request, 'books/index.html', context=context)

    def post(self, request):
        """
        Searches and displays found book publications in a table.
        :param request:
        :return:
        """

        form = PublicationSearchForm(request.POST)
        books = Publication.objects.select_related('author')

        if form.is_valid():
            title = form.cleaned_data['title'].strip() if form.data[
                'title'].strip() else None
            author = form.cleaned_data['author'].strip() if form.data[
                'author'].strip() else None
            language = form.cleaned_data['language'].strip() if form.data[
                'language'].strip() else None
            published_from = str(form.cleaned_data['published_from']) if \
                form.data['published_from'].strip() else None
            published_to = str(form.cleaned_data['published_to']) if form.data[
                'published_to'].strip() else None

            queryset = Publication.objects.select_related('author')

            if title:
                queryset = queryset.filter(title__icontains=title)
            if author:
                queryset = queryset.filter(author__author__icontains=author)
            if language:
                queryset = queryset.filter(language=language)
            if published_from:
                date = datetime.strptime(published_from, '%Y-%m-%d')
                queryset = queryset.filter(publication_date__gte=date)
            if published_to:
                date = datetime.strptime(published_to, '%Y-%m-%d')
                queryset = queryset.filter(publication_date__lte=date)

            context = {'books': queryset, 'form': form}
            return render(request, 'books/index.html', context=context)

        context = {'books': books, 'form': form}

        # Add helpful informations about form errors to context
        if form_date_errors['invalid'] in str(form.errors):
            error_string = "Błąd: data powinna używać formatu [dzień].[" \
                           "miesiąc].[rok] " \
                           "na przykład: 23.02.2015"
            context['form_date_error'] = error_string

        return render(request, 'books/index.html', context)


class CreateFormsView(View):
    def get(self, request):
        """
        Displays empty form for adding authors and publications.
        :param request:
        :return:
        """
        author_form = AuthorForm()
        publication_form = PublicationForm()

        context = {'author_form': author_form,
                   'publication_form': publication_form}
        return render(request, 'books/add_forms.html', context=context)

    def post(self, request):
        """
        Adds author or publication using form data.
        :param request:
        :return:
        """
        author_form = AuthorForm()
        publication_form = PublicationForm()
        expected_publication_form_fields = (
            'title', 'author', 'publication_date', 'publication_date_type',
            'isbn', 'page_count', 'book_cover', 'language')
        result_message = ""
        if 'author' in request.POST.keys() and len(request.POST.keys()) == 2:
            form = author_form = AuthorForm(request.POST)
        elif all(field in request.POST.keys() for field in
                 expected_publication_form_fields):
            form = publication_form = PublicationForm(request.POST)
        else:
            result_message += "<p>błąd: Otrzymano nieoczekiwany formularz.</p>"

        if form.is_valid():
            result_message = "Operacja zakończona sukcesem."
            form.save()
        else:
            result_message = form.errors

        context = {
            'author_form': author_form,
            'publication_form': publication_form,
            'result_message': result_message
        }
        return render(request, 'books/add_forms.html', context=context)


class EditPublicationFormView(View):
    def get(self, request, book_id):
        """
        Displays empty form used for editing publication specified by book_id
        :param request:
        :param book_id: id of publication
        :return:
        """
        publication = get_object_or_404(Publication, id=book_id)
        form = PublicationForm(instance=publication)
        context = {'form': form}
        return render(request, 'books/edit_publication.html', context)

    def post(self, request, book_id):
        """
        Edits specified publication using data from form.
        :param request:
        :param book_id: id of publication
        :return:
        """
        publication = get_object_or_404(Publication, id=book_id)
        form = PublicationForm(request.POST, instance=publication)
        context = {}
        if form.is_valid():
            form.save()
            context['form'] = PublicationForm(
                instance=publication)  # Display updated values to user
            # Display result to user
            context[
                'result_message'] = "Publikacja pomyślnie zmodyfikowana."

            return render(request, 'books/edit_publication.html', context)
        context[
            'result_message'] = "Nie udało się zmodyfikować publikacji. " \
                                "Sprawdź pola i spróbuj ponownie."
        return render(request, 'books/edit_publication.html', context)


class DeletePublicationView(View):
    def post(self, request, book_id):
        """
        Deletes specified in argument book and redirects to index page.
        :param request:
        :param book_id: id number of publication
        """
        publication = get_object_or_404(Publication, id=book_id)
        publication.delete()
        return HttpResponseRedirect(reverse('index'))


class ImportView(View):
    def get(self, request):
        """
        Import view, that displays form allowing user to search
        external api for books to import.
        :param request:
        :return:
        """
        form = SearchForImportBookForm()
        context = {'form': form}

        return render(request, 'books/import_book_form.html', context)

    def post(self, request):
        """
        Searches external api for books.
        External url where data will be taken from is constructed using
        query strings using every included form field.
        :param request:
        :return:
        """
        form = SearchForImportBookForm(request.POST)
        base_url = 'https://www.googleapis.com/books/v1/volumes'
        url_query = '?q='

        if form.is_valid():
            result = append_to_url_query(form, 'q', url_query, True)
            fields_to_add = list(form.cleaned_data.keys())[
                            1:]  # All fields except mandatory q field
            for field in fields_to_add:
                result = append_to_url_query(form, field, result)
            result_url = base_url + result

            response = requests.get(result_url)
            response_dict = response.json()

            # No books were found, and response wont contain 'items' key
            if 'items' not in response_dict.keys():
                return render(request, 'books/import_book_form.html',
                              {'form': form})
            found_books = []

            for item in response_dict['items']:
                title = item['volumeInfo']['title']
                try:
                    author = ", ".join(item['volumeInfo']['authors'])
                except KeyError:
                    author = None

                publication_date = self.get_value_or_none(item,
                                                          ['volumeInfo',
                                                           'publishedDate'])
                isbn = self.get_value_or_none(item, ['volumeInfo',
                                                     'industryIdentifiers', 0,
                                                     'identifier'])
                page_count = self.get_value_or_none(item, ['volumeInfo',
                                                           'pageCount'])
                book_cover = self.get_value_or_none(item, ['volumeInfo',
                                                           'imageLinks',
                                                           'thumbnail'])
                language = self.get_value_or_none(item,
                                                  ['volumeInfo', 'language'])

                found_books.append(
                    {
                        'title': title,
                        'author': author,
                        'publication_date': publication_date,
                        'isbn': isbn,
                        'page_count': page_count,
                        'book_cover': book_cover,
                        'language': language
                    }
                )
        context = {'form': form, 'found_books': found_books}
        return render(request, 'books/import_book_form.html', context)

    def get_value_or_none(self, source_dict, params):
        """
        Iterates over source dictionary, step by step by using every single
        key in param argument. If key in any moment of iteration does
        not exist, it will return None.
        :param source_dict: Dictionary imported from external google api
        :param params:  list containing strings of each key we want to search.
                        For example with params=['volumeInfo', 'publishedDate']
                        function will return same result as in
                        source_dict['volumeInfo']['publishedDate'] or None if
                        key in any of steps doesn't exist.
        :return output: if value is extracted successfully from source_dict
        :return None: if KeyError occured during attempt to get value
        """
        output = source_dict
        for param in params:
            try:
                output = output[param]
            except KeyError:
                return None
        return output


class ImportSingleBookView(View):
    def post(self, request):
        """
        Extracts query strings from url, creates publication, displays
        main import page with success message.
        :param request:
        :return:
        """
        book_title = request.GET.get('book_title')
        book_author = request.GET.get('book_author')
        book_publication_date = request.GET.get('publication_date')
        book_isbn = request.GET.get('book_isbn')
        page_count = None if request.GET.get(
            'page_count') == 'None' else request.GET.get('page_count')
        book_cover = request.GET.get('book_cover')
        book_language = request.GET.get('book_language')

        # book cover received from api can contain more query strings,
        # not picked up in book_cover variable above
        # code below fixes that issue and adds missing params to it
        url = request.GET.urlencode()
        query_strings = urllib.parse.parse_qs(url)
        additional_params = ('printsec', 'img', 'zoom', 'edge', 'source')
        for param in additional_params:
            param_or_none = query_strings.get(param)
            if param_or_none:
                book_cover += f"&{param}={param_or_none[0]}"

        form = SearchForImportBookForm()
        if book_author:
            try:
                author = Author.objects.get(author=book_author)
            except Author.DoesNotExist:
                author = Author.objects.create(author=book_author)

        parsed = check_date_format(book_publication_date)
        date_correct_format, date_filter_format = parsed[0], parsed[1]
        Publication.objects.create(title=book_title,
                                   author=author,
                                   publication_date=date_correct_format,
                                   publication_date_type=date_filter_format,
                                   isbn=book_isbn,
                                   page_count=page_count,
                                   book_cover=book_cover,
                                   language=book_language)

        result_message = f"Zaimportowano książkę {book_title}."
        context = {'form': form, 'result_message': result_message}
        return render(request, 'books/import_book_form.html', context)
