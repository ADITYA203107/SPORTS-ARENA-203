from django.core.management.base import BaseCommand
from apps.academies.models import APIKey


class Command(BaseCommand):
    help = 'Generate a new API key for the application'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, default='Default API Key', help='Name for the API key')
        parser.add_argument('--user', type=str, help='Username to associate with the API key')

    def handle(self, *args, **options):
        name = options['name']
        username = options.get('user')
        
        # Generate raw key
        raw_key = APIKey.generate_raw_key()
        hashed_key = APIKey.hash_key(raw_key)
        
        # Create API key object
        api_key_data = {
            'key': hashed_key,
            'name': name,
        }
        
        if username:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
                api_key_data['user'] = user
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User "{username}" not found'))
                return
        
        api_key = APIKey.objects.create(**api_key_data)
        
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('API KEY GENERATED SUCCESSFULLY'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.WARNING(f'Name: {name}'))
        self.stdout.write(self.style.WARNING(f'ID: {api_key.id}'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('YOUR API KEY (copy this now - it will not be shown again):'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.WARNING(f'  {raw_key}'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.NOTICE('Use this key in your API requests with header:'))
        self.stdout.write(self.style.NOTICE('  X-API-Key: <your-key>'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
