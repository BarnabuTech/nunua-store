from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from products.models import Product, Category
from allauth.socialaccount.models import SocialApp
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Checks database status and reports configuration issues'

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('=' * 60))
        self.stdout.write(self.style.HTTP_INFO('DATABASE STATUS CHECK'))
        self.stdout.write(self.style.HTTP_INFO('=' * 60))
        
        # Check Site configuration
        self.stdout.write(self.style.NOTICE('\n📍 Site Configuration:'))
        try:
            site = Site.objects.get(id=1)
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ Site ID=1 exists')
            )
            self.stdout.write(f'  Domain: {site.domain}')
            self.stdout.write(f'  Name: {site.name}')
        except Site.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('  ✗ Site ID=1 does NOT exist - this will cause 500 errors!')
            )
            self.stdout.write(
                self.style.WARNING('  Run: python manage.py setup_site')
            )
        
        # Check Products
        self.stdout.write(self.style.NOTICE('\n📦 Products:'))
        product_count = Product.objects.count()
        if product_count == 0:
            self.stdout.write(
                self.style.ERROR(f'  ✗ No products in database ({product_count} products)')
            )
            self.stdout.write(
                self.style.WARNING('  Products need to be added via Django Admin or fixtures')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ {product_count} products in database')
            )
        
        # Check Categories
        self.stdout.write(self.style.NOTICE('\n📁 Categories:'))
        category_count = Category.objects.count()
        if category_count == 0:
            self.stdout.write(
                self.style.WARNING(f'  ⚠ No categories in database ({category_count} categories)')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ {category_count} categories in database')
            )
        
        # Check Social Apps (for Google login)
        self.stdout.write(self.style.NOTICE('\n🔐 Social Apps (Google Login):'))
        try:
            google_app = SocialApp.objects.get(provider='google')
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ Google SocialApp exists')
            )
            sites = list(google_app.sites.all())
            if sites:
                self.stdout.write(f'  Linked to sites: {[s.domain for s in sites]}')
            else:
                self.stdout.write(
                    self.style.WARNING('  ⚠ Not linked to any sites')
                )
        except SocialApp.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('  ⚠ Google SocialApp does not exist')
            )
            self.stdout.write(
                self.style.WARNING('  Run: python manage.py setup_social_auth')
            )
        
        # Summary
        self.stdout.write(self.style.HTTP_INFO('\n' + '=' * 60))
        if product_count == 0:
            self.stdout.write(
                self.style.ERROR('ISSUE: Products are missing from the database!')
            )
            self.stdout.write(
                self.style.NOTICE('Solutions:')
            )
            self.stdout.write('  1. Go to Django Admin: https://nunua-store.onrender.com/admin/')
            self.stdout.write('  2. Log in with your superuser credentials')
            self.stdout.write('  3. Add products manually under Products > Products')
            self.stdout.write('  4. Or create a fixture file and load it: python manage.py loaddata products')
        
        self.stdout.write(self.style.HTTP_INFO('=' * 60))
