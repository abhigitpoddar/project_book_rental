from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "automatically creates a superuser"

    def handle(self, *args, **kwargs) -> None:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('superuser already exists'))
