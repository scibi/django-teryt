#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

"""
test_django-teryt
------------

Tests for `django-teryt` modules module.
"""
from django.utils import six
from django.test import TestCase
from django.db import models

from ..models import (RodzajMiejscowosci, JednostkaAdministracyjna,
                      Miejscowosc, Ulica)
from .factories import (RodzajMiejscowosciFactory,
                        JednostkaAdministracyjnaFactory,
                        MiejscowoscFactory, UlicaFactory)


class MixinTestObjectsManager(object):
    def test_objects_model_manager(self):
        self.assertIsInstance(JednostkaAdministracyjna.objects, models.Manager)


class TestRodzajMiejscowosci(TestCase, MixinTestObjectsManager):

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


class TestJednostkaAdministracyjna(TestCase, MixinTestObjectsManager):
    def setUp(self):
        self.rm_miasto = RodzajMiejscowosciFactory(
            id='96',
            nazwa='miasto')

        self.gmina = JednostkaAdministracyjnaFactory(
            id='0201011',
            nazwa='Bolesławiec',
            nazwa_dod='gmina miejska')

        self.gmina_nowogrodziec = JednostkaAdministracyjnaFactory(
            id='0201044',
            nazwa='Nowogrodziec',
            nazwa_dod='miasto')

        self.powiat = JednostkaAdministracyjnaFactory(
            id='0201',
            nazwa='bolesławiecki',
            nazwa_dod='powiat')

        self.wojewodztwo = JednostkaAdministracyjnaFactory(
            id='02',
            nazwa='DOLNOŚLĄSKIE',
            nazwa_dod='wojewdztwo')

        self.boleslawiec = MiejscowoscFactory(
            symbol='0935989',
            jednostka=self.gmina,
            miejscowosc_nadrzedna=None,
            nazwa='Bolesławiec',
            rodzaj_miejscowosci=self.rm_miasto)

        self.nowogrodziec = MiejscowoscFactory(
            symbol='0936262',
            jednostka=self.gmina_nowogrodziec,
            miejscowosc_nadrzedna=None,
            nazwa='Nowogrodziec',
            rodzaj_miejscowosci=self.rm_miasto)

    def test_str(self):
        self.assertEqual(six.text_type(self.gmina), '0201011: Bolesławiec')

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
        self.assertEqual(gmina.typ, 'GMI')

        # JednostkaAdministracyjna - województwo
        self.assertEqual(wojewodztwo.id, '02')
        self.assertEqual(wojewodztwo.nazwa, 'dolnośląskie')
        self.assertEqual(wojewodztwo.nazwa_dod, 'województwo')
        self.assertEqual(wojewodztwo.typ, 'WOJ')

    def test_parents(self):

        self.assertEqual(self.gmina.powiat(), self.powiat)
        self.assertEqual(self.gmina.wojewodztwo(), self.wojewodztwo)
        self.assertEqual(self.powiat.wojewodztwo(), self.wojewodztwo)

    def test_managers_wojewodztwa(self):
        self.assertIsInstance(JednostkaAdministracyjna.wojewodztwa,
                              models.Manager)
        self.assertEqual(JednostkaAdministracyjna.wojewodztwa.count(), 1)
        JednostkaAdministracyjna.wojewodztwa.get(id='02')

    def test_managers_powiaty(self):
        self.assertIsInstance(JednostkaAdministracyjna.powiaty, models.Manager)
        self.assertEqual(JednostkaAdministracyjna.powiaty.count(), 1)
        JednostkaAdministracyjna.powiaty.get(id='0201')

    def test_managers_gminy(self):
        self.assertIsInstance(JednostkaAdministracyjna.gminy, models.Manager)
        self.assertEqual(JednostkaAdministracyjna.gminy.count(), 2)
        JednostkaAdministracyjna.gminy.get(id='0201011')

    def test_miejscowosci(self):
        self.assertEqual(self.gmina.miejscowosci().count(), 1)
        self.assertEqual(self.powiat.miejscowosci().count(), 2)
        self.assertEqual(self.wojewodztwo.miejscowosci().count(), 2)
        self.gmina.miejscowosci().get(symbol='0935989')


