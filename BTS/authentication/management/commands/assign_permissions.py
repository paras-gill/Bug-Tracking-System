'''
Run this script using command: python manage.py assign_permissions.
It will assign delete_project permission to 'admin101' user.
Only run it once, unless you are creating another user with role='Manager' who access manager homepage where he/she can delete projects. 
'''

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
User=get_user_model()

class Command(BaseCommand):
    help = 'Assign permissions to a user'

    def handle(self, *args, **options):
        # Retrieve the user object
        user = User.objects.get(username='admin101')

        # Retrieve the permission object
        permission = Permission.objects.get(codename='delete_project')

        # Assign the permission to the user
        user.user_permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Permission assigned successfully'))
