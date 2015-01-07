# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JednostkaAdministracyjna',
            fields=[
                ('stan_na', models.DateField()),
                ('id', models.CharField(max_length=7, serialize=False, primary_key=True)),
                ('nazwa', models.CharField(max_length=50)),
                ('nazwa_dod', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Miejscowosc',
            fields=[
                ('stan_na', models.DateField()),
                ('symbol', models.CharField(max_length=7, serialize=False, primary_key=True)),
                ('nazwa', models.CharField(max_length=100)),
                ('jednostka', models.ForeignKey(to='teryt.JednostkaAdministracyjna')),
                ('miejscowosc_nadrzedna', models.ForeignKey(blank=True, to='teryt.Miejscowosc', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RodzajMiejsowosci',
            fields=[
                ('stan_na', models.DateField()),
                ('id', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('nazwa', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ulica',
            fields=[
                ('stan_na', models.DateField()),
                ('id', models.CharField(max_length=12, serialize=False, primary_key=True)),
                ('symbol_ulicy', models.CharField(max_length=10)),
                ('cecha', models.CharField(max_length=10)),
                ('nazwa_1', models.CharField(max_length=100)),
                ('nazwa_2', models.CharField(max_length=100, null=True, blank=True)),
                ('miejscowosc', models.ForeignKey(to='teryt.Miejscowosc')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='miejscowosc',
            name='rodzaj_miejscowosci',
            field=models.ForeignKey(to='teryt.RodzajMiejsowosci'),
            preserve_default=True,
        ),
    ]
