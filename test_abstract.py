import os
import sys
import django
from django.conf import settings

# Add project root AND archivebox subdir to sys.path
sys.path.append('/home/ubuntu/workspace/ArchiveBox')
sys.path.append('/home/ubuntu/workspace/ArchiveBox/archivebox')

# Minimal Django settings
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'tags', 
        ],
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    )
    django.setup()

try:
    from archivebox.base_models.models import ModelWithSerializers
    print("Successfully imported ModelWithSerializers")
except Exception as e:
    print(f"Error: {e}")