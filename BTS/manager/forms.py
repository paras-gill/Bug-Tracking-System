from django import forms
from .models import Project, Bug

from django.contrib.auth import get_user_model
User=get_user_model()

class UploadProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name']

        
class AssignBugForm(forms.Form):
    def project_bug_choices():
        """Returns a list of tuples with project-bug pairs for projects with non-zero bug_count."""
        project_bug_choices = []
        projects = Project.objects.filter(bug_count__gt=0)  
        for project in projects:
            bugs = project.bug_set.all()  # bug_set is the default reverse relation created by django
            for bug in bugs:
                # List only those bugs which have not been assigned yet. 
                if bug.assign_to == None:
                    project_bug_choices.append((f"{bug.pk}", f"{bug} ({project})"))
        return project_bug_choices
    
    project_bug = forms.ChoiceField(choices=project_bug_choices, label="Select bug")
    assigned_to = forms.ModelChoiceField(queryset=User.objects.filter(role='developer'), empty_label=None)