class TestMiejscowosc(TestCase, MixinTestObjectsManager):
    def setUp(self):
        self.miejscowosc = MiejscowoscFactory(
            symbol='0861110',
            miejscowosc_nadrzedna=None,
            nazwa='Strzygowska Kolonia',
            rodzaj_miejscowosci__id='02',
            rodzaj_miejscowosci__nazwa='kolonia')

        self.warszawa = MiejscowoscFactory(
            symbol='0918123',
            miejscowosc_nadrzedna=None,
            nazwa='Warszawa',
            rodzaj_miejscowosci__id='96',
            rodzaj_miejscowosci__nazwa='miasto')

        self.wies = MiejscowoscFactory(
            symbol='0005546',
            miejscowosc_nadrzedna=None,
            nazwa='Wolica',
            rodzaj_miejscowosci__id='01',
            rodzaj_miejscowosci__nazwa='wieś')

    def test_managers_miasta(self):
        self.assertIsInstance(Miejscowosc.miasta, models.Manager)
        self.assertEqual(Miejscowosc.miasta.count(), 1)
        Miejscowosc.miasta.get(symbol='0918123')

    def test_managers_wsie(self):
        self.assertIsInstance(Miejscowosc.wsie, models.Manager)
        self.assertEqual(Miejscowosc.wsie.count(), 1)
        Miejscowosc.wsie.get(symbol='0005546')

    def test_str(self):
        self.assertEqual(six.text_type(self.miejscowosc),
                         '0861110: Strzygowska Kolonia')

    def test_set_val(self):
        m_dict = {
            'GMI': '06',
            'RODZ_GMI': '5',
            'POW': '18',
            'STAN_NA': '2013-03-06',
            'SYM': '0861110',
            'NAZWA': 'Strzygowska Kolonia',
            'WOJ': '04',
            'RM': '02',
            'SYMPOD': '0861110',
            'MZ': '1'
        }
        miejscowosc = Miejscowosc()
        miejscowosc.set_val(m_dict)

        # Common
        self.assertEqual(miejscowosc.stan_na, '2013-03-06')
        self.assertEqual(miejscowosc.aktywny, False)

        # Miejscowosc
        self.assertIsNone(miejscowosc.miejscowosc_nadrzedna)
        self.assertEqual(miejscowosc.symbol, '0861110')
        self.assertEqual(miejscowosc.jednostka_id, '0418065')
        self.assertEqual(miejscowosc.nazwa, 'Strzygowska Kolonia')
        # RodzajMiejscowosci instance made in setUp()
        self.assertEqual(miejscowosc.rodzaj_miejscowosci.nazwa, 'kolonia')

        m_dict['SYMPOD'] = '1234567'
        miejscowosc2 = Miejscowosc()
        miejscowosc2.set_val(m_dict)
        self.assertEqual(miejscowosc2.miejscowosc_nadrzedna_id, '1234567')


class TestUlica(TestCase, MixinTestObjectsManager):
    def setUp(self):
        self.ulica1 = UlicaFactory(
            miejscowosc__miejscowosc_nadrzedna=None
        )

        self.ulica2 = UlicaFactory(
            cecha='pl.',
            nazwa_1='Hoffa',
            nazwa_2='Bogumiła',
            miejscowosc__miejscowosc_nadrzedna=None
        )

    def test_str(self):
        self.assertEqual(six.text_type(self.ulica1), 'ul. {} ({})'.format(
            self.ulica1.nazwa_1, self.ulica1.miejscowosc.nazwa))

        self.assertEqual(six.text_type(self.ulica2),
                         'pl. Bogumiła Hoffa ({})'.format(
                         self.ulica2.miejscowosc.nazwa))

    def test_set_val(self):
        m_dict = {
            'GMI': '03',
            'RODZ_GMI': '2',
            'NAZWA_1': 'Cicha',
            'NAZWA_2': None,
            'POW': '03',
            'STAN_NA': '2013-12-16',
            'SYM': '0185962',
            'CECHA': 'ul.',
            'WOJ': '08',
            'SYM_UL': '02974'
        }
        ulica = Ulica()
        ulica.set_val(m_dict)

        # Common
        self.assertEqual(ulica.stan_na, '2013-12-16')
        self.assertEqual(ulica.aktywny, False)

        # Ulica
        self.assertEqual(ulica.id, '018596202974')
        self.assertEqual(ulica.miejscowosc_id, '0185962')
        self.assertEqual(ulica.symbol_ulicy, '02974')
        self.assertEqual(ulica.cecha, 'ul.')
        self.assertEqual(ulica.nazwa_1, 'Cicha')
        self.assertIsNone(ulica.nazwa_2)
