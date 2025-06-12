from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.db import transaction

class Command(BaseCommand):
    help = 'Cleans up duplicate social authentication configurations'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Get the default site
                site = Site.objects.get(id=1)
                
                # Get all Google social apps
                google_apps = SocialApp.objects.filter(provider='google')
                
                if google_apps.count() > 1:
                    # Keep the first one and delete the rest
                    first_app = google_apps.first()
                    self.stdout.write(self.style.SUCCESS(f'Found {google_apps.count()} Google apps'))
                    self.stdout.write(self.style.SUCCESS(f'Keeping Google app with ID: {first_app.id}'))
                    
                    # Delete the rest
                    deleted_count = 0
                    for app in google_apps.exclude(id=first_app.id):
                        app_id = app.id
                        app.delete()
                        deleted_count += 1
                        self.stdout.write(self.style.SUCCESS(f'Deleted duplicate Google app with ID: {app_id}'))
                    
                    # Ensure the remaining app is associated with the site
                    if site not in first_app.sites.all():
                        first_app.sites.add(site)
                        self.stdout.write(self.style.SUCCESS('Added site to remaining Google app'))
                    
                    self.stdout.write(self.style.SUCCESS(f'Successfully cleaned up {deleted_count} duplicate apps'))
                else:
                    self.stdout.write(self.style.SUCCESS('No duplicate Google apps found'))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            raise 