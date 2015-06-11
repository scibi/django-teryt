#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

"""
test_django-teryt
------------

Tests for `django-teryt` modules module.
"""
import unittest

from ..models import RodzajMiejscowosci
from .factories import RodzajMiejscowosciFactory


class TestRodzajMiejscowosci(unittest.TestCase):

    def test_str(self):
        rm = RodzajMiejscowosciFactory(id='96', nazwa='miasto')
        self.assertEqual(str(rm), '96: miasto')

    def test_set_val(self):
        rm = RodzajMiejscowosci()
        rm.set_val({'RM': '01',
                    'STAN_NA': '2013-02-28',
                    'NAZWA_RM': 'wieś'})
        self.assertEqual(rm.nazwa, 'wieś')
        self.assertEqual(rm.id, '01')
        self.assertEqual(rm.stan_na, '2013-02-28')
