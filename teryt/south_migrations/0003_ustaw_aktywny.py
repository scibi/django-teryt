# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.db.models import Max

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        print "Updating: JednostkaAdministracyjna"
        ja_akt_stan=orm.JednostkaAdministracyjna.objects.all().aggregate(Max('stan_na'))['stan_na__max']
        orm.JednostkaAdministracyjna.objects.filter(stan_na__exact=ja_akt_stan).update(aktywny=True)
        orm.JednostkaAdministracyjna.objects.exclude(stan_na__exact=ja_akt_stan).update(aktywny=False)

        print "Updating: Miejscowosc"
        m_akt_stan=orm.Miejscowosc.objects.all().aggregate(Max('stan_na'))['stan_na__max']
        orm.Miejscowosc.objects.filter(stan_na__exact=m_akt_stan).update(aktywny=True)
        orm.Miejscowosc.objects.exclude(stan_na__exact=m_akt_stan).update(aktywny=False)

        print "Updating: RodzajMiejsowosci"
        rm_akt_stan=orm.RodzajMiejsowosci.objects.all().aggregate(Max('stan_na'))['stan_na__max']
        orm.RodzajMiejsowosci.objects.filter(stan_na__exact=rm_akt_stan).update(aktywny=True)
        orm.RodzajMiejsowosci.objects.exclude(stan_na__exact=rm_akt_stan).update(aktywny=False)

        print "Updating: Ulica"
        u_akt_stan=orm.Ulica.objects.all().aggregate(Max('stan_na'))['stan_na__max']
        orm.Ulica.objects.filter(stan_na__exact=u_akt_stan).update(aktywny=True)
        orm.Ulica.objects.exclude(stan_na__exact=u_akt_stan).update(aktywny=False)

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'teryt.jednostkaadministracyjna': {
            'Meta': {'object_name': 'JednostkaAdministracyjna'},
            'aktywny': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nazwa_dod': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'stan_na': ('django.db.models.fields.DateField', [], {})
        },
        u'teryt.miejscowosc': {
            'Meta': {'object_name': 'Miejscowosc'},
            'aktywny': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'jednostka': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teryt.JednostkaAdministracyjna']"}),
            'miejscowosc_nadrzedna': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teryt.Miejscowosc']", 'null': 'True', 'blank': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rodzaj_miejscowosci': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teryt.RodzajMiejsowosci']"}),
            'stan_na': ('django.db.models.fields.DateField', [], {}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'})
        },
        u'teryt.rodzajmiejsowosci': {
            'Meta': {'object_name': 'RodzajMiejsowosci'},
            'aktywny': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'stan_na': ('django.db.models.fields.DateField', [], {})
        },
        u'teryt.ulica': {
            'Meta': {'object_name': 'Ulica'},
            'aktywny': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'cecha': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '12', 'primary_key': 'True'}),
            'miejscowosc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teryt.Miejscowosc']"}),
            'nazwa_1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'nazwa_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'stan_na': ('django.db.models.fields.DateField', [], {}),
            'symbol_ulicy': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['teryt']
    symmetrical = True
