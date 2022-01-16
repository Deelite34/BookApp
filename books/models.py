from django.core.validators import MaxValueValidator
from django.db import models

from .validators import validate_publication_date


class Author(models.Model):
    """
    Information on original book. Due to task requirements of this project,
    there
    is no need to include in this model all information it should contain
    otherwise.
    In result, model is small in size.
    """
    author = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author}"


class Publication(models.Model):
    """
    Information about books specific publication.
    """
    DATE_TYPES = [
        ('Y', 'Tylko rok'),
        ('m.Y', 'Miesiąc i rok '),
        ('d.m.Y', 'Dzień, miesiąc, rok'),
    ]

    title = models.CharField(max_length=500)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True,
                               blank=True)
    publication_date = models.DateField(null=True, blank=True,
                                        validators=[validate_publication_date])
    publication_date_type = models.CharField(choices=DATE_TYPES, max_length=50)
    isbn = models.CharField(null=True, blank=True, max_length=20)
    page_count = models.PositiveIntegerField(null=True, blank=True,
                                             validators=[
                                                 MaxValueValidator(50000)])
    book_cover = models.URLField(max_length=500, null=True, blank=True)
    language = models.CharField(max_length=10, null=True,
                                blank=True)  # Short code ISO-639-1

    def __str__(self):
        return f"{self.title}"
