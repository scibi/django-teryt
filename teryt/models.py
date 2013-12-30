# -*- coding: utf-8 -*-

from django.db import models

def xstr(s):
    return '' if s is None else str(s)

#WMRODZ
class RodzajMiejsowosci(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    nazwa = models.CharField(max_length=30)
    stan_na = models.DateField()

    def set_val(self, d):
        #{'RM': '01', 'STAN_NA': '2013-02-28', 'NAZWA_RM': u'wie\u015b'}
        self.id=d['RM']
        self.nazwa=d['NAZWA_RM']
        self.stan_na=d['STAN_NA']

    def __unicode__(self):
        return u'{}: {}'.format(self.id, self.nazwa)

# SIMC
class Miejscowosc(models.Model):
    symbol = models.CharField(max_length=7, primary_key=True)
    jednostka = models.ForeignKey('JednostkaAdministracyjna')
    miejscowosc_nadrzedna = models.ForeignKey('self', null=True, blank=True)
    nazwa = models.CharField(max_length=100)
    rodzaj_miejscowosci = models.ForeignKey('RodzajMiejsowosci')
    stan_na = models.DateField()

    def set_val(self, d):
        #{'GMI': '06', 'RODZ_GMI': '5', 'POW': '18', 'STAN_NA': '2013-03-06',
        # 'SYM': '0861110', 'NAZWA': 'Strzygowska Kolonia', 'WOJ': '04', 'RM':
        # '02', 'SYMPOD': '0861110', 'MZ': '1'}
        self.symbol=d['SYM']
        self.nazwa=d['NAZWA']
        self.rodzaj_miejscowosci_id=d['RM']
        self.stan_na=d['STAN_NA']

        if d['SYMPOD']!=d['SYM']:
            self.miejscowosc_nadrzedna_id=d['SYMPOD']
        self.jednostka_id=d['WOJ']+xstr(d['POW'])+xstr(d['GMI'])+xstr(d['RODZ_GMI'])

# TERC
class JednostkaAdministracyjna(models.Model):
    LEN_TYPE={
        7: 'GMI',
        4: 'POW',
        2: 'WOJ',
    }

    id = models.CharField(max_length=7, primary_key=True)
    nazwa = models.CharField(max_length=50)
    nazwa_dod = models.CharField(max_length=50)
    stan_na = models.DateField()

    def typ(self):
        return self.LEN_TYPE[len(self.id)]

    def set_val(self, d):
        # {'GMI': None, 'POW': None, 'STAN_NA': '2013-01-01', 'NAZDOD':
        #  u'wojew\xf3dztwo', 'RODZ': None, 'NAZWA': u'DOLNO\u015aL\u0104SKIE',
        #  'WOJ': '02'}
        # {'GMI': '01', 'POW': '01', 'STAN_NA': '2013-01-01', 'NAZDOD':
        #  'gmina miejska', 'RODZ': '1', 'NAZWA': u'Boles\u0142awiec', 'WOJ':
        #  '02'}
        self.nazwa=d['NAZWA']
        self.nazwa_dod=d['NAZDOD']
        self.stan_na=d['STAN_NA']

        self.id=d['WOJ']+xstr(d['POW'])+xstr(d['GMI'])+xstr(d['RODZ'])
        if self.typ()=='WOJ':
            self.nazwa = self.nazwa.lower()
        

    def __unicode__(self):
        return u'{}: {}'.format(self.id, self.nazwa)

# ULIC
class Ulica(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    miejscowosc = models.ForeignKey('Miejscowosc')
    symbol_ulicy = models.CharField(max_length=10)
    cecha = models.CharField(max_length=10)
    nazwa_1 = models.CharField(max_length=100)
    nazwa_2 = models.CharField(max_length=100, null=True, blank=True)
    stan_na = models.DateField()

    def set_val(self, d):
        # {'GMI': '03', 'RODZ_GMI': '2', 'NAZWA_1': 'Cicha', 'NAZWA_2': None, 'POW':
        # '03', 'STAN_NA': '2013-12-16', 'SYM': '0185962', 'CECHA': 'ul.', 'WOJ': '08',
        # 'SYM_UL': '02974'}
        self.id=d['SYM']+d['SYM_UL']
        self.miejscowosc_id=d['SYM']
        self.symbol_ulicy=d['SYM_UL']
        self.cecha=d['CECHA']
        self.nazwa_1=d['NAZWA_1']
        self.nazwa_2=d['NAZWA_2']
        self.stan_na=d['STAN_NA']

    def __unicode__(self):
        return u'{s.cecha} {s.nazwa_2} {s.nazwa_1} ({s.miejscowosc.nazwa})'.format(s=self)
