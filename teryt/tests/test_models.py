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

from ..models import RodzajMiejscowosci, JednostkaAdministracyjna
from .factories import (RodzajMiejscowosciFactory,
                        JednostkaAdministracyjnaFactory)

import six


class TestRodzajMiejscowosci(unittest.TestCase):

    def test_str(self):
        rm = RodzajMiejscowosciFactory(id='96', nazwa='miasto')
        self.assertEqual(six.text_type(rm), '96: miasto')

    def test_set_val(self):
        rm = RodzajMiejscowosci()
        rm.set_val({'RM': '01',
                    'STAN_NA': '2013-02-28',
                    'NAZWA_RM': 'wieś'})
        self.assertEqual(rm.nazwa, 'wieś')
        self.assertEqual(rm.id, '01')
        self.assertEqual(rm.stan_na, '2013-02-28')


class TestJednostkaAdministracyjna(unittest.TestCase):
    def test_str(self):
        ja = JednostkaAdministracyjnaFactory(id='0201011', nazwa='Bolesławiec',
                nazwa_dod='gmina miejska')
        self.assertEqual(six.text_type(ja), '0201011: Bolesławiec')

    def test_set_val(self):
        gmina = JednostkaAdministracyjna()
        gmina.set_val({
            'GMI': '01',
            'POW': '01',
            'STAN_NA': '2013-01-01',
            'NAZDOD': 'gmina miejska',
            'RODZ': '1',
            'NAZWA': 'Bolesławiec',
            'WOJ': '02'
        })
        
        wojewodztwo = JednostkaAdministracyjna()
        wojewodztwo.set_val({
            'GMI': None,
            'POW': None,
            'STAN_NA': '2013-01-01',
            'NAZDOD': 'województwo',
            'RODZ': None,
            'NAZWA': u'DOLNOŚLĄSKIE',
            'WOJ': '02'})
        # Common
        self.assertEqual(gmina.stan_na, '2013-01-01')
        self.assertEqual(gmina.aktywny, False)

        # JednostkaAdministracyjna - gmina
        self.assertEqual(gmina.id, '0201011')
        self.assertEqual(gmina.nazwa, 'Bolesławiec')
        self.assertEqual(gmina.nazwa_dod, 'gmina miejska')

        # JednostkaAdministracyjna - województwo
        self.assertEqual(wojewodztwo.id, '02')
        self.assertEqual(wojewodztwo.nazwa, 'dolnośląskie')
        self.assertEqual(wojewodztwo.nazwa_dod, 'województwo')

    def test_parents(self):
        gmina = JednostkaAdministracyjnaFactory(id='0201012', nazwa='Bolesławiec',
                nazwa_dod='gmina wiejska')
        powiat = JednostkaAdministracyjnaFactory(id='0201', nazwa='bolesławiecki',
                nazwa_dod='powiat')
        wojewodztwo = JednostkaAdministracyjnaFactory(id='02',
                nazwa='DOLNOŚLĄSKIE', nazwa_dod='wojewdztwo')

        self.assertEqual(gmina.powiat(), powiat)
        self.assertEqual(gmina.wojewodztwo(), wojewodztwo)
        self.assertEqual(powiat.wojewodztwo(), wojewodztwo)
