'''
Run this script using command: python manage.py assign_permissions.
It will assign delete_project and delete_bug permission to 'manager101' user.
Only run it once, unless you are creating another user with role='Manager' who access manager homepage where he/she can delete projects. 
'''

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
User=get_user_model()

class Command(BaseCommand):
    help = 'Assign permissions to a user'

    def handle(self, *args, **options):
        # Retrieve the user objects
        user = User.objects.get(username='manager101')

        # Retrieve the permission objects
        permission1 = Permission.objects.get(codename='delete_project')  # Permission to delete project
        permission2 = Permission.objects.get(codename='delete_bug')   # Permission to delete bug

        # Assign the permissions to the users
        user.user_permissions.add(permission1)
        user.user_permissions.add(permission2)

        self.stdout.write(self.style.SUCCESS(f'Permission assigned successfully to {user.username}' ))
