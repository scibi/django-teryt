#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from collections import OrderedDict
from os import path
import zipfile

import requests

from django.core import management
from django.test import TransactionTestCase


class TestCommand(TransactionTestCase):
    tmp_dir = '/tmp/'
    files = OrderedDict([
        ('WMRODZ.xml', '941'),
        ('TERC.xml', '1110'),
        ('SIMC.xml', '1112'),
        ('ULIC.xml', '1246'),
    ])

    @staticmethod
    def _save_file(filename, url):
        filepath = path.join(TestCommand.tmp_dir, filename + ".zip")
        with open(filepath, 'wb') as handle:
            response = requests.get(url, stream=True)
            if response.ok:
                for block in response.iter_content(1024):
                    handle.write(block)
        with open(filepath) as handle:
            myzipfile = zipfile.ZipFile(handle)
            myzipfile.extract(filename, TestCommand.tmp_dir)

    def setUp(self):
        # _, tmp_dir = mkstemp()
        url_tmpl = 'http://www.stat.gov.pl/broker/access/prefile/'\
                   'downloadPreFile.jspa?id={}'
        for filename, file_id in self.files.items():
            TestCommand._save_file(filename, url_tmpl.format(file_id))

    def test_command(self):
        for filename in self.files.keys():
            # print("running teryt_parse {}".format(filename))
            management.call_command('teryt_parse', path.join(self.tmp_dir,
                                                             filename))
