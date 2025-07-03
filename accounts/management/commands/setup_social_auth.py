from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings
from decouple import config

class Command(BaseCommand):
    help = 'Sets up social authentication for the application'

    def handle(self, *args, **options):
        # Get or create the default site
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': 'localhost:8000',
                'name': 'Nunua Store'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created default site'))
        
        # Get or create Google social app
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google',
                'client_id': config('GOOGLE_CLIENT_ID', default=''),
                'secret': config('GOOGLE_CLIENT_SECRET', default='')
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created Google social app'))
        
        # Add site to social app if not already added
        if site not in google_app.sites.all():
            google_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS('Added site to Google social app'))
        
        self.stdout.write(self.style.SUCCESS('Social authentication setup completed')) 