from datetime import datetime

from books.utils import check_date_format, append_to_url_query
from django.test import TestCase


class UtilsTest(TestCase):
    def test_check_date_format(self):
        date_1 = '2020-12-04'
        date_2 = '1996-12'
        date_3 = '2022'
        date_4 = '123456'
        date_1_format = '%Y-%m-%d'
        date_2_format = '%Y-%m'
        date_3_format = '%Y'

        result_1 = check_date_format(date_1)
        result_2 = check_date_format(date_2)
        result_3 = check_date_format(date_3)
        result_4 = check_date_format(date_4)
        expected_date_1 = datetime.strptime(date_1, date_1_format)
        expected_date_2 = datetime.strptime(date_2, date_2_format)
        expected_date_3 = datetime.strptime(date_3, date_3_format)
        expected_string_1 = 'd.m.Y'
        expected_string_2 = 'm.Y'
        expected_string_3 = 'Y'

        self.assertEqual(result_1[0], expected_date_1)
        self.assertEqual(result_2[0], expected_date_2)
        self.assertEqual(result_3[0], expected_date_3)
        self.assertEqual(result_1[1], expected_string_1)
        self.assertEqual(result_2[1], expected_string_2)
        self.assertEqual(result_3[1], expected_string_3)
        self.assertIsNone(result_4)

    def test_append_to_url_query(self):
        input_dict_1 = {
            'q': 'Harry Potter',
            'intitle': '',
            'inauthor': '',
            'inpublisher': '',
            'subject': '',
            'isbn': '',
            'lccn': '',
            'aclc': '',
        }
        input_dict_2 = {
            'q': 'Harry Potter',
            'intitle': 'Harry Potter',
            'inauthor': 'Rowling',
            'inpublisher': 'a',
            'subject': 'magic fantasy',
            'isbn': '1',
            'lccn': '23',
            'aclc': '345',
        }
        base_url_query = '?q='
        expected_result_1 = "?q=Harry+Potter"
        expected_result_2 = "?q=Harry+Potter+intitle:Harry+Potter+inauthor" \
                            ":Rowling+inpublisher:a+subject:magic" \
                            "+fantasy+isbn:1+lccn:23+aclc:345"
        fields_to_add = list(input_dict_2.keys())[1:]

        result_1 = append_to_url_query(input_dict_1, 'q', base_url_query, True,
                                       True)
        result_2 = result_1[:]  # Copy of result_1 string
        for field in fields_to_add:
            result_2 = append_to_url_query(input_dict_2, field, result_2,
                                           test=True)

        self.assertEqual(result_1, expected_result_1)
        self.assertEqual(result_2, expected_result_2)
