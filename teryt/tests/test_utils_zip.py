"""
test_django-teryt
------------

Tests for `django-teryt` module utils_zip.
"""
import io
import zipfile
try:
    import unittest.mock as mock
except ImportError:
    import mock

from django.test import TestCase
from django.core.management.base import CommandError
from django.db import DatabaseError

import requests
import requests_mock

from ..utils_zip import (open_zipfile_from_url, get_zip_files,
                        update_database)

correct_file_url = {'WMRODZ.xml': 'http://www.stat.gov.pl/broker/access/'
                'prefile/downloadPreFile.jspa?id=941'}

correct_ordered_xml_files_list = ['WMRODZ.xml', 'TERC.xml',
                                'SIMC.xml', 'ULIC.xml']


class TestUtilsZipFunctions(TestCase):
    def setUp(self):
        request = requests.get(correct_file_url['WMRODZ.xml'],
                                stream=True)
        zip = zipfile.ZipFile(io.BytesIO(request.content))
        self.correct_xml_stream = zip.open('WMRODZ.xml')

    def test_open_zip_from_url_correct(self):
        try:
            zfile = open_zipfile_from_url('WMRODZ.xml',
                                        correct_file_url['WMRODZ.xml'])
        except (zipfile.BadZipFile, zipfile.BadZipfile):
            self.fail("BadZipFile exception raised unexpectedly!")

        # .testzip() returns name of first bad file in the archive,
        # otherwise it returns None
        self.assertEqual(zfile.testzip(), None)
        self.assertEqual(zfile.namelist()[0], 'WMRODZ.xml')

    def test_open_zip_from_url_bad_zip(self):
        with requests_mock.mock() as m:
            m.get(correct_file_url['WMRODZ.xml'], text='')
            self.assertRaises(
                (zipfile.BadZipFile, zipfile.BadZipfile),
                open_zipfile_from_url,
                'WMRODZ.xml',
                correct_file_url['WMRODZ.xml']
            )

    def test_open_zip_from_url_bad_url(self):
        self.assertRaises(
            (zipfile.BadZipFile, zipfile.BadZipfile),
            open_zipfile_from_url,
            'WMRODZ.xml',
            'http://www.wp.pl'
        )

    def test_get_zip_files_correct(self):
        try:
            zip_files = get_zip_files()
        except (zipfile.BadZipFile, zipfile.BadZipfile):
            self.fail("BadZipFile exception raised unexpectedly!")

        for zfile in zip_files:
            self.assertEqual(zfile.testzip(), None)
        xml_list = [zfile.namelist()[0] for zfile in zip_files]
        self.assertEqual(xml_list, correct_ordered_xml_files_list)

    @mock.patch('teryt.utils_zip.get_xml_id_dictionary',
                return_value=None)
    def test_get_zip_files_dictionary_fail(self, mock_method):
        self.assertRaises(TypeError, get_zip_files)
        self.assertTrue(mock_method.called)

    @mock.patch('teryt.utils_zip.get_xml_id_dictionary',
                return_value={'Incorrect': 'dictionary'})
    def test_get_zip_files_dictionary_incorrect(self, mock_method):
        self.assertRaises(KeyError, get_zip_files)
        self.assertTrue(mock_method.called)
    
    def test_update_database_correct(self):
        try:
            update_database(self.correct_xml_stream,
                            'WMRODZ.xml', False)
        except CommandError:
            self.fail("CommandError exception raised unexpectedly!")

    def test_update_database_incorrect_stream(self):
        self.assertRaises(CommandError, update_database,
                    None, 'WMRODZ.xml', False)

    def test_update_database_unknown_filename(self):
        self.assertRaises(CommandError, update_database,
                    self.correct_xml_stream, 'Unknown.xml', False)

    @mock.patch('django.db.models.Model.save', side_effect=DatabaseError())
    def test_update_database_database_error(self, mock_method):
        self.assertRaises(CommandError, update_database,
                    self.correct_xml_stream, 'WMRODZ.xml', False)
        self.assertTrue(mock_method.called)
