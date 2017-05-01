"""
./manage.py teryt_parse [xml/zip files] [--update]
------------

Command will parse xml/zip and upload it into teryt database.
Option --update must be used if files have records
already existing in database
"""

from optparse import make_option
import zipfile

from django.core.management.base import BaseCommand, CommandError

from teryt.utils_zip import update_database


class Command(BaseCommand):
    args = '[xml/zip file list]'
    help = 'Import TERYT data from XML/ZIP files prepared by GUS'
    option_list = BaseCommand.option_list + (
        make_option('--update',
                    action='store_true',
                    dest='update',
                    default=False,
                    help='Update exisitng data'),
    )

    def handle(self, *args, **options):
        force_ins = not options['update']

        if not args:
            raise CommandError('At least 1 file name required')

        for data_file in args:
            self.stdout.write('Working on {}'.format(data_file))
            if zipfile.is_zipfile(data_file):
                zfile = zipfile.ZipFile(data_file)
                fname = zfile.namelist()[0]
                with zfile.open(fname) as xml_file:
                    update_database(xml_file, fname, force_ins)
            else:
                with open(data_file) as xml_file:
                    update_database(xml_file, data_file, force_ins)
            self.stdout.write('File {} uploaded'.format(data_file))

        self.stdout.write("Done.")
