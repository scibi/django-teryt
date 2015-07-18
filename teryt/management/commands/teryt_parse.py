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
                with transaction.atomic():
                    c.objects.all().update(aktywny=False)

                    row_list = parse(a)

                    # MySQL doesn't support deferred checking of foreign key
                    # constraints. As a workaround we sort data placing rows
                    # with no a parent row at the begining.
                    if c is Miejscowosc:
                        row_list = sorted(row_list, key=lambda x: '0000000'
                                          if x['SYM'] == x['SYMPOD']
                                          else x['SYM'])

                    for vals in row_list:
                        t = c()
                        t.set_val(vals)
                        t.aktywny = True
                        t.save(force_insert=force_ins)
            except IntegrityError as e:
                raise CommandError("Database integrity error: {}".format(e))
            except DatabaseError as e:
                raise CommandError("General database error: {}\n"
                                   "Make sure you run syncdb or migrate before"
                                   "importing data!".format(e))
