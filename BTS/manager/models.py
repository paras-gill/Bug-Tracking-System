from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User=get_user_model()


class Project(models.Model):
    project_name = models.CharField(max_length=100, unique=True, error_messages={'unique': "Project with this name already exists."})
    date_added = models.DateTimeField(default=timezone.now)
    bug_count = models.IntegerField(default=0)

    
    def __str__(self):
        return self.project_name
    

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

    def __str__(self):
        return self.bug_title
    

    # Difference between null and blank:
    '''
    Difference between null and blank: 
    -----------------------------------

    1.  null: Applies at the database level. It determines whether a field can be set to NULL in the database. 
        If null=True, it means the field can have a NULL value in the database, indicating the absence of a value.

    2. blank: Applies at the validation level, particularly in forms. It determines whether a field is required 
       when submitting data through a form. If blank=True, it means the field is not required and can be left blank 
       in forms.

    In form when a field is not filled i.e. it is kept blank, then at database level null value is stored in that field.
    If a form field is left blank and the corresponding model field does not have null=True, Django will not allow the 
    empty value, and an error will be raised during form validation unless blank=True is also set for the field.
    
    Then why do we need seprate attribute for null and blank when defining django model class?
    Separating these concerns allows for more flexibility and clarity in defining the behavior of your models and forms. 
    It allows you to specify whether a field is optional in forms (blank) independently of whether it can be NULL in the 
    database (null).
    
    '''

    # What is related_name parameter?
    '''
    What is related_name parameter?
    --------------------------------

    The related_name attribute in a Django model class is used to specify the name of the reverse relation from the related 
    model back to the model that defines the relationship.

    When you define a ForeignKey, OneToOneField, or ManyToManyField in a Django model, it automatically creates a reverse 
    relation for you. By default, the name of this reverse relation is the name of the model that defines the ForeignKey, 
    OneToOneField, or ManyToManyField, followed by "_set". For example, if you have a ForeignKey from Author to Book, Django 
    will create a reverse relation on the Book model called author_set.

    However, you can use the related_name attribute to specify a custom name for this reverse relation. This can be useful for 
    making your code more readable and for avoiding clashes with other related models.

    '''

    # What is on_delete parameter of model class attributes?
    '''
    What is on_delete parameter of model class attributes?
    ------------------------------------------------------
    The on_delete attribute in Django models specifies the behavior to adopt when the referenced object is deleted. It applies to 
    ForeignKey, OneToOneField, and many-to-many relationships.

    Possible values for on_delete:
    
    1. models.CASCADE: When the referenced object is deleted, also delete the objects that have a foreign key pointing to it. 
    2. models.PROTECT: Prevent deletion of the referenced object by raising a ProtectedError exception. 
    etc.
    '''

    