#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from collections import OrderedDict
from os import path
import tempfile
import zipfile
import io

import requests

from django.core import management
from django.test import TestCase


class TestParseCommand(TestCase):
    url_tmpl = 'http://www.stat.gov.pl/broker/access/prefile/'\
               'downloadPreFile.jspa?id={}'

    files = OrderedDict([
        ('WMRODZ.xml', '941'),
        ('TERC.xml', '1110'),
        ('SIMC.xml', '1112'),
        ('ULIC.xml', '1246'),
    ])

    def _save_file(self, filename, url):
        request = requests.get(url)
        zfile = zipfile.ZipFile(io.BytesIO(request.content))
        zfile.extract(filename, self.tempdir)

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        for filename, file_id in self.files.items():
            self._save_file(filename, self.url_tmpl.format(file_id))

    def test_command(self):
        for filename in self.files.keys():
            # print("running teryt_parse {}".format(filename))
            management.call_command('teryt_parse', path.join(self.tempdir,
                                                             filename))
