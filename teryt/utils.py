#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as et


def parse(stream):
    for event, element in et.iterparse(stream):
        if element.tag != 'row':
            continue
        yield {
            x.get('name'): x.text.strip() if x.text else None for x in element
        }
