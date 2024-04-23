from django import forms
from manager.models import Bug
from manager.models import Project
from django.utils import timezone


class BugForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), empty_label=None)
    impact = forms.ChoiceField(choices=Bug.IMPACT_CHOICES, initial='Severe')

    class Meta:
        model = Bug
        fields = ['project', 'bug_title', 'impact',]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BugForm, self).__init__(*args, **kwargs)
        self.fields['project'].label_from_instance = lambda obj: obj.project_name  # Set project field label to display project name
        