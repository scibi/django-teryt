from collections import OrderedDict
import io
import os.path
import zipfile

from django.core.management.base import CommandError
from django.db import transaction, DatabaseError, IntegrityError
import requests

from .models import (RodzajMiejscowosci, JednostkaAdministracyjna,
                    Miejscowosc, Ulica)
from .utils import get_xml_id_dictionary, parse

# Dictionary containing teryt data files and according 
# data models inside them. Order is crucual correct data update -
# Miejscowosc depends on RodzajMiejscowosci and so on. If file would
# be updated in other order, foreign keys dependencies will be broken.
fn_dict = OrderedDict([
            ('WMRODZ.xml', RodzajMiejscowosci),
            ('TERC.xml', JednostkaAdministracyjna),
            ('SIMC.xml', Miejscowosc),
            ('ULIC.xml', Ulica),
        ])

url_tmpl = 'http://www.stat.gov.pl/broker/access/'\
            'prefile/downloadPreFile.jspa?id={}'


def open_zipfile_from_url(filename, url):
    request = requests.get(url, stream=True)
    zfile = zipfile.ZipFile(io.BytesIO(request.content))
    return zfile


def get_zip_files():
    zip_files = []
    xml_dictionary = get_xml_id_dictionary()
    for file in fn_dict.keys():
        zfile = open_zipfile_from_url(
                file,
                url_tmpl.format(xml_dictionary[file])
            )
        zip_files.append(zfile)

    return zip_files


def update_database(xml_stream, fname, force_flag):
    try:
        teryt_class = fn_dict[os.path.basename(fname)]
    except KeyError as e:
        raise CommandError('Unknown filename: {}'.format(e))

    try:
        with transaction.atomic():
            teryt_class.objects.all().update(aktywny=False)

            row_list = parse(xml_stream)

            # MySQL doesn't support deferred checking of foreign key
            # constraints. As a workaround we sort data placing rows
            # with no a parent row at the begining.
            if teryt_class is Miejscowosc:
                row_list = sorted(row_list, key=lambda x: '0000000'
                                  if x['SYM'] == x['SYMPOD']
                                  else x['SYM'])

            for vals in row_list:
                instance = teryt_class()
                instance.set_val(vals)
                instance.aktywny = True
                instance.save(force_insert=force_flag)

    except IntegrityError as e:
        raise CommandError("Database integrity error: {}".format(e))
    except DatabaseError as e:
        raise CommandError("General database error: {}\n"
                           "Make sure you run syncdb or migrate before"
                           "importing data!".format(e))
    except TypeError as e:
        raise CommandError("File type error: {}\n"
                           "Check if your file is correct "
                           "xml file".format(e))
