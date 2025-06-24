from django.core.management.base import BaseCommand
from customers.models import Client, Domain
from datetime import date, timedelta
from getpass import getpass

class Command(BaseCommand):
    help = 'Interactively or via flags creates a new tenant with domain and optional superuser.'

    def add_arguments(self, parser):
        parser.add_argument('--schema', type=str, help='Tenant schema name')
        parser.add_argument('--name', type=str, help='Tenant name')
        parser.add_argument('--domain', type=str, help='Domain for the tenant')
        parser.add_argument('--email', type=str, help='Optional: Superuser email')
        parser.add_argument('--password', type=str, help='Optional: Superuser password')

    def handle(self, *args, **options):
        # Prompt interactively if not provided
        schema_name = options['schema'] or input("🧱 Enter schema name (e.g. tenant1): ").strip()
        name = options['name'] or input("🏷️  Enter tenant name: ").strip()
        domain_url = options['domain'] or input("🌐 Enter domain (e.g. tenant1.localhost): ").strip()

        tenant = Client.objects.create(
            schema_name=schema_name,
            name=name,
            paid_until=date.today() + timedelta(days=30),
            on_trial=True
        )
        self.stdout.write(self.style.SUCCESS(f'✅ Tenant `{name}` created with schema `{schema_name}`'))

        Domain.objects.create(
            domain=domain_url,
            tenant=tenant,
            is_primary=True
        )
        self.stdout.write(self.style.SUCCESS(f'🌍 Domain `{domain_url}` created for tenant'))

        # Superuser creation prompt (optional)
        create_user = input("👤 Create a superuser now? [y/N]: ").lower() == 'y'
        if create_user:
            email = options['email'] or input("📧 Email: ").strip()
            password = options['password'] or getpass("🔒 Password (input hidden): ").strip()

            from django_tenants.utils import schema_context
            from django.contrib.auth import get_user_model
            with schema_context(schema_name):
                User = get_user_model()
                User.objects.create_superuser(email=email, username=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'👑 Superuser `{email}` created successfully in `{schema_name}` schema.'))
