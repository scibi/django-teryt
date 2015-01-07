# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RodzajMiejsowosci'
        db.create_table(u'teryt_rodzajmiejsowosci', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
            ('nazwa', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('stan_na', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'teryt', ['RodzajMiejsowosci'])

        # Adding model 'Miejscowosc'
        db.create_table(u'teryt_miejscowosc', (
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=7, primary_key=True)),
            ('jednostka', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teryt.JednostkaAdministracyjna'])),
            ('miejscowosc_nadrzedna', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teryt.Miejscowosc'], null=True, blank=True)),
            ('nazwa', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('rodzaj_miejscowosci', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teryt.RodzajMiejsowosci'])),
            ('stan_na', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'teryt', ['Miejscowosc'])

        # Adding model 'JednostkaAdministracyjna'
        db.create_table(u'teryt_jednostkaadministracyjna', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=7, primary_key=True)),
            ('nazwa', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('nazwa_dod', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('stan_na', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'teryt', ['JednostkaAdministracyjna'])

        # Adding model 'Ulica'
        db.create_table(u'teryt_ulica', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=12, primary_key=True)),
            ('miejscowosc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teryt.Miejscowosc'])),
            ('symbol_ulicy', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('cecha', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('nazwa_1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('nazwa_2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('stan_na', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'teryt', ['Ulica'])


    def backwards(self, orm):
        # Deleting model 'RodzajMiejsowosci'
        db.delete_table(u'teryt_rodzajmiejsowosci')

        # Deleting model 'Miejscowosc'
        db.delete_table(u'teryt_miejscowosc')

        # Deleting model 'JednostkaAdministracyjna'
        db.delete_table(u'teryt_jednostkaadministracyjna')

        # Deleting model 'Ulica'
        db.delete_table(u'teryt_ulica')


    models = {
        u'teryt.jednostkaadministracyjna': {
            'Meta': {'object_name': 'JednostkaAdministracyjna'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nazwa_dod': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'stan_na': ('django.db.models.fields.DateField', [], {})
        },
        u'teryt.miejscowosc': {
            'Meta': {'object_name': 'Miejscowosc'},
            'jednostka': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teryt.JednostkaAdministracyjna']"}),
            'miejscowosc_nadrzedna': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teryt.Miejscowosc']", 'null': 'True', 'blank': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rodzaj_miejscowosci': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teryt.RodzajMiejsowosci']"}),
            'stan_na': ('django.db.models.fields.DateField', [], {}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'})
        },
        u'teryt.rodzajmiejsowosci': {
            'Meta': {'object_name': 'RodzajMiejsowosci'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'stan_na': ('django.db.models.fields.DateField', [], {})
        },
        u'teryt.ulica': {
            'Meta': {'object_name': 'Ulica'},
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