"""
./manage.py teryt_auto_update
------------

Command will automatically download all teryt data files
from GUS site, unpack them and upload into database.

Database should be set up before updating it!
"""
from django.core.management.base import BaseCommand

from teryt.utils_zip import (
    get_zip_files, update_database
)


class Command(BaseCommand):
    help = 'Import TERYT data from ZIP files prepared by GUS,\
            auto download, unpack and update with them.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        # download zip files from GUS site
        zip_files = get_zip_files() 

        for zfile in zip_files:
            # only file inside a proper archive is xml with teryt data
            fname = zfile.namelist()[0]
            self.stdout.write('Working on {}'.format(fname))
            with zfile.open(fname) as xml_file:
                update_database(xml_file, fname, False)
                self.stdout.write('File {} uploaded.'.format(fname))

        self.stdout.write("Done.")
