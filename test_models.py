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
            'archivebox.tags', # Ensure we use full path
            'archivebox.crawls',
            'archivebox.machine',
            'archivebox.workers',
        ],
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    )
    django.setup()

try:
    from archivebox.crawls.models import Seed
    print("Successfully imported Seed")
except Exception as e:
    print(f"Error importing Seed: {e}")

try:
    from archivebox.machine.models import Process
    print("Successfully imported Process")
except Exception as e:
    print(f"Error importing Process: {e}")

try:
    from archivebox.workers.models import Event
    print("Successfully imported Event")
except Exception as e:
    print(f"Error importing Event: {e}")
