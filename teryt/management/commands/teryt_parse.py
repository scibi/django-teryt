from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, DatabaseError, IntegrityError
from django.conf import settings
from optparse import make_option


from teryt.models import RodzajMiejsowosci, JednostkaAdministracyjna, Miejscowosc, Ulica
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

    @transaction.commit_manually
    def handle(self, *args, **options):
        if settings.DEBUG:
            raise CommandError('Django DEBUG is enabled. Please disable it to run this command')

        force_ins=not options['update']



        fn_dict={
            'WMRODZ.xml': RodzajMiejsowosci,
            'TERC.xml': JednostkaAdministracyjna,
            'SIMC.xml': Miejscowosc,
            'ULIC.xml': Ulica,
        }

        if not args:
            raise CommandError('At least 1 file name required')

        for a in args:
            try:
                c=fn_dict[os.path.basename(a)]
            except KeyError as e:
                raise CommandError('Unknown filename: {}'.format(e))

            try:
                for vals in parse(a):
                    t=c()
                    t.set_val(vals)
                    t.save(force_insert=force_ins)
                transaction.commit()
            except IntegrityError as e:
                transaction.rollback()
                raise CommandError("Database integrity error: {}".format(e))
            except DatabaseError as e:
                transaction.rollback()
                raise CommandError("General database error: {}\n"
                    "Make sure you run syncdb or migrate before importing"
                    " data!".format(e))

#        if options['all']:
#            if len(args)!=0:
#                raise CommandError('There should not bo arguments when option --all is given')
#            for r in LogReport.objects.filter(status__in=['NEW']):
#                self.run_report(r)
#        else:
#            if len(args)==0:
#                raise CommandError('You should give some arguments or option --all')
#            for a in args:
#                r=LogReport.objects.get(id=a)
#                self.run_report(r)
#                print r
#
#    @transaction.commit_manually
#    def run_report(self,r):
#        r.status='PROCESSING'
#        r.save(update_fields=['status'])
#        transaction.commit()
#        try:
#            r.prepare_time_ranges()
#            r.prepare_net_port_pairs()
#            r.prepare_sessions()
#            r.update_from_cp()
#            r.update_from_dhcp()
#            r.filter_mac()
#            r.filter_users()
#        except KeyboardInterrupt:
#            transaction.rollback()
#            r.status='NEW'
#            r.save(update_fields=['status'])
#            transaction.commit()
#            return
#        except:
#            transaction.rollback()
#            r.status='ERROR'
#            r.save(update_fields=['status'])
#            transaction.commit()
#            raise
#        else:
#            r.status='READY'
#            r.save(update_fields=['status'])
#            transaction.commit()
