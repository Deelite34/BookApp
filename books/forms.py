from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Author, Publication

form_date_errors = {'invalid': 'Podaj datę w formacie dzień.miesiąc.rok'}


class PublicationSearchForm(forms.Form):
    title = forms.CharField(label="Tytuł", required=False, max_length=500,
                            widget=forms.TextInput(attrs={'class': 'search-form-title'}))
    author = forms.CharField(label="Autor", required=False, max_length=200,
                             widget=forms.TextInput(attrs={'class': 'search-form-author'}))
    language = forms.CharField(label="Język", required=False, max_length=10,
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
        labels = {
            'author': _('Autor'),
        }


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'author', 'publication_date', 'publication_date_type',
                  'isbn', 'page_count', 'book_cover', 'language']
        labels = {
            'title': _('Tytuł'),
            'author': _('Autor'),
            'publication_date': _('Data publikacji'),
            'publication_date_type': _('Format daty'),
            'isbn': _('Nr. ISBN'),
            'page_count': _('Ilość stron'),
            'book_cover': _('Link do okładki'),
            'language': _('Kod języka'),
        }

    def __init__(self, *args, **kwargs):
        super(PublicationForm, self).__init__(*args, **kwargs)
        self.fields['author'].required = True
        self.fields['publication_date'].required = True
        self.fields['isbn'].required = True
        self.fields['language'].required = True


class SearchForImportBookForm(forms.Form):
    q = forms.CharField(label="Słowa kluczowe", required=True, max_length=500,
                        widget=forms.TextInput(attrs={'class': 'search-form-title'}))
    intitle = forms.CharField(label="Tytuł", required=False, max_length=500,
                              widget=forms.TextInput(attrs={'class': 'search-form-title'}))
    inauthor = forms.CharField(label="Autor", required=False, max_length=100,
                               widget=forms.TextInput(attrs={'class': 'search-form-author'}))
    inpublisher = forms.CharField(label="Wydawca", required=False, max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'search-form-author'}))
    subject = forms.CharField(label="Tematyka", required=False, max_length=100,
                              widget=forms.TextInput(attrs={'class': 'search-form-author'}))
    isbn = forms.IntegerField(label="Numer ISBN", required=False,
                              widget=forms.TextInput(attrs={'class': 'search-form-author'}))
    lccn = forms.IntegerField(label="Numer LCCN", required=False,
                              widget=forms.TextInput(attrs={'class': 'search-form-author'}))
    aclc = forms.IntegerField(label="Numer ACLC", required=False,
                              widget=forms.TextInput(attrs={'class': 'search-form-author'}))
