#!/usr/bin/env python
# -*- coding: utf-8 -*-


import xml.etree.cElementTree as et

def parse(stream):
    for event, element in et.iterparse(stream):
        if element.tag != 'row':
            continue
        yield {x.get('name'):x.text.strip() if x.text else None for x in element}

#for x in teryt_parse('/tmp/teryt/TERC.xml'):
#for x in teryt_parse('/tmp/teryt/WMRODZ.xml'):
#for x in teryt_parse('/tmp/teryt/SIMC.xml'):
#for x in teryt_parse('/tmp/teryt/ULIC.xml'):
#    print x
#parse('/tmp/teryt/SIMC.xml')
#parse('/tmp/teryt/ULIC.xml')
#parse('/tmp/teryt/TERC.xml')
