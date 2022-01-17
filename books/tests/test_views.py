from datetime import datetime

from books.models import Author, Publication
from django.test import Client, TestCase
from django.urls import reverse

# constants shared by all tests
BOOK_COVER = 'http://asdf.com'
SEARCH_FORM_FIELDS = ("Tytuł", 'Autor', 'Język', 'Opublikowana od',
                      'Opublikowana do')
NAME = 'Bobby'
NAME_ALT = "Johnny"
TITLE = 'testtitle'
TITLE_ALT = 'whatevertitle'
PUBLICATION_DATE = '2012-02-01'
PUBLICATION_DATE_ALT = '2020-01-04'
PUBLICATION_DATE_TYPE = 'd.m.Y'
DATE_FORMATTED = PUBLICATION_DATE.split('-')
DATE_FORMATTED.reverse()
DATE_FORMATTED = '.'.join(DATE_FORMATTED)
ISBN = '1234'
ISBN_ALT = '6789'
PAGE_COUNT = '12'
PAGE_COUNT_ALT = 321
LANGUAGE = 'en'
LANGUAGE_ALT = 'en'
VISIBLE_PUBLICATION_PARAMS = (NAME, TITLE, ISBN, PAGE_COUNT,
                              BOOK_COVER, LANGUAGE)
CLIENT = Client()


class IndexViewTest(TestCase):
    url = reverse('index')

    def test_get_index_page(self):
        author = Author.objects.create(author=NAME)
        Publication.objects.create(title=TITLE, author=author,
                                   publication_date=PUBLICATION_DATE,
                                   publication_date_type=PUBLICATION_DATE_TYPE,
                                   isbn=ISBN, page_count=PAGE_COUNT,
                                   book_cover=BOOK_COVER)

        response = CLIENT.get(self.url)
        response_content = response.content.decode("UTF-8")

        self.assertEqual(response.status_code, 200)
        # Displaying labels for search form fields in the template
        for arg in SEARCH_FORM_FIELDS:
            self.assertIn(arg, response_content)
        # Displaying created publications
        for param in VISIBLE_PUBLICATION_PARAMS:
            self.assertIn(param, response_content)

    def test_post_index_page(self):
        """
        Post request in index page is used for searching database
        for publications using specified parameters
        """
        author = Author.objects.create(author=NAME)
        Publication.objects.create(title=TITLE, author=author,
                                   publication_date=PUBLICATION_DATE,
                                   publication_date_type=PUBLICATION_DATE_TYPE,
                                   isbn=ISBN, page_count=PAGE_COUNT,
                                   book_cover=BOOK_COVER)
        Publication.objects.create(title=TITLE_ALT, author=author,
                                   publication_date=PUBLICATION_DATE,
                                   publication_date_type=PUBLICATION_DATE_TYPE,
                                   isbn=ISBN, page_count=PAGE_COUNT,
                                   book_cover=BOOK_COVER)
        request_data_1 = {
            # Searching 'obbi' should allow us to find 'Hobbit'
            'title': TITLE[1:-2],
            'author': NAME[1:-2],
            'language': '',
            'published_from': '01.01.2000',
            'published_to': '01.01.2020'
        }
        request_data_2 = dict(request_data_1)
        request_data_2['title'] = 'qweqweqwe'
        request_data_3 = dict(request_data_1)
        request_data_3['author'] = 'qweqweqwe'
        request_data_4 = dict(request_data_1)
        request_data_4['published_from'] = '01.01.2019'
        request_data_5 = dict(request_data_1)
        request_data_5['published_to'] = '01.01.2001'

        response_1 = CLIENT.post(self.url, data=request_data_1)
        response_content_1 = response_1.content.decode("UTF-8")
        response_2 = CLIENT.post(self.url, data=request_data_2)
        response_content_2 = response_2.content.decode("UTF-8")
        response_3 = CLIENT.post(self.url, data=request_data_2)
        response_content_3 = response_3.content.decode("UTF-8")
        response_4 = CLIENT.post(self.url, data=request_data_2)
        response_content_4 = response_4.content.decode("UTF-8")
        response_5 = CLIENT.post(self.url, data=request_data_2)
        response_content_5 = response_5.content.decode("UTF-8")

        self.assertEqual(response_1.status_code, 200)
        # If one form field is visible, all should be too
        self.assertIn("Opublikowana od", response_content_1)
        self.assertIn(TITLE, response_content_1)
        self.assertIn(NAME, response_content_1)
        # found book param 'None' is displayed as understandable text
        self.assertIn('Brak danych', response_content_1)
        self.assertIn(DATE_FORMATTED, response_content_1)
        self.assertIn('Edytuj', response_content_1)  # Edit button is visible
        self.assertIn('Usuń', response_content_1)  # Delete button is visible
        self.assertNotIn(TITLE, response_content_2)
        self.assertNotIn(TITLE, response_content_3)
        self.assertNotIn(TITLE, response_content_4)
        self.assertNotIn(TITLE, response_content_5)


