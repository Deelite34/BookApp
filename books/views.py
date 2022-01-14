from datetime import datetime

import requests
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from .forms import form_date_errors, PublicationSearchForm, AuthorForm, PublicationForm, SearchForImportBookForm
from .models import Publication, Author


class ListPublicationsView(View):
    def get(self, request):
        """
        Displays all books in a table, and a book publication search form.
        :param request:
        :return:
        """
        form = PublicationSearchForm()
        books = Publication.objects.select_related('author')
        for book in books:
            print('format:', book.publication_date_type)

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
            title = form.cleaned_data['title'].strip() if form.data['title'].strip() else None
            author = form.cleaned_data['author'].strip() if form.data['author'].strip() else None
            language = form.cleaned_data['language'].strip() if form.data['language'].strip() else None
            published_from = str(form.cleaned_data['published_from']) if form.data['published_from'].strip() else None
            published_to = str(form.cleaned_data['published_to']) if form.data['published_to'].strip() else None

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
            error_string = "Błąd: data powinna używać formatu [dzień].[miesiąc].[rok] " \
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

        context = {'author_form': author_form, 'publication_form': publication_form}
        return render(request, 'books/add_forms.html', context=context)

    def post(self, request):
        """
        Adds author or publication using form data.
        :param request:
        :return:
        """
        author_form = AuthorForm()
        publication_form = PublicationForm()
        publication_form_fields = ('title', 'author', 'publication_date',
                                   'isbn', 'page_cound', 'book_cover', 'language')

        if 'author' in request.POST.keys():
            form = author_form = AuthorForm(request.POST)
        elif all(field in publication_form_fields for field in request.POST.keys()):
            form = publication_form = PublicationForm(request.POST)
        else:
            return HttpResponse("<p>błąd: Otrzymano nieoczekiwany formularz.</p>")

        result_message = None
        if form.is_valid():
            result_message = "Operacja zakończona sukcesem."
            form.save()

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
        if form.is_valid:
            form.save()
            context['form'] = PublicationForm(instance=publication)  # Display updated values to user
            context['result_message'] = "Publikacja pomyślnie zmodyfikowana."  # Display result to user
            return render(request, 'books/edit_publication.html', context)
        context['result_message'] = "Nie udało się zmodyfikować publikacji. Sprawdź pola i spróbuj ponownie."
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
        form = SearchForImportBookForm()
        context = {'form': form}

        return render(request, 'books/import_book_form.html', context)

    def post(self, request):
        form = SearchForImportBookForm(request.POST)
        base_url = 'https://www.googleapis.com/books/v1/volumes'
        url_query = '?q='

        if form.is_valid():
            result = self.append_to_url_query(form, 'q', url_query, True)
            fields_to_add = list(form.cleaned_data.keys())[1:]  # All fields except q field
            for field in fields_to_add:
                result = self.append_to_url_query(form, field, result)
            result_url = base_url + result

            response = requests.get(result_url)
            response_dict = response.json()

            # No books were found, and response wont contain 'items' key
            if not 'items' in response_dict.keys():
                return render(request, 'books/import_book_form.html', {'form': form})
            found_books = []

            for item in response_dict['items']:
                title = item['volumeInfo']['title']
                # Possible TODO: authors model have many to many relation with publications
                # TODO abide by DRY principle in code below
                try:
                    author = ", ".join(item['volumeInfo']['authors'])
                except KeyError:
                    author = None
                try:
                    publication_date = item['volumeInfo']['publishedDate']
                except KeyError:
                    publication_date = None
                try:
                    isbn = item['volumeInfo']['industryIdentifiers'][0]['identifier']
                except KeyError:
                    isbn = None
                try:
                    page_count = item['volumeInfo']['pageCount']
                except KeyError:
                    page_count = None
                try:
                    book_cover = item['volumeInfo']['imageLinks']['thumbnail']
                except KeyError:
                    book_cover = None
                try:
                    language = item['volumeInfo']['language']
                except KeyError:
                    language = None
                print("Found book:", title, author, publication_date, isbn, page_count, book_cover, language)
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

        # TODO przycisk dodaj wszystkie znalezione ksiazki

        context = {'form': form, 'found_books': found_books}
        return render(request, 'books/import_book_form.html', context)

    def append_to_url_query(self, form, key, query_string, q=False):
        """
        Appends key correctly to the query_string.
        :param form: Form object containing input data from user
        :param key: String, name of the field to be added to query string
        :param query_string: String, query string contains already created query string. Data will be appended to it
        :param q: Boolean informing whetever this is a first, mandatory parameter, or not.
        :return query_string_helper: string result containing created query string
        """
        keywords = str(form.cleaned_data[key]).strip().split()  # All keywords from single field in form of a list
        query_string_helper = query_string
        for index, keyword in enumerate(keywords):
            if not keyword or keyword == "None":
                continue
            match index:
                case 0:
                    if q:
                        query_string_helper = f'{query_string_helper}{keyword}'
                    else:
                        query_string_helper = f'{query_string_helper}+{key}:{keyword}'
                case _:
                    query_string_helper = f'{query_string_helper}+{keyword}'
        return query_string_helper


class ImportSingleBookView(View):
    def post(self, request, book_title, book_author, book_publication_date, book_isbn, book_page_count, book_cover,
             book_language):
        form = SearchForImportBookForm()
        print(book_title, book_author, book_publication_date, book_isbn,
              book_page_count, book_cover, book_language)

        if book_author:
            try:
                author = Author.objects.get(author=book_author)
            except Author.DoesNotExist:
                author = Author.objects.create(author=book_author)

        # TODO oczekiwana data to rok, miesiąc i dzień
        # TODO co robić jak otrzymana z api data ma tylko rok lub tylko rok i miesiąc?
        parsed = self.check_date_format(book_publication_date)
        date_correct_format, date_filter_format = parsed[0], parsed[1]
        print('aaaaaaaaaaaaaaa')
        print(date_correct_format, date_filter_format)
        print(book_publication_date)
        # TODO FILTROWANIE DATY/USTALENIE FORMATU DATY/ZAPISANIE TYPU DATY W MODELU

        Publication.objects.create(title=book_title,
                                   author=author,
                                   publication_date=date_correct_format,
                                   publication_date_type=date_filter_format,
                                   isbn=book_isbn,
                                   page_count=int(book_page_count) if type(book_page_count) is int else None,
                                   book_cover=book_cover,
                                   language=book_language)

        result_message = f"Zaimportowano książkę {book_title}."
        context = {'form': form, 'result_message': result_message}
        return render(request, 'books/import_book_form.html', context)

    def check_date_format(self, input_date):
        """
        Attempts to detect date format in one of few expected formats.
        If no format is correct, it returns None
        :param input_date: date in string format#TODO
        :return date: datetime.datetime object created from parsed input_date#TODO
        """

        possible_formats = {
            '%Y-%m-%d': 'd.m.Y',
            '%Y-%m': 'm.Y',
            '%Y': 'Y'
        }
        print("W FUNKCJI:")
        print(input_date)
        print(type(input_date))
        #time_string = datetime.strptime(input_date, '%Y-%m')


        for possible_format in possible_formats.keys():
            try:
                date = datetime.strptime(input_date, possible_format)
                print(f"PRZYDZIELONO DATE:{date}")
            except ValueError:
                pass
            else:
                print(f'WYKRYTY FORMAT DATY: {possible_format} CZYLI {possible_formats[possible_format]}')
                return [date, possible_formats[possible_format]]
        return None

