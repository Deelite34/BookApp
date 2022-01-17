import json

from books.models import Author, Publication
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

BOOK_COVER = 'http://asdf.com'
NAME = 'Bobby'
TITLE = 'testtitle'
PUBLICATION_DATE = '2012-02-01'
PUBLICATION_DATE_TYPE = 'd.m.Y'
DATE_FORMATTED = PUBLICATION_DATE.split('-')
DATE_FORMATTED.reverse()
DATE_FORMATTED = '.'.join(DATE_FORMATTED)
ISBN = '1234'
PAGE_COUNT = '12'
LANGUAGE = 'en'
VISIBLE_PUBLICATION_PARAMS = (
NAME, TITLE, ISBN, PAGE_COUNT, BOOK_COVER, LANGUAGE)
CLIENT = APIClient()
NAME_ALT = "Johnny"
TITLE_ALT = 'whatevertitle'
PUBLICATION_DATE_ALT = '2020-01-04'
ISBN_ALT = '6789'
PAGE_COUNT_ALT = 321
LANGUAGE_ALT = 'en'
NAME_THIRD = "Lenny"
FIELDS = (
'id', 'title', 'url', 'author', 'publication_date', 'publication_date_type',
'isbn', 'page_count',
'book_cover', 'language')


def create_initial_data():
    """
    Creates author with 2 assigned books, and  and returns list
    with [author_1, publication_1, publication_2, author_2]
    """
    author_1 = Author.objects.create(author=NAME)

    pub_1 = Publication.objects.create(title=TITLE, author=author_1,
                                       publication_date=PUBLICATION_DATE,
                                       publication_date_type=PUBLICATION_DATE_TYPE,
                                       isbn=ISBN, page_count=PAGE_COUNT,
                                       book_cover=BOOK_COVER,
                                       language=LANGUAGE)

    pub_2 = Publication.objects.create(title=TITLE_ALT, author=author_1,
                                       publication_date=PUBLICATION_DATE_ALT,
                                       publication_date_type=PUBLICATION_DATE_TYPE,
                                       isbn=ISBN_ALT,
                                       page_count=PAGE_COUNT_ALT,
                                       book_cover=BOOK_COVER,
                                       language=LANGUAGE_ALT)

    author_2 = Author.objects.create(author=NAME_ALT)

    return [author_1, pub_1, pub_2, author_2]


class ApiAuthorEndpointTest(TestCase):
    def test_author_api_list(self):
        create_initial_data()
        list_endpoint = reverse('author-list')

        response = CLIENT.get(list_endpoint)
        response_dict = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_dict), 2)
        self.assertIn('id', response_dict[0].keys())
        self.assertIn('author', response_dict[0].keys())
        self.assertEquals(NAME, response_dict[0]['author'])
        self.assertEquals(NAME_ALT, response_dict[1]['author'])

    def test_author_api_retrieve(self):
        initial_data = create_initial_data()
        detail_endpoint = reverse('author-detail', args=(initial_data[0].id,))

        response = CLIENT.get(detail_endpoint)
        response_dict = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response_dict.keys())
        self.assertIn('author', response_dict.keys())
        self.assertEquals(NAME, response_dict['author'])

    def test_author_api_create(self):
        list_endpoint = reverse('author-list')
        data = {
            'author': NAME
        }

        response = CLIENT.post(list_endpoint, data)
        response_dict = json.loads(response.content)
        author_exists = Author.objects.filter(author=NAME).exists()

        self.assertEquals(response.status_code, 201)
        self.assertIn('id', response_dict.keys())
        self.assertIn('author', response_dict.keys())
        self.assertEquals(NAME, response_dict['author'])
        self.assertTrue(author_exists)

    def test_author_api_put(self):
        initial_data = create_initial_data()
        detail_endpoint = reverse('author-detail', args=(initial_data[0].id,))
        data = {
            'author': NAME_THIRD
        }

        response = CLIENT.put(detail_endpoint, data)
        response_dict = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertIn('id', response_dict.keys())
        self.assertIn('author', response_dict.keys())
        self.assertEquals(NAME_THIRD, response_dict['author'])

    def test_author_api_delete(self):
        initial_data = create_initial_data()
        detail_endpoint = reverse('author-detail', args=(initial_data[0].id,))

        response = CLIENT.delete(detail_endpoint)
        found_authors = Author.objects.filter(author=NAME)

        self.assertEquals(response.status_code, 204)
        self.assertEquals(response.content, b'')
        self.assertFalse(found_authors.exists())


