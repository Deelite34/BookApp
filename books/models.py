from django.db import models


class Author(models.Model):
    """
    Information on original book. Due to task requirements of this project, there
    is no need to include in this model all information it should contain otherwise.
    In result, model is small in size.
    """
    author = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.author}"


class Publication(models.Model):
    """
    Information about books specific publication.
    """
    title = models.CharField(max_length=500)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    isbn = models.PositiveBigIntegerField()
    page_count = models.PositiveIntegerField()
    book_cover = models.URLField(max_length=500)
    language = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"
