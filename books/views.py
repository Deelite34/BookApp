from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from .forms import form_date_errors, PublicationSearchForm, AuthorForm, PublicationForm
from .models import Publication


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
