"""
test_django-teryt
------------

Tests for `django-teryt` modules utils.
"""

from django.test import TestCase
import requests_mock
from bs4 import BeautifulSoup

try:
    import unittest.mock as mock
except ImportError:
    import mock

from ..utils import get_xml_id_dictionary, HttpError, ParsingError

correct_dict = {'SIMC.xml': 1360, 'TERC.xml': 1358,
            'ULIC.xml': 1493, 'WMRODZ.xml': 941}

correct_html = """<html><body>
            <table class="list" id="row"><tbody>

            <tr><td>ULIC</td>
            <td><a href="downloadPreFile.jspa?id=1493"/>
            </td></tr>

            <tr><td>TERC</td>
            <td><a href="downloadPreFile.jspa?id=1358"/>
            </td></tr>

            <tr><td>SIMC</td>
            <td><a href="downloadPreFile.jspa?id=1360"/>
            </td></tr>

            <tr><td>WMRODZ</td>
            <td><a href="downloadPreFile.jspa?id=941"/>
            </td></tr>

            </tbody></table></body></html>
            """

gus_url = 'http://www.stat.gov.pl/broker/access/prefile/listPreFiles.jspa'


class TestUtils(TestCase):
    def test_parse_correct(self):
        with requests_mock.mock() as m:
            m.get(gus_url, text=correct_html)
            dictionary = get_xml_id_dictionary(gus_url)
            self.assertEqual(dictionary, correct_dict)

    def test_http_connection_error(self):
        with requests_mock.mock() as m:
            m.get(gus_url, text='Not found', status_code=404)
            self.assertRaises(HttpError, get_xml_id_dictionary)

    def test_incorrect_parse_wrong_url(self):
        self.assertRaises(ParsingError, get_xml_id_dictionary,
        'http://www.wp.pl')

    def test_incorrect_parse_initialize_parse_tree_fail(self):
        with mock.patch.object(BeautifulSoup, 'find',
        return_value=None) as mock_method:
            self.assertRaises(ParsingError, get_xml_id_dictionary)
            self.assertTrue(mock_method.called)
