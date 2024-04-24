from django import forms
from manager.models import Bug
from manager.models import Project



class BugForm(forms.ModelForm):
    
    project = forms.ModelChoiceField(queryset=Project.objects.all(), empty_label=None) 
    # empty_label=None makes sure there is no empty choice at the top of the dropdown menu.
      
    impact = forms.ChoiceField(choices=Bug.IMPACT_CHOICES, initial='Severe')

    class Meta:
        model = Bug
        fields = ['project', 'bug_title', 'impact',]

    def clean(self):
            cleaned_data = super().clean()
            project = cleaned_data.get('project')
            bug_title = cleaned_data.get('bug_title')

            # Check if the bug_title is unique within the selected project
            if Bug.objects.filter(project=project, bug_title=bug_title).exists():
                raise forms.ValidationError("A bug with this title already exists in the selected project.")

            return cleaned_data