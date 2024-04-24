from django import forms
from .models import Project, Bug

from django.contrib.auth import get_user_model
User=get_user_model()

class UploadProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name']

'''
class AssignBugForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=User.objects.filter(role='developer'), empty_label=None)

    class Meta:
        model = Bug
        fields = ['bug_title', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super(AssignBugForm).__init__(*args, **kwargs)
        projects=Project.objects.exclude(bug_count=0)
        bugs=Bug.objects.filter()
'''
        
class AssignBugForm(forms.Form):
    def project_bug_choices():
        """Returns a list of tuples with project-bug pairs for projects with non-zero bug_count."""
        project_bug_choices = []
        projects = Project.objects.filter(bug_count__gt=0)  # __gt is greater than comparision operator for query sets
        for project in projects:
            bugs = project.bug_set.all()  # bug_set is the default reverse relation created by django
            for bug in bugs:
                # List only those bugs which have not been assigned yet. 
                if bug.assign_to == None:
                    project_bug_choices.append((f"{bug.pk}", f"{bug} ({project})"))
        return project_bug_choices
    
    project_bug = forms.ChoiceField(choices=project_bug_choices, label="Select bug")
    assigned_to = forms.ModelChoiceField(queryset=User.objects.filter(role='developer'), empty_label=None)


# Since we have to update this assignment in Bug table and we are not using forms.ModelForm as parent class, we'll
# have define custom  clean_project_bug() method to seprate out project value and bug value out of project_bug form field; which can then
# be saved using the view function.
'''
    def clean_project_bug(self):
        project_bug = self.cleaned_data.get('project_bug')  # cleaned_data is a dictionary-like object that contains validated form data.
        if project_bug:
            try:
                bug = Bug.objects.get(pk=project_bug)
                self.cleaned_data['bug'] = bug
                self.cleaned_data['project'] = bug.project
            except Bug.DoesNotExist:
                raise forms.ValidationError("Invalid project-bug selection.")
        return project_bug
'''    




# Difference between forms.Form and forms.ModelForm parent classes
'''
Difference between forms.Form and forms.ModelForm parent classes
-----------------------------------------------------------------

These are two parent classes provided by Django for creating forms.

1. forms.Form
    - It's used when you need to create a form that doesn't directly map to a model in the database.
    - You define form fields explicitly in the form class, and you're responsible for handling the data 
      processing and validation manually.
    - You would use forms.Form when you need to create a form for purposes other than interacting directly 
      with database models, such as search forms, contact forms, or forms for user registration where you 
      might need to perform custom validation or processing.

2. forms.ModelForm
    - This is a form class specifically designed to work with Django models.
    - It's used when you want to create a form that directly maps to a model in the database.
    - It automatically generates form fields based on the fields in the model you specify.
    - It provides built-in support for validation and saving data to the database, leveraging the model's 
      field definitions and validation rules.
    - You would use forms.ModelForm when you want to create a form for CRUD (Create, Read, Update, Delete) 
      operations on database models, such as creating a form for adding or editing model instances through a 
      web interface.

'''  


# What are query sets
'''
What are query sets?
--------------------

In Django, a queryset is a collection of database query results represented as a Python data structure. It is 
essentially a list of objects returned from a database query, where each object corresponds to a row in the 
database table that matches the query criteria.

Querysets are lazy, meaning that the actual database query is not executed until the data is needed. This allows 
for efficient handling of large datasets, as the database query is only executed when necessary.

Some common queryset methods include filter(), exclude(), order_by(), annotate(), aggregate(), count(), exists(), etc.

'''


# What is cleaned_data
'''
What is cleaned_data?
---------------------

cleaned_data is a dictionary-like object that contains validated form data. It's typically accessed after form validation 
is performed, and it provides cleaned and validated values for each form field.

Here's how it works:

    When you call form.is_valid(), Django runs the validation logic defined in your form class. If validation passes, the 
    cleaned data is stored in the cleaned_data attribute of the form instance.
    
    The cleaned_data dictionary contains the cleaned and validated values for each form field, with keys corresponding to 
    the field names.
    
    The values in cleaned_data are Python objects that have been converted and validated based on the field types and any 
    custom validation logic defined in your form class.

'''