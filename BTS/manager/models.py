from django.db import models
from django.utils import timezone


class Project(models.Model):
    project_name = models.CharField(max_length=100, unique=True, error_messages={'unique': "Project with this name already exists."})
    date_added = models.DateTimeField(default=timezone.now)
    bug_count = models.IntegerField(default=0)
