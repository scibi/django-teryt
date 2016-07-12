#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as et
from django.utils.encoding import smart_text
import re

def_gus_url = 'http://www.stat.gov.pl/broker/access/prefile/'\
              'listPreFiles.jspa'


class HttpError(Exception):
    pass


class ParsingError(Exception):
    pass


def xstr(s):
    return '' if s is None else smart_text(s)


def parse(stream):
    for event, element in et.iterparse(stream):
        if element.tag != 'row':
            continue
        yield {
            x.get('name'): x.text.strip() if x.text else None for x in element
        }


def get_xml_id_dictionary(url=def_gus_url):
    from bs4 import BeautifulSoup
    import requests

    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise HttpError('Cannot connect to {}, '
            'status code: {}'.format(url, response.status_code))
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        files = {}
        table = soup.find(name='table', id='row')
        tbody = table.find(name='tbody')

        for tr in tbody.find_all(name='tr'):
            fname = tr.find(name='td')
            fname = fname.string
            fname = fname + '.xml'
            fid = tr.find(name='a', href=re.compile('downloadPreFile'))
            files[fname] = int(fid['href'].split('id=')[-1])
    except AttributeError:
        raise ParsingError('Cannot parse tree, '
        'possibly incorrect url or obsolete code.')

    return files
