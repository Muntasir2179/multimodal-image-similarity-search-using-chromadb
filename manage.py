#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dashboard.settings import BASE_DIR
import shutil


def main():
    # creating uploads folder if it doesn't exists
    if 'uploads' not in os.listdir(path=BASE_DIR):
        os.mkdir(path=BASE_DIR / 'uploads')
    else:
        # clearing previous data in uploads folder
        if len(os.listdir(path=BASE_DIR / 'uploads')) != 0:
            files = os.listdir(path=BASE_DIR / 'uploads')
            for item in files:
                # if it is a file
                if os.path.isfile(BASE_DIR / f'uploads/{item}'):
                    os.remove(path=BASE_DIR / f'uploads/{item}')
                
                # if it is a directory
                if os.path.isdir(BASE_DIR / f'uploads/{item}'):
                    shutil.rmtree(path=BASE_DIR / f'uploads/{item}')

    # for vector database folder
    if 'database' not in os.listdir(path=BASE_DIR):
        os.mkdir(path=BASE_DIR / 'database')
    else:
        # cleaning the previous vector data
        if len(os.listdir(path=BASE_DIR / 'database')) != 0:
            files = os.listdir(path=BASE_DIR / 'database')
            for item in files:
                # if it is a file
                if os.path.isfile(path=BASE_DIR / f"database/{item}"):
                    os.remove(path=BASE_DIR / f"database/{item}")
                
                # if it is a directory
                if os.path.isdir(BASE_DIR / f"database/{item}"):
                    shutil.rmtree(path=BASE_DIR / f"database/{item}")
    
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
