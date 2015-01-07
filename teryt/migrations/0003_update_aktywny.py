# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def update_aktywny(apps, schema_editor):
    model_list = [
        "JednostkaAdministracyjna", "Miejscowosc", "RodzajMiejsowosci", "Ulica"
    ]

    for model_name in model_list:
        print "Updating: {}".format(model_name)
        model_class = apps.get_model("teryt", model_name)

        akt_stan = model_class.objects.all().aggregate(models.Max('stan_na'))['stan_na__max']
        model_class.objects.filter(stan_na__exact=akt_stan).update(aktywny=True)
        model_class.objects.exclude(stan_na__exact=akt_stan).update(aktywny=False)


class Migration(migrations.Migration):

    dependencies = [
        ('teryt', '0002_add_aktywny'),
    ]

    operations = [
        migrations.RunPython(update_aktywny),
    ]
