import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Self_LearningPython.settings')
try:
    from django.core.management import execute_from_command_line
except ImportError as exc:
    raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
execute_from_command_line(sys.argv)
from django.contrib.auth.models import User
user = User.objects.get(username='toantoanphatdinh')  # Replace with actual username
user.is_staff = True
user.is_superuser = True
user.save()
print("Successfully created")