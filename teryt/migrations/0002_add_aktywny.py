# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teryt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jednostkaadministracyjna',
            name='aktywny',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='miejscowosc',
            name='aktywny',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rodzajmiejsowosci',
            name='aktywny',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ulica',
            name='aktywny',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
