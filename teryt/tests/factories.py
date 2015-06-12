#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import factory

from ..models import RodzajMiejscowosci, JednostkaAdministracyjna, Miejscowosc


class RodzajMiejscowosciFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RodzajMiejscowosci

    # Common
    stan_na = '2015-01-01'
    aktywny = True

    # RodzajMiejscowosci
    id = factory.Sequence(lambda n: "{:02d}".format(n))
    nazwa = factory.Sequence(lambda n: "Rodzaj {:02d}".format(n))


class JednostkaAdministracyjnaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JednostkaAdministracyjna

    # Common
    stan_na = '2015-01-01'
    aktywny = True

    # JednostkaAdministracyjna
    id = factory.Sequence(lambda n: "{:07d}".format(n))
    nazwa = factory.Sequence(lambda n: "Gmina {}".format(n))
    nazwa_dod = 'gmina miejska'


class MiejscowoscFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Miejscowosc

    # Common
    stan_na = '2015-01-01'
    aktywny = True

    # Miejscowosc
    symbol = factory.Sequence(lambda n: "{:07d}".format(n))
    jednostka = factory.SubFactory(JednostkaAdministracyjnaFactory)
    miejscowosc_nadrzedna = factory.SubFactory(
        'teryt.tests.factories.MiejscowoscFactory')
    nazwa = factory.Sequence(lambda n: "Miejscowość {}".format(n))
    rodzaj_miejscowosci = factory.SubFactory(RodzajMiejscowosciFactory)
