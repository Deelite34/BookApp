from django import forms

from .models import Author, Publication

form_date_errors = {'invalid': 'Podaj datę w formacie dzień.miesiąc.rok'}


class PublicationSearchForm(forms.Form):
    title = forms.CharField(label="Tytuł", required=False, max_length=500,
                            widget=forms.TextInput(attrs={'class': 'search-form-title'}))
    author = forms.CharField(label="Autor", required=False, max_length=100,
                             widget=forms.TextInput(attrs={'class': 'search-form-author'}))
    language = forms.CharField(label="Język", required=False, max_length=100,
                               widget=forms.TextInput(attrs={'class': 'search-form-language'}))
    published_from = forms.DateField(label="Opublikowana od",
                                     error_messages=form_date_errors, required=False,
                                     widget=forms.DateInput(attrs={'class': 'search-form-published-from'}))
    published_to = forms.DateField(label="Opublikowana do",
                                   error_messages=form_date_errors, required=False,
                                   widget=forms.DateInput(attrs={'class': 'search-form-published-to'}))


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['author']


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'author', 'publication_date', 'isbn', 'page_count', 'book_cover', 'language']

