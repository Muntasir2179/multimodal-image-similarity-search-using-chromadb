#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dashboard.settings import BASE_DIR


def main():
    # creating uploads folder if it doesn't exists
    if 'uploads' not in os.listdir(path=BASE_DIR):
        os.mkdir(path=BASE_DIR / 'uploads')

    # for vector database folder
    if 'database' not in os.listdir(path=BASE_DIR):
        os.mkdir(path=BASE_DIR / 'database')
    
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
