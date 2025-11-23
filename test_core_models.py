import os
import sys
import django
from django.conf import settings

# Add project root to sys.path
sys.path.append('/home/ubuntu/workspace/ArchiveBox')

# Minimal Django settings
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
            'django_huey',
            'bx_django_utils',
            'huey_monitor',
            'archivebox.tags',
            'archivebox.crawls',
            'archivebox.machine',
            'archivebox.workers',
            'archivebox.core',
        ],
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
        DJANGO_HUEY={
            'default': 'commands',
            'queues': {
                'commands': {
                    'huey_class': 'huey.SqliteHuey',
                    'name': 'commands',
                    'filename': ':memory:',
                }
            }
        },
        HUEY={
            'huey_class': 'huey.SqliteHuey',
            'name': 'commands',
            'filename': ':memory:',
        },
    )
    django.setup()

try:
    from archivebox.core.models import Snapshot
    print("Successfully imported Snapshot")
except Exception as e:
    print(f"Error importing Snapshot: {e}")
