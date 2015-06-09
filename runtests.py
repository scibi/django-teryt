import sys
from optparse import OptionParser

try:
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
#        DATABASES={
#            "default": {
#                "ENGINE": "django.db.backends.sqlite3",
#            }
#        },
	DATABASES = {
	    'default': {
	        'ENGINE':'django.db.backends.postgresql_psycopg2',
                'NAME': 'django_teryt',
		'USER': 'postgres',
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
        SITE_ID=1,
        NOSE_ARGS=[],
    )

    from django_nose import NoseTestSuiteRunner
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


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
