from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Permission


class CustomUserManager(BaseUserManager):

    def normalize_username(self, username):
        """
        Normalize the username by lowercasing it and removing leading/trailing whitespace.
        """
        return username.strip().lower()
    
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('The Username field must be set')
        username = self.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class User(AbstractUser):
    
    MANAGER = 'Manager'
    DEVELOPER = 'Developer'
  
    ROLE_CHOICES = (
        (MANAGER, 'Manager'),
        (DEVELOPER, 'Developer'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Developer') 

    # Set the USERNAME_FIELD to 'username' for authentication
    username = models.CharField(max_length=150, unique=True)
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    # Now let's add fname and lname as fields for User class
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)


    objects = CustomUserManager()   


# Create custom permission for deleting projects
Permission.objects.get_or_create(codename='delete_project', name='Can delete project')

# If a permission with the specified codename doesn't exist, it creates one that's why get_or_create().

# Create custom permission for deleting bugs
Permission.objects.get_or_create(codename='delete_bug', name='Can delete bug')