class AddViewTest(TestCase):
    url = reverse('add')

    def test_get_add_page(self):
        response = CLIENT.get(self.url)
        response_content = response.content.decode("UTF-8")

        self.assertEqual(response.status_code, 200)
        # If both forms author label appears, then all field should be visible
        self.assertEqual(response_content.count('Autor'), 2)

    def test_post_add_page(self):
        add_author_form_data = {
            'csrftoken': 'doesntmater',
            'author': NAME
        }
        author = Author.objects.create(author=NAME_ALT)
        add_publication_form_data = {
            'title': TITLE,
            'author': author.id,
            'publication_date': PUBLICATION_DATE,
            'publication_date_type': PUBLICATION_DATE_TYPE,
            'isbn': ISBN,
            'page_count': PAGE_COUNT,
            'book_cover': BOOK_COVER,
            'language': LANGUAGE,
        }
        success_msg = 'Operacja zakończona sukcesem'

        response_post_author = CLIENT.post(self.url, add_author_form_data)
        author_exists = Author.objects.filter(author=NAME).exists()
        response_post_author_content = response_post_author.content \
            .decode("UTF-8")
        response_post_publication = CLIENT.post(self.url,
                                                add_publication_form_data)
        response_post_publication_content = \
            response_post_publication.content.decode(
                "UTF-8")
        publication_exists = Publication.objects.filter(title=TITLE,
                                                        author=author)

        self.assertEqual(response_post_author.status_code, 200)
        self.assertTrue(author_exists)
        self.assertIn(success_msg, response_post_author_content)
        self.assertEqual(response_post_publication.status_code, 200)
        self.assertTrue(publication_exists)
        self.assertIn(success_msg, response_post_publication_content)


class ImportViewTest(TestCase):
    url = reverse('import')

    def test_get_import_page(self):
        response = CLIENT.get(self.url)
        response_content = response.content.decode("UTF-8")

        self.assertEqual(response.status_code, 200)
        # If one form label appears, then all field should be visible
        self.assertIn("Słowa kluczowe:", response_content)

    def test_post_import_page(self):
        search_import_items_data = {
            'q': 'Harry Potter',
            'intitle': 'Harry',
            'inauthor': 'Rowling',
            'inpublisher': '',
            'subject': 'magic',
            'isbn': '',
            'lccn': '',
            'aclc': '',
        }

        response_post = CLIENT.post(self.url, search_import_items_data)
        response_post_content = response_post.content.decode("UTF-8")

        self.assertEqual(response_post.status_code, 200)
        self.assertIn('Harry Potter i kamien filozoficzny',
                      response_post_content)
        self.assertIn('Harry Potter i Zakon Feniksa 5', response_post_content)
        self.assertIn('Brak danych', response_post_content)
        self.assertIn("Dodaj", response_post_content)


