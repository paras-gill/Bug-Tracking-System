from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from manager.models import Project, Bug
from django.db.models import F
from django.utils import timezone

@login_required
def developer_home(request):
    projects=Project.objects.all()  # Query set of all projects
    bugs_assigned=Bug.objects.filter(assign_to=request.user.pk)
    bugs_assigned_open=Bug.objects.filter(assign_to=request.user.pk, status='Open')
    bugs_submitted=Bug.objects.filter(submitted_by=request.user.pk)
    bugs_submitted_open=Bug.objects.filter(submitted_by=request.user.pk, status='Open')
    context={
        'projects' : projects, 
        'bugs_assigned' : bugs_assigned, 
        'bugs_assigned_open' : bugs_assigned_open,
        'bugs_submitted' : bugs_submitted,
        'bugs_submitted_open' : bugs_submitted_open,
        }
    
    return render(request, 'developer/developer_home.html', context)

@login_required
def file_bug(request):
    message=''
    if request.method == 'POST':
        form = forms.BugForm(request.POST)
        if form.is_valid():
            bug=form.save(commit=False) # commit=False because we want to modify the object beofre saving.
            bug.submitted_by = request.user  # Set the submitted_by field to the current user object (bcoz it is a foreign key)
            bug.date_submitted = timezone.now().date()  # Set the date_submitted field to the current date without timestamp
            bug.save()
            project = bug.project
            Project.objects.filter(id=project.id).update(bug_count=F('bug_count') + 1)
            message=f" <span style='color:blue;'> Bug with title <b>{bug.bug_title}</b> successfully filed for <b>{bug.project}</b> project </span>"
        else:
            message='<span style="color:red;"> A bug with this title already exists in the selected project.</span>'

    form = forms.BugForm()
    return render(request, 'developer/file_bug.html', {'form': form, 'message' : message})

@login_required
def change_status(request):
    pass
    #return redirect('developerHome')



