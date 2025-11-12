# create_superuser.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labsite.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
password = 'admin'
email = 'admin@example.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Суперпользователь '{username}' создан.")
else:
    print(f"Суперпользователь '{username}' уже существует.")
