#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import factory

from ..models import RodzajMiejscowosci


class RodzajMiejscowosciFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RodzajMiejscowosci

    # Common
    stan_na = '2015-01-01'
    aktywny = True

    # RodzajMiejscowosci
    id = factory.Sequence(lambda n: "{:02d}".format(n))
    nazwa = factory.Sequence(lambda n: "Rodzaj {:02d}".format(n))
