from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings
import logging
import os

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Configures the Django Site model for production deployment'

    def handle(self, *args, **options):
        # Get the primary domain from ALLOWED_HOSTS
        domain = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'
        
        # Remove protocol prefix if present
        if domain.startswith(('http://', 'https://')):
            domain = domain.split('://', 1)[1]
        
        # Remove port if present
        if ':' in domain:
            domain = domain.split(':', 1)[0]
        
        # Remove www. prefix for consistency
        if domain.startswith('www.'):
            domain = domain[4:]
            
        try:
            # Update or create the site with ID=1
            site, created = Site.objects.update_or_create(
                id=1,
                defaults={
                    'domain': domain,
                    'name': 'Nunua Store'
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created site with domain: {domain}')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated site domain to: {domain}')
                )
                
            logger.info(f'Site configured with domain: {domain}')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error configuring site: {str(e)}')
            )
            logger.error(f'Failed to configure site: {str(e)}')
            raise
        
        # Load products if they don't exist
        try:
            from products.models import Product
            product_count = Product.objects.count()
            
            if product_count == 0:
                fixture_path = 'data/products.json'
                if os.path.exists(fixture_path):
                    self.stdout.write('Loading products from fixture...')
                    from django.core.management import call_command
                    call_command('loaddata', fixture_path)
                    self.stdout.write(
                        self.style.SUCCESS('Products loaded successfully!')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'No products found and fixture not found at {fixture_path}')
                    )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Products already exist: {product_count} products')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading products: {str(e)}')
            )
            logger.error(f'Failed to load products: {str(e)}')
