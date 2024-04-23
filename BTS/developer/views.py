from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from manager.models import Project
from django.db.models import F
from django.utils import timezone

@login_required
def developer_home(request):
    projects=Project.objects.all()  # Query set of all projects
    context={'projects' : projects}
    
    return render(request, 'developer/developer_home.html', context)

@login_required
def file_bug(request):
    if request.method == 'POST':
        form = forms.BugForm(request.POST)
        if form.is_valid():
            bug=form.save(commit=False) # commit=False because we want to modify the object beofre saving.
            bug.submitted_by = request.user  # Set the submitted_by field to the current user object (bcoz it is a foreign key)
            bug.date_submitted = timezone.now().date()  # Set the date_submitted field to the current date without timestamp
            bug.save()
            project = bug.project
            Project.objects.filter(id=project.id).update(bug_count=F('bug_count') + 1)
            return redirect('developerHome') 
    else:
        form = forms.BugForm()
    return render(request, 'developer/file_bug.html', {'form': form})


