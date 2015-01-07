# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teryt', '0003_update_aktywny'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jednostkaadministracyjna',
            name='aktywny',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='miejscowosc',
            name='aktywny',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rodzajmiejsowosci',
            name='aktywny',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ulica',
            name='aktywny',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
