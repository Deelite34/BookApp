from books.models import Author, Publication
from django.test import TestCase


class ModelsTest(TestCase):
    def test_author_str_method(self):
        name = 'John'

        author = Author.objects.create(author=name)

        self.assertEqual(str(author), name)

    def test_publication_str_method(self):
        title = 'publication_title'

        publication = Publication.objects.create(title=title)

        self.assertEqual(str(publication), title)
