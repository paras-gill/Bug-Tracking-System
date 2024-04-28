from django import forms
from manager.models import Bug
from manager.models import Project


class BugForm(forms.ModelForm):
    
    project = forms.ModelChoiceField(queryset = Project.objects.all(), empty_label =None) 
    # empty_label = None makes sure there is no empty choice at the top of the dropdown menu.
      
    impact = forms.ChoiceField(choices =[('', 'Select Impact')] + Bug.IMPACT_CHOICES, initial = '', required=True)

    class Meta:
        model = Bug
        fields = ['project', 'bug_title', 'impact',]

    def clean(self):
            cleaned_data = super().clean()
            project = cleaned_data.get('project')
            bug_title = cleaned_data.get('bug_title')
            impact = cleaned_data.get('impact')

            # Check if the bug_title is unique within the selected project
            if Bug.objects.filter(project = project, bug_title = bug_title).exists():
                raise forms.ValidationError("A bug with this title already exists in the selected project.")
            
            # Check if a valid impact value is selected
            if impact == '':
                raise forms.ValidationError("Please select a valid value for impact.")

            return cleaned_data


class ChangeStatusForm(forms.ModelForm):   
    class Meta:
        model = Bug
        fields = ['resolve']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resolve'].label = ''
        self.fields['resolve'].widget = forms.RadioSelect(choices=[(True, 'Close')])
        self.fields['resolve'].required = True
 