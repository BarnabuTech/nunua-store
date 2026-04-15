# Generated manually for auto-setup

from django.db import migrations
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site


def create_superuser(apps, schema_editor):
    """Create superuser automatically on deployment"""
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@nunuastore.com',
            password='admin123'  # Change this after first login!
        )
        print("✓ Superuser 'admin' created with password 'admin123'")
        print("⚠ IMPORTANT: Change the password immediately after first login!")


def create_site(apps, schema_editor):
    """Ensure Site ID=1 exists with correct domain"""
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=1,
        defaults={
            'domain': 'nunua-store.onrender.com',
            'name': 'Nunua Store'
        }
    )
    print("✓ Site configured for nunua-store.onrender.com")


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('sites', '0002_alter_domain_unique'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_site, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(create_superuser, reverse_code=migrations.RunPython.noop),
    ]
