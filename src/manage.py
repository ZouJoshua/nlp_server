#!/usr/bin/env python
import os
import sys


def set_environ(server_name):
    os.environ.setdefault("NLP_SERVER_NAME", server_name)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.{}_conf".format(server_name))



if __name__ == '__main__':
    set_environ("video_classification")
    os.environ.get('DJANGO_SETTINGS_MODULE', 'config.base_conf')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
