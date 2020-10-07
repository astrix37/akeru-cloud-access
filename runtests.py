#!/usr/bin/env python
import os
import sys

import django
from django.test.runner import DiscoverRunner
from django.core.management import call_command


if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    call_command("makemigrations", "akeru")
    call_command("migrate", "akeru")
    test_runner = DiscoverRunner()
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))
