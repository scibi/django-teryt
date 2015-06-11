#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
import os
from optparse import OptionParser

try:
    from django.conf import settings

    import django
    print("Django version: {}".format(django.get_version()))

    db_user = os.getenv('TEST_DB_USER', 'django_teryt')

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        # DATABASES={
        #   "default": {
        #       "ENGINE": "django.db.backends.sqlite3",
        #   }
        # },
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'django_teryt',
                'USER': db_user,
                'PASSWORD': '',
            }
        },
        ROOT_URLCONF="teryt.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "teryt",
        ],
        # To suppress Django 1.7 warning about changed defaults
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware'
        ),
        SITE_ID=1,
        TEST_RUNNER = 'django_nose.NoseTestSuiteRunner',
        NOSE_ARGS=['-s'],
    )

    from django_nose import NoseTestSuiteRunner
except ImportError:
    raise ImportError("To fix this error, run: "
                      "pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['teryt.tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=2)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    run_tests(*args)
