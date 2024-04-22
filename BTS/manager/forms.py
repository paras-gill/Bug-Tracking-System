from django import forms
from .models import Project

class UploadProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name']