class ImportSingleBookView(TestCase):
    url = reverse('import_book')

    def test_import_single_book(self):
        url_query_strings = "/import-book?book_title=Hobbit czyli Tam i z " \
                            "powrotem&book_author=John Ronald Reuel " \
                            "Tolkien&publication_date=1985&book_isbn=IND" \
                            ":39000004593617&page_count=233&book_cover" \
                            "=http://books" \
                            ".google.com/books/content?id=DqLPAAAAMAAJ" \
                            "&printsec=" \
                            "frontcover&img=1&zoom=1&source=gbs_api" \
                            "&book_language=pl"
        title = 'Hobbit czyli Tam i z powrotem'
        author = 'John Ronald Reuel Tolkien'
        publication_date = '1985-01-01'
        isbn = 'IND:39000004593617'
        page_count = '233'
        book_cover = 'http://books.google.com/books/content?id=DqLPAAAAMAAJ' \
                     '&printsec=frontcover&img=1&zoom=1&source=gbs_api'
        language = 'pl'

        response_post = CLIENT.post(url_query_strings, {})
        response_post_content = response_post.content.decode("UTF-8")
        author_obj = Author.objects.get(author=author)
        publication_exists = Publication.objects.filter(title=title,
                                                        author=author_obj,
                                                        publication_date=publication_date,
                                                        isbn=isbn,
                                                        page_count=page_count,
                                                        book_cover=book_cover,
                                                        language=language)

        self.assertEqual(response_post.status_code, 200)
        self.assertTrue(publication_exists)
        self.assertIn(f'Zaimportowano książkę {title}', response_post_content)


class EditBookView(TestCase):
    book_cover_alt = "http://asdf.com"
    datetime_obj_alt = datetime.strptime(PUBLICATION_DATE_ALT,
                                         '%Y-%m-%d').date()

    def test_get_edit_page(self):
        publication = Publication.objects.create(title=TITLE,
                                                 language=LANGUAGE,
                                                 publication_date=PUBLICATION_DATE,
                                                 publication_date_type=PUBLICATION_DATE_TYPE)
        url = reverse('edit', args=(publication.id,))

        response = CLIENT.get(url)
        response_content = response.content.decode("UTF-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn('Tytuł:', response_content)
        self.assertIn(TITLE, response_content)
        self.assertIn(LANGUAGE, response_content)

    def test_post_edit_page(self):
        author = Author.objects.create(author=NAME)
        author_alt = Author.objects.create(author=NAME_ALT)
        edit_item_data = {
            'title': TITLE_ALT,
            'author': author_alt.id,
            'publication_date': PUBLICATION_DATE_ALT,
            'publication_date_type': PUBLICATION_DATE_TYPE,
            'isbn': ISBN_ALT,
            'page_count': PAGE_COUNT_ALT,
            'book_cover': self.book_cover_alt,
            'language': LANGUAGE_ALT
        }
        publication = Publication.objects.create(title=TITLE, author=author,
                                                 language=LANGUAGE,
                                                 publication_date=PUBLICATION_DATE,
                                                 publication_date_type=PUBLICATION_DATE_TYPE,
                                                 isbn=ISBN)
        success_msg = "Publikacja pomyślnie zmodyfikowana."
        url = reverse('edit', args=(publication.id,))

        response_post = CLIENT.post(url, edit_item_data)
        response_post_content = response_post.content.decode("UTF-8")
        publication = Publication.objects.get(title=TITLE_ALT,
                                              author=author_alt,
                                              language=LANGUAGE_ALT,
                                              publication_date=PUBLICATION_DATE_ALT,
                                              publication_date_type=PUBLICATION_DATE_TYPE,
                                              isbn=ISBN_ALT)

        # Ensure all fields submited by form have been modified
        self.assertEqual(response_post.status_code, 200)
        self.assertIn(success_msg, response_post_content)
        self.assertIn(LANGUAGE_ALT, response_post_content)
        self.assertEqual(publication.language, LANGUAGE_ALT)
        self.assertEqual(publication.publication_date, self.datetime_obj_alt)
        self.assertEqual(publication.isbn, ISBN_ALT)
        self.assertEqual(publication.book_cover, self.book_cover_alt)
        self.assertEqual(publication.page_count, PAGE_COUNT_ALT)
        self.assertEqual(publication.author.author, NAME_ALT)


class DeleteBookView(TestCase):
    def test_post_delete_book(self):
        author = Author.objects.create(author=NAME)
        publication = Publication.objects.create(title=TITLE, author=author,
                                                 language=LANGUAGE,
                                                 publication_date=PUBLICATION_DATE,
                                                 publication_date_type=PUBLICATION_DATE_TYPE,
                                                 isbn=ISBN)
        url = reverse('delete', args=(publication.id,))

        response_post = CLIENT.post(url, {})
        response_post_content = response_post.content.decode("UTF-8")

        # Deleted item wont appear anywehere
        self.assertEqual(response_post.status_code, 302)
        self.assertNotIn(TITLE, response_post_content)
