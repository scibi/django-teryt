# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Miejscowosc.aktywny'
        db.alter_column(u'teryt_miejscowosc', 'aktywny', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Ulica.aktywny'
        db.alter_column(u'teryt_ulica', 'aktywny', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'JednostkaAdministracyjna.aktywny'
        db.alter_column(u'teryt_jednostkaadministracyjna', 'aktywny', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RodzajMiejsowosci.aktywny'
        db.alter_column(u'teryt_rodzajmiejsowosci', 'aktywny', self.gf('django.db.models.fields.BooleanField')())

    def backwards(self, orm):

        # Changing field 'Miejscowosc.aktywny'
        db.alter_column(u'teryt_miejscowosc', 'aktywny', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'Ulica.aktywny'
        db.alter_column(u'teryt_ulica', 'aktywny', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'JednostkaAdministracyjna.aktywny'
        db.alter_column(u'teryt_jednostkaadministracyjna', 'aktywny', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RodzajMiejsowosci.aktywny'
        db.alter_column(u'teryt_rodzajmiejsowosci', 'aktywny', self.gf('django.db.models.fields.NullBooleanField')(null=True))

    models = {
        u'teryt.jednostkaadministracyjna': {
            'Meta': {'object_name': 'JednostkaAdministracyjna'},
            'aktywny': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nazwa_dod': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'stan_na': ('django.db.models.fields.DateField', [], {})
        },
        u'teryt.miejscowosc': {
            'Meta': {'object_name': 'Miejscowosc'},
            'aktywny': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jednostka': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teryt.JednostkaAdministracyjna']"}),
            'miejscowosc_nadrzedna': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teryt.Miejscowosc']", 'null': 'True', 'blank': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rodzaj_miejscowosci': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teryt.RodzajMiejsowosci']"}),
            'stan_na': ('django.db.models.fields.DateField', [], {}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'})
        },
        u'teryt.rodzajmiejsowosci': {
            'Meta': {'object_name': 'RodzajMiejsowosci'},
            'aktywny': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'stan_na': ('django.db.models.fields.DateField', [], {})
        },
        u'teryt.ulica': {
            'Meta': {'object_name': 'Ulica'},
            'aktywny': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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