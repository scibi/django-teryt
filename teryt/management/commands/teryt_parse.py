from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, DatabaseError, IntegrityError
from optparse import make_option


from teryt.models import (
    RodzajMiejscowosci, JednostkaAdministracyjna, Miejscowosc, Ulica
)
from teryt.utils import parse

import os.path


class Command(BaseCommand):
    args = '[xml file list]'
    help = 'Import TERYT data from XML files prepared by GUS'
    option_list = BaseCommand.option_list + (
        make_option('--update',
                    action='store_true',
                    dest='update',
                    default=False,
                    help='Update exisitng data'),
    )

    def handle(self, *args, **options):
        force_ins = not options['update']
        transaction.set_autocommit(False)

        fn_dict = {
            'WMRODZ.xml': RodzajMiejscowosci,
            'TERC.xml': JednostkaAdministracyjna,
            'SIMC.xml': Miejscowosc,
            'ULIC.xml': Ulica,
        }

        if not args:
            raise CommandError('At least 1 file name required')

        for a in args:
            try:
                c = fn_dict[os.path.basename(a)]
            except KeyError as e:
                raise CommandError('Unknown filename: {}'.format(e))

            try:
                c.objects.all().update(aktywny=False)
                for vals in parse(a):
                    t = c()
                    t.set_val(vals)
                    t.aktywny = True
                    t.save(force_insert=force_ins)
                transaction.commit()
            except IntegrityError as e:
                transaction.rollback()
                raise CommandError("Database integrity error: {}".format(e))
            except DatabaseError as e:
                transaction.rollback()
                raise CommandError("General database error: {}\n"
                                   "Make sure you run syncdb or migrate before"
                                   "importing data!".format(e))
