#!/bin/bash

TEST_TYPES="unit integration"
DJANGO_VERSIONS="16 17 18 19"
PYTHON_VERSIONS="py27 py34"
DB_ENGINES="pgsql mysql sqlite"
DB_URL_pgsql="postgres://postgres@/django_teryt"
DB_URL_sqlite="sqlite://:memory:"
DB_URL_mysql="mysql://root:@localhost/django_teryt"

for test_type in $TEST_TYPES; do
  for python_version in $PYTHON_VERSIONS; do
    for django_version in $DJANGO_VERSIONS; do
      for db_engine in $DB_ENGINES; do
        db_url_name=DB_URL_${db_engine}
        db_url=${!db_url_name}

        echo -n "    - TOXENV=${python_version}-django-${django_version}-${test_type}"
        echo -e "\tDATABASE_URL=\"${db_url}\""
      done
    done
  done
done
