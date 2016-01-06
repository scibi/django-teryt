# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'JednostkaAdministracyjna.typ'
        db.add_column(u'teryt_jednostkaadministracyjna', 'typ',
                      self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'JednostkaAdministracyjna.typ'
        db.delete_column(u'teryt_jednostkaadministracyjna', 'typ')


    models = {
        u'teryt.jednostkaadministracyjna': {
            'Meta': {'object_name': 'JednostkaAdministracyjna'},
            'aktywny': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nazwa_dod': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'stan_na': ('django.db.models.fields.DateField', [], {}),
            'typ': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'})
        },
        u'teryt.miejscowosc': {
            'Meta': {'object_name': 'Miejscowosc'},
            'aktywny': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jednostka': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teryt.JednostkaAdministracyjna']"}),
            'miejscowosc_nadrzedna': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teryt.Miejscowosc']", 'null': 'True', 'blank': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rodzaj_miejscowosci': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teryt.RodzajMiejscowosci']"}),
            'stan_na': ('django.db.models.fields.DateField', [], {}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'})
        },
        u'teryt.rodzajmiejscowosci': {
            'Meta': {'object_name': 'RodzajMiejscowosci'},
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