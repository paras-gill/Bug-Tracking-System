from django.db import models
from django.utils import timezone
#from developer.models import Bug

from django.contrib.auth import get_user_model
User=get_user_model()


class Project(models.Model):
    project_name = models.CharField(max_length=100, unique=True, error_messages={'unique': "Project with this name already exists."})
    date_added = models.DateTimeField(default=timezone.now)
    bug_count = models.IntegerField(default=0)




class Bug(models.Model):
    SEVERE = 'Severe'
    NORMAL = 'Normal'
    IMPACT_CHOICES = [
        (SEVERE, 'Severe'),
        (NORMAL, 'Normal'),
    ]

    OPEN = 'Open'
    CLOSED = 'Closed'
    STATUS_CHOICES = [
        (OPEN, 'True'),
        (CLOSED,'Closed')  
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    bug_title = models.CharField(max_length=100)
    impact = models.CharField(max_length=10, choices=IMPACT_CHOICES,  default='severe')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_bugs')
    date_submitted = models.DateTimeField()
    status = models.CharField(max_length=10, default='Open', choices=STATUS_CHOICES)
    assign_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_bugs', null=True, blank=True)
    date_assigned = models.DateTimeField(null=True, blank=True)