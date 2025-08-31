from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Creates the default site for the application'

    def handle(self, *args, **options):
        # Create or update the default site
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': '127.0.0.1:8000',
                'name': 'Nunua Store'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created site'))
        else:
            self.stdout.write(self.style.SUCCESS('Site already exists')) 