class ApiPublicationEndpointTest(TestCase):
    def test_publication_api_list(self):
        create_initial_data()
        list_endpoint = reverse('publication-list')

        response = CLIENT.get(list_endpoint)
        response_dict = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response_dict), 2)
        self.assertEquals(len(response_dict[0].keys()), 10)
        self.assertTrue(
            all(field in response_dict[0].keys() for field in FIELDS))

    def test_publication_api_retrieve(self):
        initial_data = create_initial_data()
        detail_endpoint = reverse('publication-detail',
                                  args=(initial_data[1].id,))

        response = CLIENT.get(detail_endpoint)
        response_dict = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response_dict.keys()), 10)
        self.assertTrue(all(field in response_dict.keys() for field in FIELDS))

    def test_publication_api_create(self):
        list_endpoint = reverse('publication-list')
        author = Author.objects.create(author=NAME)
        data = {
            'title': TITLE,
            'author': author.id,
            'publication_date': PUBLICATION_DATE,
            'publication_date_type': PUBLICATION_DATE_TYPE,
            'isbn': ISBN,
            'page_count': PAGE_COUNT,
            'book_cover': BOOK_COVER,
            'language': LANGUAGE
        }

        response = CLIENT.post(list_endpoint, data)
        response_dict = json.loads(response.content)
        publication_exists = Publication.objects.filter(title=TITLE,
                                                        language=LANGUAGE).exists()

        self.assertEquals(response.status_code, 201)
        self.assertTrue(all(field in response_dict.keys() for field in FIELDS))
        self.assertTrue(publication_exists)

    def test_publication_api_put(self):
        initial_data = create_initial_data()
        detail_endpoint = reverse('publication-detail',
                                  args=(initial_data[1].id,))
        data = {
            'title': TITLE_ALT,
            'author': initial_data[0].id,
            'publication_date': PUBLICATION_DATE,
            'publication_date_type': PUBLICATION_DATE_TYPE,
            'isbn': ISBN_ALT,
            'page_count': PAGE_COUNT,
            'book_cover': BOOK_COVER,
            'language': LANGUAGE
        }

        response = CLIENT.put(detail_endpoint, data)
        response_dict = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(TITLE_ALT, response_dict['title'])
        self.assertEquals(ISBN_ALT, response_dict['isbn'])
        self.assertEquals(BOOK_COVER, response_dict['book_cover'])
        self.assertTrue(all(field in response_dict.keys() for field in FIELDS))

    def test_publication_api_delete(self):
        initial_data = create_initial_data()
        detail_endpoint = reverse('publication-detail',
                                  args=(initial_data[1].id,))

        response = CLIENT.delete(detail_endpoint)
        found_publications = Publication.objects.filter(title=TITLE,
                                                        language=LANGUAGE,
                                                        author=initial_data[
                                                            0].id)

        self.assertEquals(response.status_code, 204)
        self.assertEquals(response.content, b'')
        self.assertFalse(found_publications.exists())


class ApiFilterEndpointTest(TestCase):
    def test_author_filter_api_filtering(self):
        initial_data = create_initial_data()
        endpoint_1 = reverse('filter-authors-list')
        endpoint_1 = f'{endpoint_1}?author={initial_data[0].author}'
        endpoint_2 = reverse('filter-authors-list')
        endpoint_2 = f'{endpoint_2}?id={initial_data[3].id}'

        response_1 = CLIENT.get(endpoint_1)
        response_2 = CLIENT.get(endpoint_2)
        response_dict_1 = json.loads(response_1.content)
        response_dict_2 = json.loads(response_2.content)

        self.assertEquals(response_dict_1[0]['author'], NAME)
        self.assertEquals(len(response_dict_1), 1)
        self.assertEquals(response_dict_2[0]['author'], NAME_ALT)
        self.assertEquals(len(response_dict_2), 1)

    def test_publication_filter_api_filtering(self):
        create_initial_data()
        endpoint_1 = reverse('filter-publications-list')
        endpoint_1 = f'{endpoint_1}?publication_after={PUBLICATION_DATE_ALT}'
        endpoint_2 = reverse('filter-publications-list')
        endpoint_2 = f'{endpoint_2}?title={TITLE}&publication_date=' \
                     f'{PUBLICATION_DATE}'

        response_1 = CLIENT.get(endpoint_1)
        response_2 = CLIENT.get(endpoint_2)
        response_dict_1 = json.loads(response_1.content)
        response_dict_2 = json.loads(response_2.content)

        self.assertEquals(response_dict_1[0]['publication_date'],
                          PUBLICATION_DATE_ALT)
        self.assertEquals(len(response_dict_1), 1)
        self.assertEquals(response_dict_2[0]['title'], TITLE)
        self.assertEquals(len(response_dict_2), 1)


class ApiSearchEndpointTest(TestCase):
    def test_author_search_api_searching(self):
        initial_data = create_initial_data()
        endpoint_1 = reverse('search-authors-list')
        endpoint_1 = f'{endpoint_1}?search={initial_data[0].id}'
        endpoint_2 = reverse('search-authors-list')
        endpoint_2 = f'{endpoint_2}?search={initial_data[3].author}'

        response_1 = CLIENT.get(endpoint_1)
        response_2 = CLIENT.get(endpoint_2)
        response_dict_1 = json.loads(response_1.content)
        response_dict_2 = json.loads(response_2.content)

        self.assertEquals(response_dict_1[0]['author'], NAME)
        self.assertEquals(len(response_dict_1), 1)
        self.assertEquals(response_dict_2[0]['author'], NAME_ALT)
        self.assertEquals(len(response_dict_2), 1)

    def test_publication_filter_api_filtering(self):
        create_initial_data()
        endpoint_1 = reverse('search-publications-list')
        endpoint_1 = f'{endpoint_1}?search={PAGE_COUNT}'
        endpoint_2 = reverse('search-publications-list')
        endpoint_2 = f'{endpoint_2}?search={TITLE_ALT}'

        response_1 = CLIENT.get(endpoint_1)
        response_2 = CLIENT.get(endpoint_2)
        response_dict_1 = json.loads(response_1.content)
        response_dict_2 = json.loads(response_2.content)

        self.assertEquals(response_dict_1[0]['title'], TITLE)
        self.assertEquals(len(response_dict_1), 1)
        self.assertEquals(response_dict_2[0]['title'], TITLE_ALT)
        self.assertEquals(len(response_dict_2), 1)
