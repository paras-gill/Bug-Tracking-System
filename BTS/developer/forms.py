from django import forms
from manager.models import Bug
from manager.models import Project
from django.utils import timezone

class BugForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), empty_label=None)
    submitted_by = forms.CharField(widget=forms.HiddenInput())
    date_submitted = forms.DateTimeField(widget=forms.HiddenInput())
    status = forms.BooleanField(initial=True, widget=forms.HiddenInput())

    class Meta:
        model = Bug
        fields = ['project', 'bug_title', 'impact', 'submitted_by', 'date_submitted', 'status']
        widgets = {
            'impact': forms.RadioSelect(choices=Bug.IMPACT_CHOICES, attrs={'class': 'horizontal-radio'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BugForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['submitted_by'].initial = user.username
            self.fields['date_submitted'].initial = timezone.now()
            self.fields['impact'].initial = Bug.SEVERE  # Set default value to 'Severe'
        
        # Set project field label to display project name
        self.fields['project'].label_from_instance = lambda obj: obj.project_name

    def clean_submitted_by(self):
        return self.cleaned_data['submitted_by']

    def clean_date_submitted(self):
        return self.cleaned_data['date_submitted']

    def clean_status(self):
        return self.cleaned_data['status']
