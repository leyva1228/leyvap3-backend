import json
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates superusers from env var or defaults'

    def handle(self, *args, **options):
        User = get_user_model()
        raw = os.environ.get('DJANGO_SUPERUSERS')
        if raw:
            try:
                users = json.loads(raw)
            except json.JSONDecodeError:
                self.stderr.write('Invalid DJANGO_SUPERUSERS JSON')
                return
        else:
            users = [
                {'username': 'john', 'password': '60480150', 'email': 'john@email.com'},
                {'username': 'omar', 'password': 'Tecsup2026', 'email': 'omar@email.com'},
            ]

        for u in users:
            username = u['username']
            password = u['password']
            email = u.get('email', f'{username}@email.com')
            if User.objects.filter(username=username).exists():
                self.stdout.write(f'Superuser "{username}" already exists, skipped')
            else:
                User.objects.create_superuser(username=username, password=password, email=email)
                self.stdout.write(f'Superuser "{username}" created')
